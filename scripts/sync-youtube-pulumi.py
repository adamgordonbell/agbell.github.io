#!/usr/bin/env python3
"""Sync PulumiTV videos featuring Adam → data/youtube_pulumi.json.

Strategy: Adam started at Pulumi 2024-11-01, so videos older than that are
not him. We extract only videos newer than that cutoff via yt-dlp's
--dateafter, then keep videos where either:
  - "Adam Gordon Bell" or "adamgordonbell" appears in title or description
  - the video ID is listed in config/youtube-pulumi-picks.txt (manual override)

The picks.txt mechanism lets Adam add videos where he hosts/presents but isn't
named in the description.

Editorial overrides live in data/youtube_pulumi_overrides.yaml.

Usage: scripts/sync-youtube-pulumi.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

CHANNEL_URL = "https://www.youtube.com/@PulumiTV/videos"
ADAM_START = "20241101"  # YYYYMMDD — only videos this date or newer
PICKS_PATH = Path(__file__).resolve().parents[1] / "config" / "youtube-pulumi-picks.txt"
OUT_PATH = Path(__file__).resolve().parents[1] / "data" / "youtube_pulumi.json"


def read_picks() -> set[str]:
    """Return video IDs manually marked as Adam-relevant."""
    if not PICKS_PATH.exists():
        return set()
    out = set()
    for line in PICKS_PATH.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.add(line)
    return out


def mentions_adam(raw: dict) -> bool:
    text = (raw.get("title") or "") + " " + (raw.get("description") or "")
    return ("Adam Gordon Bell" in text) or ("adamgordonbell" in text.lower())


def extract_recent() -> list[dict]:
    """Run yt-dlp full extraction limited to post-Adam-start videos."""
    cmd = [
        "yt-dlp",
        "--no-update",
        "--skip-download",
        "--dump-json",
        "--ignore-errors",
        "--dateafter", ADAM_START,
        CHANNEL_URL,
    ]
    print(f"Extracting PulumiTV videos uploaded on/after {ADAM_START}…", file=sys.stderr)
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
    print(f"  → {len(items)} videos in date range", file=sys.stderr)
    return items


_LINK_LINE_RE = re.compile(r"^[^\n]{1,80}?(?:[➤➜→»►])\s*https?://", re.IGNORECASE)
_BARE_URL_RE = re.compile(r"^\s*https?://\S+\s*$")
_SOCIAL_HEADER_RE = re.compile(r"^\s*(?:follow|subscribe|join|connect|find me|find us|check out|website|patreon|sponsor|chapters?|timestamps?|links?)\b", re.IGNORECASE)


def clean_description(desc: str) -> str:
    body = []
    for ln in desc.splitlines():
        if not ln.strip():
            if body: body.append("")
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
    upload_date = raw.get("upload_date")
    if not (vid and title and upload_date):
        return None
    date = f"{upload_date[0:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
    return {
        "title": title,
        "url": f"https://www.youtube.com/watch?v={vid}",
        "date": date,
        "slug": vid,
        "description": clean_description((raw.get("description") or "").strip()),
        "duration": raw.get("duration_string") or "",
    }


def main() -> int:
    raw_items = extract_recent()
    picks = read_picks()

    items: list[dict] = []
    auto_count = 0
    pick_count = 0
    for raw in raw_items:
        keep = False
        if mentions_adam(raw):
            keep = True
            auto_count += 1
        elif raw.get("id") in picks:
            keep = True
            pick_count += 1
        if not keep:
            continue
        norm = normalize(raw)
        if norm:
            items.append(norm)

    items.sort(key=lambda x: x["date"], reverse=True)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps({"items": items}, indent=2, ensure_ascii=False) + "\n")
    print(
        f"Wrote {len(items)} videos to {OUT_PATH} "
        f"({auto_count} auto-matched, {pick_count} from picks)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
