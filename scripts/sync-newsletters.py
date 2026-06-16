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
# "Adam Gordon Bell May 2nd " — the byline prefix. Allow loose suffixes
# (e.g. typoed "2nth") with \w*. Stripped first, then the title/greeting
# that comes immediately after is stripped by _LEAD_TO_GREETING.
_BYLINE = re.compile(
    rf"^\s*Adam Gordon Bell\s+(?:{_MONTHS})\s+\d{{1,2}}\w*\s+",
    re.IGNORECASE,
)
# After the byline, intros tend to read either "Hey!", or "{Title} Hello, ..."
# or "{Title} Welcome to {month} ...". Strip everything up to and including
# the greeting + its punctuation + an optional "CoRecursive newsletter
# subscriber" suffix.
_LEAD_TO_GREETING = re.compile(
    r"^.{0,120}?\b(?:Hey|Hello|Welcome(?:\s+to)?|Hi|Happy(?:\s+\w+)?)\b[\s,!.:]*(?:CoRecursive\s+newsletter\s+subscribers?[\s,!.:]*)?",
    re.IGNORECASE | re.DOTALL,
)
# Fallback: standalone "Hello CoRecursive newsletter subscribers,"
_HELLO_SUB = re.compile(
    r"^\s*Hello\s+CoRecursive\s+newsletter\s+subscribers?[!,.\s]*",
    re.IGNORECASE,
)
# Fallback: bare "newsletter subscriber," at start (if byline ate the "Hello")
_BARE_SUB = re.compile(
    r"^\s*newsletter\s+subscribers?[,.\s]*",
    re.IGNORECASE,
)


def clean_intro(raw: str, max_len: int = 280) -> str:
    s = (raw or "").strip()
    s = _BYLINE.sub("", s, count=1)
    s = _LEAD_TO_GREETING.sub("", s, count=1)
    s = _HELLO_SUB.sub("", s, count=1)
    s = _BARE_SUB.sub("", s, count=1)
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
