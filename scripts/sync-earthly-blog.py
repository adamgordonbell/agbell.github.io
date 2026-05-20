#!/usr/bin/env python3
"""Sync Earthly blog posts authored by Adam → data/earthly_blog.json.

Two-step scrape:
  1. List page https://earthly.dev/blog/authors/adam/ → all post slugs and titles
  2. Per-post page fetch → og:title, og:description, article:published_time

Earthly is frozen — no new posts coming — so this script is run once and the
cache file is the canonical record. Re-running is idempotent.

Editorial overrides live in data/earthly_blog_overrides.yaml.

Usage: scripts/sync-earthly-blog.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

AUTHOR_URL = "https://earthly.dev/blog/authors/adam/"
BASE = "https://earthly.dev"
OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "earthly_blog.json"


def http_get(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "sync-earthly-blog/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", errors="replace")


def extract_og(html: str, prop: str) -> str | None:
    m = re.search(
        rf'<meta\s+property=["\']og:{re.escape(prop)}["\']\s+content=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    )
    return m.group(1) if m else None


def extract_published(html: str) -> str | None:
    m = re.search(
        r'<meta\s+property=["\']article:published_time["\']\s+content=["\']([^"\']*)["\']',
        html, re.IGNORECASE,
    )
    return m.group(1)[:10] if m else None


def list_posts() -> list[tuple[str, str]]:
    """Return [(slug, listed_title)] of all posts attributed to Adam."""
    html = http_get(AUTHOR_URL)
    pairs = []
    for m in re.finditer(r'<li>\s*<a href="(/blog/([a-z0-9-]+)/?)">([^<]+)</a>', html):
        slug = m.group(2)
        title = m.group(3).strip()
        pairs.append((slug, title))
    # Dedupe by slug (the page lists Featured then chronological)
    seen = set()
    out = []
    for slug, title in pairs:
        if slug in seen:
            continue
        seen.add(slug)
        out.append((slug, title))
    return out


def fetch_post(slug: str, listed_title: str) -> dict | None:
    url = f"{BASE}/blog/{slug}/"
    try:
        html = http_get(url)
    except Exception as e:
        print(f"  ! fetch failed {url}: {e}", file=sys.stderr)
        return None

    title = extract_og(html, "title") or listed_title
    description = extract_og(html, "description") or ""
    date = extract_published(html) or ""
    if not date:
        return None

    return {
        "title": title,
        "url": url,
        "date": date,
        "slug": slug,
        "description": description,
    }


def main() -> int:
    print("Fetching author page…")
    pairs = list_posts()
    print(f"  → {len(pairs)} Adam-attributed posts")

    print("Fetching each post (concurrent)…")
    items = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        futures = {pool.submit(fetch_post, slug, title): slug for slug, title in pairs}
        for fut in as_completed(futures):
            it = fut.result()
            if it:
                items.append(it)

    items.sort(key=lambda x: x["date"], reverse=True)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps({"items": items}, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(items)} Earthly posts to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
