#!/usr/bin/env python3
"""Sync CoRecursive episodes into data/corecursive.json.

Strategy:
  1. Pull corecursive.com/sitemap.xml → list of every page URL the site publishes.
  2. Filter to episode URLs (heuristic: top-level slug, excluding known meta paths).
  3. For each episode URL, fetch the page concurrently and parse og:title / og:description.
  4. Cross-reference the RSS feed for episode_number and duration where available
     (matched by canonical URL; feed metadata is messy on old episodes so we treat
     it as a supplement, not source of truth).

The feed alone is unreliable for older episodes (broken <link> tags, duplicates,
mp3-only URLs). The website's sitemap + per-page og: metadata is.

Editorial overrides live in data/corecursive_overrides.yaml and win at render time.

Usage: scripts/sync-corecursive.py
"""

from __future__ import annotations

import html
import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET

SITEMAP_URL = "https://corecursive.com/sitemap.xml"
FEED_URL = "https://corecursive.com/feed"
OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "corecursive.json"

# Sitemap URLs to skip — these aren't episodes.
SKIP_PATH_PREFIXES = (
    "/tags/", "/technologies/", "/story_types/", "/collections/",
    "/rankings/", "/category/", "/api/", "/host/", "/about/", "/links/",
    "/book/", "/book2/", "/donate/", "/supporters/", "/newsletter/",
    "/reinforcement/", "/record/", "/feed/", "/slack/", "/subscribe/",
    "/debug/", "/guest-guide/", "/episodes/", "/fan-favorites/",
    "/toc-manifest.json",
)
SKIP_EXACT = {"/", ""}

NS = {
    "sm": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
}


def http_get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "sync-corecursive/2.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def slug_from_url(url: str) -> str:
    return url.rstrip("/").rsplit("/", 1)[-1]


def parse_guest(title: str) -> str | None:
    m = re.search(r"\s+[Ww]ith\s+(.+?)\s*$", title)
    return m.group(1) if m else None


def list_episode_urls() -> list[tuple[str, str]]:
    """Return [(url, lastmod_yyyy_mm_dd), ...] of episode pages from sitemap."""
    xml_text = http_get(SITEMAP_URL)
    root = ET.fromstring(xml_text)
    out: list[tuple[str, str]] = []
    for url_el in root.findall("sm:url", NS):
        loc_el = url_el.find("sm:loc", NS)
        lastmod_el = url_el.find("sm:lastmod", NS)
        if loc_el is None or not loc_el.text:
            continue
        loc = loc_el.text.strip()
        if not loc.startswith("https://corecursive.com/"):
            continue
        path = loc[len("https://corecursive.com"):]
        if path in SKIP_EXACT or any(path.startswith(p) for p in SKIP_PATH_PREFIXES):
            continue
        lastmod = ""
        if lastmod_el is not None and lastmod_el.text:
            lastmod = lastmod_el.text[:10]  # yyyy-mm-dd
        out.append((loc, lastmod))
    return out


def _attr(html: str, pattern: str) -> str | None:
    # Match content="..." OR content='...' — capture only up to the SAME quote
    # that opened it, so apostrophes inside double-quoted values don't truncate.
    m = re.search(pattern + r'\s+content=(["\'])(.*?)\1', html, re.IGNORECASE | re.DOTALL)
    return m.group(2) if m else None


def extract_og(html: str, prop: str) -> str | None:
    return _attr(html, rf'<meta\s+property=["\']og:{re.escape(prop)}["\']')


def extract_published_time(html: str) -> str | None:
    v = _attr(html, r'<meta\s+property=["\']article:published_time["\']')
    return v[:10] if v else None


def normalize_description(s: str) -> str:
    s = html.unescape(s)
    s = re.sub(r"^\s*#+\s+\*\*[^*]+\*\*\s*", "", s)
    s = re.sub(r"^\s*#+\s+.+?\n", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def fetch_episode(url: str, fallback_date: str) -> dict | None:
    try:
        html = http_get(url)
    except Exception as e:
        print(f"  ! fetch failed {url}: {e}", file=sys.stderr)
        return None

    title = extract_og(html, "title")
    if not title:
        return None  # not an episode page

    description = extract_og(html, "description") or ""
    image = extract_og(html, "image") or ""
    date = extract_published_time(html) or fallback_date

    item = {
        "title": title,
        "url": url,
        "date": date,
        "slug": slug_from_url(url),
        "description": normalize_description(description),
    }
    if image:
        item["image"] = image
    guest = parse_guest(title)
    if guest:
        item["with"] = guest
    return item


def feed_supplements() -> dict[str, dict]:
    """Map slug → {episode_number, duration} from the RSS feed (best-effort)."""
    try:
        xml_text = http_get(FEED_URL)
        root = ET.fromstring(xml_text)
    except Exception as e:
        print(f"  ! feed unavailable: {e}", file=sys.stderr)
        return {}
    out: dict[str, dict] = {}
    channel = root.find("channel")
    if channel is None:
        return out
    for it in channel.findall("item"):
        link = (it.findtext("link") or "").strip()
        if not link.startswith("https://corecursive.com/"):
            continue
        slug = slug_from_url(link)
        if not slug or slug.endswith(".mp3"):
            continue
        ep = it.findtext("itunes:episode", default="", namespaces=NS).strip()
        dur = it.findtext("itunes:duration", default="", namespaces=NS).strip()
        supp = {}
        if ep.isdigit():
            supp["episode_number"] = int(ep)
        if dur:
            supp["duration"] = dur
        if supp:
            out[slug] = supp
    return out


def main() -> int:
    print("Fetching sitemap…")
    pairs = list_episode_urls()
    print(f"  → {len(pairs)} candidate episode URLs")

    print("Fetching episode pages (concurrent)…")
    items: list[dict] = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = {pool.submit(fetch_episode, url, lastmod): url for url, lastmod in pairs}
        for fut in as_completed(futures):
            it = fut.result()
            if it:
                items.append(it)

    print("Fetching feed for episode_number/duration…")
    supp = feed_supplements()
    for it in items:
        if it["slug"] in supp:
            it.update(supp[it["slug"]])

    items.sort(key=lambda x: x["date"], reverse=True)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps({"items": items}, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(items)} episodes to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
