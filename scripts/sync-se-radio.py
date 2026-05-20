#!/usr/bin/env python3
"""Sync Software Engineering Radio episodes hosted by Adam → data/se_radio.json.

Strategy: paginate WordPress search at se-radio.net/?s=Adam+Gordon+Bell, collect
unique episode URLs (filter out sidebar "latest" injection), then fetch each
page for og:title, og:description, article:published_time.

Episode list grew while Adam was hosting (2019-2020). Re-runnable when new
episodes ship that include his name in the text.

Editorial overrides live in data/se_radio_overrides.yaml.

Usage: scripts/sync-se-radio.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SEARCH_BASE = "https://se-radio.net"
QUERY = "Adam Gordon Bell"
MAX_PAGES = 5
TARGET = "podcasts.yaml"
SOURCE = "se-radio"
TYPE = "podcast"
ROLE = "host"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_yaml_sync import make_item, merge_and_save  # noqa: E402

# Sidebar "latest episodes" injection — same on every search page. These get
# filtered out by appearing on every page.
EPISODE_URL_RE = re.compile(
    r'href="(https://se-radio\.net/20\d{2}/\d{2}/[a-z0-9-]+/?)"'
)


def http_get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "sync-se-radio/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


_TITLE_SUFFIX = re.compile(r"\s*[–—-]\s*Software Engineering Radio\s*$")
_TITLE_PREFIX = re.compile(r"^(SE Radio\s+)?(Episode\s+)?\d+\s*[:\-–—]\s*", re.IGNORECASE)


def extract_title(html: str) -> str | None:
    m = re.search(r"<title>([^<]+)</title>", html)
    if not m:
        return None
    import html as html_lib
    t = html_lib.unescape(m.group(1)).strip()
    t = _TITLE_SUFFIX.sub("", t)
    t = _TITLE_PREFIX.sub("", t)
    return t


_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12,
}


def extract_published(html: str, url: str = "") -> str | None:
    # 1. <time datetime="ISO">
    m = re.search(r'<time[^>]*datetime="([^"]+)"', html)
    if m:
        return m.group(1)[:10]
    # 2. <span class="updated">Month D, YYYY</span>
    m = re.search(r'class="updated"[^>]*>([^<]+)<', html)
    if m:
        s = m.group(1).strip()
        m2 = re.match(r"(\w+)\s+(\d{1,2}),\s*(\d{4})", s)
        if m2:
            month_name, day, year = m2.group(1).lower(), int(m2.group(2)), int(m2.group(3))
            month = _MONTHS.get(month_name)
            if month:
                return f"{year:04d}-{month:02d}-{day:02d}"
    # 3. URL-derived fallback (YYYY/MM/)
    m = re.search(r"/(\d{4})/(\d{2})/", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}-01"
    return None


def extract_excerpt(html: str) -> str:
    import html as html_lib
    # SE Radio episode pages have no meta description. Pull the first
    # substantive <p> from the entry-content block.
    m = re.search(r'class="entry-content[^"]*"[^>]*>(.+?)(?:<footer|</article)', html, re.DOTALL)
    if not m:
        return ""
    body = m.group(1)
    for raw_p in re.findall(r"<p[^>]*>(.+?)</p>", body, re.DOTALL):
        text = re.sub(r"<[^>]+>", "", raw_p)
        text = html_lib.unescape(text).replace("\xa0", " ")
        text = re.sub(r"\s+", " ", text).strip()
        # Skip music credits / sponsor blurbs
        if len(text) < 50:
            continue
        if text.startswith("SE Radio theme music"):
            continue
        return text
    return ""


def slug_from_url(url: str) -> str:
    return url.rstrip("/").rsplit("/", 1)[-1]


ARTICLE_BLOCK_RE = re.compile(r"<article[^>]*>(.+?)</article>", re.DOTALL)


def list_episodes() -> list[str]:
    """Return unique episode URLs from real search results (inside <article>),
    not sidebar 'latest episodes' injection."""
    found: set[str] = set()
    for p in range(1, MAX_PAGES + 1):
        path = "/" if p == 1 else f"/page/{p}/"
        url = f"{SEARCH_BASE}{path}?s={urllib.parse.quote_plus(QUERY)}"
        try:
            html = http_get(url)
        except Exception:
            break
        page_count_before = len(found)
        for block in ARTICLE_BLOCK_RE.finditer(html):
            for m in EPISODE_URL_RE.finditer(block.group(1)):
                found.add(m.group(1).rstrip("/") + "/")
        if len(found) == page_count_before:
            break  # no new results → done paginating
    return sorted(found)


def fetch_episode(url: str) -> dict | None:
    try:
        html = http_get(url)
    except Exception as e:
        print(f"  ! fetch failed {url}: {e}", file=sys.stderr)
        return None

    title = extract_title(html)
    if not title:
        return None
    description = extract_excerpt(html)
    date = extract_published(html, url) or ""
    if not date:
        return None

    return {
        "title": title,
        "url": url,
        "date": date,
        "slug": slug_from_url(url),
        "description": description,
    }


def main() -> int:
    print("Searching SE Radio…")
    urls = list_episodes()
    print(f"  → {len(urls)} candidate episode URLs")

    items = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(fetch_episode, u): u for u in urls}
        for fut in as_completed(futures):
            it = fut.result()
            if it:
                items.append(it)

    new = [
        make_item(
            type_=TYPE, role=ROLE, source=SOURCE,
            title=it["title"], url=it["url"], date=it["date"],
            slug=it.get("slug"), description=it.get("description"),
        )
        for it in items
    ]
    added, skipped = merge_and_save(TARGET, new)
    print(f"  → {added} new, {skipped} already in {TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
