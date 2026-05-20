#!/usr/bin/env python3
"""Sync a YouTube channel into data/<output>.json via yt-dlp.

Strategy: yt-dlp full extraction (slow ~5s/video but gives upload_date and
description). For channels with hundreds of videos where only a few are
Adam-relevant, pass --ids-file with a list of video IDs to extract instead.

Editorial overrides live in data/<output>_overrides.yaml (keyed by video ID).

Usage:
  scripts/sync-youtube.py --channel @EarthlyTech --out data/youtube_earthly.json
  scripts/sync-youtube.py --ids-file picks.txt --out data/youtube_pulumi.json

picks.txt has one YouTube video ID per line (lines starting with # are
comments).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def yt_dlp_json(target: str) -> list[dict]:
    """Run yt-dlp full extraction, yield one JSON dict per video."""
    cmd = [
        "yt-dlp",
        "--no-update",
        "--skip-download",
        "--dump-json",
        "--ignore-errors",
        target,
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    items = []
    assert proc.stdout is not None
    for line in proc.stdout:
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            items.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    proc.wait()
    return items


_LINK_LINE_RE = re.compile(
    r"^[^\n]{1,80}?(?:[➤➜→»►])\s*https?://", re.IGNORECASE
)
_BARE_URL_RE = re.compile(r"^\s*https?://\S+\s*$")
_SOCIAL_HEADER_RE = re.compile(
    r"^\s*(?:follow|subscribe|join|connect|find me|find us|check out|website|patreon|sponsor|chapters?|timestamps?|links?)\b",
    re.IGNORECASE,
)


def clean_description(desc: str) -> str:
    """Drop link-list and chapter scaffolding, return the first body paragraph."""
    lines = [ln.rstrip() for ln in desc.splitlines()]
    body: list[str] = []
    for ln in lines:
        if not ln.strip():
            if body:
                body.append("")
            continue
        if _LINK_LINE_RE.match(ln) or _BARE_URL_RE.match(ln) or _SOCIAL_HEADER_RE.match(ln):
            continue
        body.append(ln)
    text = "\n".join(body).strip()
    first_para = text.split("\n\n", 1)[0].replace("\n", " ").strip()
    if len(first_para) > 280:
        first_para = first_para[:280].rsplit(" ", 1)[0] + "…"
    return first_para


def normalize(raw: dict) -> dict | None:
    vid = raw.get("id")
    title = raw.get("title")
    upload_date = raw.get("upload_date")  # "20231115"
    if not (vid and title and upload_date):
        return None
    date = f"{upload_date[0:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
    desc = (raw.get("description") or "").strip()
    return {
        "title": title,
        "url": f"https://www.youtube.com/watch?v={vid}",
        "date": date,
        "slug": vid,
        "description": clean_description(desc),
        "duration": raw.get("duration_string") or "",
    }


TARGET = "videos.yaml"
TYPE = "video"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_yaml_sync import make_item, merge_and_save  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--channel", help="YouTube channel handle, e.g. @EarthlyTech")
    ap.add_argument("--ids-file", help="File with one YouTube video ID per line")
    ap.add_argument("--source", required=True, help="Source ID, e.g. youtube-earthly")
    args = ap.parse_args()

    if not args.channel and not args.ids_file:
        ap.error("must provide --channel or --ids-file")

    targets: list[str] = []
    if args.channel:
        targets.append(f"https://www.youtube.com/{args.channel}/videos")
    if args.ids_file:
        for line in Path(args.ids_file).read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                targets.append(f"https://www.youtube.com/watch?v={line}")

    print(f"Extracting from {len(targets)} target(s)…", file=sys.stderr)
    all_items: list[dict] = []
    for t in targets:
        all_items.extend(yt_dlp_json(t))

    items = []
    seen = set()
    for raw in all_items:
        norm = normalize(raw)
        if norm and norm["slug"] not in seen:
            seen.add(norm["slug"])
            items.append(norm)

    new = [
        make_item(
            type_=TYPE, source=args.source,
            title=it["title"], url=it["url"], date=it["date"],
            slug=it.get("slug"),
            description=it.get("description"),
            duration=it.get("duration"),
        )
        for it in items
    ]
    added, skipped = merge_and_save(TARGET, new)
    print(f"  → {added} new, {skipped} already in {TARGET}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
