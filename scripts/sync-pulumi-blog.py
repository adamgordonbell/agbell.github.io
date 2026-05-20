#!/usr/bin/env python3
"""Sync Pulumi blog posts authored by Adam → data/pulumi_blog.json.

Reads directly from the local Pulumi docs repo at ~/sandbox/docs/.
No HTTP — the source of truth is on disk because Adam committed the posts.

Filters posts where frontmatter `authors:` list includes "adam-gordon-bell".

Editorial overrides live in data/pulumi_blog_overrides.yaml.

Usage: scripts/sync-pulumi-blog.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

DOCS_REPO = Path("~/sandbox/docs").expanduser()
BLOG_DIR = DOCS_REPO / "content" / "blog"
OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "pulumi_blog.json"
AUTHOR_SLUG = "adam-gordon-bell"
PUBLIC_BASE = "https://www.pulumi.com/blog"


def parse_frontmatter(text: str) -> dict | None:
    """Lightweight YAML frontmatter parser. Handles the fields we need."""
    if not text.startswith("---"):
        return None
    m = re.match(r"---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    fm_text = m.group(1)
    fm: dict = {}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        # key: value
        kv = re.match(r"^(\w[\w_-]*):\s*(.*)$", line)
        if kv:
            key, val = kv.group(1), kv.group(2).strip()
            # Multi-line list (authors: \n  - foo\n  - bar)
            if not val:
                items = []
                j = i + 1
                while j < len(lines) and re.match(r"^\s+-\s+", lines[j]):
                    items.append(re.sub(r"^\s+-\s+", "", lines[j]).strip())
                    j += 1
                if items:
                    fm[key] = items
                    i = j
                    continue
            # Strip surrounding quotes
            if (val.startswith('"') and val.endswith('"')) or (
                val.startswith("'") and val.endswith("'")
            ):
                val = val[1:-1]
            fm[key] = val
        i += 1
    return fm


def normalize_date(val: str) -> str:
    # "2026-05-19T02:00:00-07:00" or "2025-10-06" etc.
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", val)
    return m.group(1) if m else val[:10]


def main() -> int:
    if not BLOG_DIR.exists():
        print(f"Blog dir not found: {BLOG_DIR}", file=sys.stderr)
        return 1

    items = []
    for index_md in BLOG_DIR.glob("*/index.md"):
        slug = index_md.parent.name
        text = index_md.read_text()
        fm = parse_frontmatter(text)
        if not fm:
            continue
        authors = fm.get("authors") or []
        if isinstance(authors, str):
            authors = [authors]
        if AUTHOR_SLUG not in authors:
            continue
        if fm.get("draft") == "true":
            continue

        title = fm.get("title", "").strip()
        date = normalize_date(fm.get("date", ""))
        if not (title and date):
            continue

        items.append({
            "title": title,
            "url": f"{PUBLIC_BASE}/{slug}/",
            "date": date,
            "slug": slug,
            "description": fm.get("meta_desc") or "",
        })

    items.sort(key=lambda x: x["date"], reverse=True)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps({"items": items}, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {len(items)} Pulumi blog posts to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
