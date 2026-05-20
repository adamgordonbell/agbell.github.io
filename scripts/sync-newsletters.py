#!/usr/bin/env python3
"""Sync CoRecursive newsletter posts into data/newsletters.json.

Pulls from Kit's (formerly ConvertKit) public profile API:
  https://newsletter.corecursive.com/profile/fetch-posts?page=1&per_page=200

Editorial overrides live in data/newsletters_overrides.yaml and win at render time.

Usage: scripts/sync-newsletters.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

API_URL = "https://newsletter.corecursive.com/profile/fetch-posts?page=1&per_page=500"
TARGET = "writing.yaml"
SOURCE = "corecursive-newsletter"
TYPE = "newsletter"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_yaml_sync import make_item, merge_and_save  # noqa: E402


def http_get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={
        "User-Agent": "sync-newsletters/1.0",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


_MONTHS = (
    "January|February|March|April|May|June|July|August|"
    "September|October|November|December|"
    "Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
)
# "Adam Gordon Bell May 2nd Hey!" / "Adam Gordon Bell July 4th Hey!"
_BYLINE_HEY = re.compile(
    rf"^\s*Adam Gordon Bell\s+(?:{_MONTHS})\s+\d{{1,2}}(?:st|nd|rd|th)?\s+Hey[!,]?\s*",
    re.IGNORECASE,
)
# "Hello CoRecursive newsletter subscriber!"  / variants
_HELLO_SUB = re.compile(
    r"^\s*Hello\s+CoRecursive\s+newsletter\s+subscribers?[!,.]?\s*",
    re.IGNORECASE,
)
# Bare "Hey!" / "Hey," at the start of a cleaned intro
_BARE_HEY = re.compile(r"^\s*Hey[!,]?\s+", re.IGNORECASE)


def clean_intro(raw: str, max_len: int = 280) -> str:
    s = (raw or "").strip()
    # Strip Kit's standard byline / greeting prefixes
    for pat in (_BYLINE_HEY, _HELLO_SUB):
        s = pat.sub("", s, count=1)
    s = _BARE_HEY.sub("", s, count=1)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= max_len:
        return s
    cut = s[:max_len].rsplit(" ", 1)[0]
    return cut + "…"


def to_yyyy_mm_dd(iso: str) -> str:
    # "2025-05-02T11:20:18.000Z"
    return iso[:10]


def main() -> int:
    data = http_get_json(API_URL)
    posts = data.get("posts", [])
    if data.get("hasMore"):
        print("Warning: API reports hasMore=true; bump per_page in the script", file=sys.stderr)

    items = []
    for p in posts:
        title = (p.get("title") or "").strip()
        url = p.get("url") or ""
        published = p.get("publishedAt") or p.get("campaignCompletedAt") or ""
        if not (title and url and published):
            continue
        items.append({
            "title": title,
            "url": url,
            "date": to_yyyy_mm_dd(published),
            "slug": p.get("slug") or "",
            "description": clean_intro(p.get("introContent") or ""),
        })

    new = [
        make_item(
            type_=TYPE, source=SOURCE,
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
