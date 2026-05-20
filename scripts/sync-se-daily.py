#!/usr/bin/env python3
"""Sync Software Engineering Daily episodes featuring Adam → data/se_daily.json.

Scrapes softwareengineeringdaily.com/tag/adam-gordon-bell/ for episode URLs,
filters to ones whose slug contains "adam-gordon-bell" (Adam-featuring), then
fetches each page for og:title / og:description / published_time.

Editorial overrides live in data/se_daily_overrides.yaml.

Usage: scripts/sync-se-daily.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

TAG_URL = "https://softwareengineeringdaily.com/tag/adam-gordon-bell/"
TARGET = "podcasts.yaml"
SOURCE = "se-daily"
TYPE = "podcast"
ROLE = "guest"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_yaml_sync import make_item, merge_and_save  # noqa: E402

POST_URL_RE = re.compile(
    r"https://softwareengineeringdaily\.com/\d{4}/\d{2}/\d{2}/[a-z0-9-]+/?"
)


def http_get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "sync-se-daily/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def extract_og(html: str, prop: str) -> str | None:
    m = re.search(
        rf'<meta\s+property=["\']og:{re.escape(prop)}["\']\s+content=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    )
    return m.group(1) if m else None


def extract_published(html: str, url: str = "") -> str | None:
    m = re.search(
        r'<meta\s+property=["\']article:published_time["\']\s+content=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    )
    if m:
        return m.group(1)[:10]
    # URL-embedded /YYYY/MM/DD/
    m = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", url)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


def slug_from_url(url: str) -> str:
    return url.rstrip("/").rsplit("/", 1)[-1]


def list_episodes() -> list[str]:
    html = http_get(TAG_URL)
    # Filter to URLs whose slug includes "adam-gordon-bell" (so only Adam's
    # episodes, not sidebar recommended posts).
    urls = set()
    for m in POST_URL_RE.finditer(html):
        url = m.group(0).rstrip("/") + "/"
        if "adam-gordon-bell" in slug_from_url(url):
            urls.add(url)
    return sorted(urls)


def fetch_episode(url: str) -> dict | None:
    try:
        html = http_get(url)
    except Exception as e:
        print(f"  ! fetch failed {url}: {e}", file=sys.stderr)
        return None
    title = extract_og(html, "title")
    if not title:
        return None
    title = re.sub(r"\s*[–—-]\s*Software Engineering Daily\s*$", "", title).strip()
    description = extract_og(html, "description") or ""
    date = extract_published(html, url)
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
    urls = list_episodes()
    print(f"Found {len(urls)} Adam-featuring SED episodes")
    items = []
    with ThreadPoolExecutor(max_workers=4) as pool:
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
