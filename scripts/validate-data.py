#!/usr/bin/env python3
"""
validate-data.py — Validates YAML data files for agbell.github.io

Checks:
1. URL liveness (HEAD requests, follow redirects)
2. YouTube title + description match (via yt-dlp)
3. Stub/TODO detection
4. Missing key fields

Run from repo root:
    python3 scripts/validate-data.py
    python3 scripts/validate-data.py --youtube-only
"""

import sys
import os
import re
import time
import shutil
import subprocess
import urllib.request
import urllib.error
import urllib.parse
import html
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------------------------------------------------------------
# Minimal YAML parser — handles the subset used in these files
# ---------------------------------------------------------------------------
try:
    import yaml
    def load_yaml(text):
        return yaml.safe_load(text)
    YAML_MODULE = "PyYAML"
except ImportError:
    YAML_MODULE = None

if YAML_MODULE is None:
    print("ERROR: PyYAML not available. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
DATA_DIR  = REPO_ROOT / "data"
SCRATCH   = REPO_ROOT / "scratch"
REPORT    = SCRATCH / "validation-report.md"

YAML_FILES = ["talks.yaml", "podcasts.yaml", "writing.yaml", "videos.yaml"]

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
TIMEOUT = 10      # seconds per request
MAX_WORKERS = 8   # concurrent HTTP workers

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def log(msg):
    print(msg, flush=True)


def is_youtube(url):
    return bool(url) and ("youtube.com/watch" in url or "youtu.be/" in url)


def extract_video_id(url):
    """Extract YouTube video ID."""
    m = re.search(r"[?&]v=([A-Za-z0-9_-]{11})", url)
    if m:
        return m.group(1)
    m = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", url)
    if m:
        return m.group(1)
    return None


def token_overlap(a, b):
    """Fraction of tokens in the shorter string that appear in the longer string."""
    stop = {"the", "a", "an", "and", "or", "of", "in", "on", "at", "to",
            "for", "with", "is", "are", "was", "were", "be", "by", "as"}

    def tokens(s):
        words = re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()
        return set(w for w in words if w not in stop and len(w) > 1)

    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    shorter = ta if len(ta) <= len(tb) else tb
    overlap = ta & tb
    return len(overlap) / len(shorter)


def check_url(url):
    """
    Do a HEAD request; fall back to GET if HEAD returns 405.
    Returns (status_code, final_url, error_str).
    error_str is None on success.
    """
    if not url or url.startswith("mailto:"):
        return (None, url, "skipped")

    req = urllib.request.Request(url, method="HEAD")
    req.add_header("User-Agent", USER_AGENT)
    req.add_header("Accept", "*/*")

    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return (resp.status, resp.url, None)
    except urllib.error.HTTPError as e:
        if e.code == 405:
            # Server doesn't allow HEAD — try GET
            req2 = urllib.request.Request(url, method="GET")
            req2.add_header("User-Agent", USER_AGENT)
            req2.add_header("Accept", "*/*")
            try:
                with urllib.request.urlopen(req2, timeout=TIMEOUT) as resp2:
                    return (resp2.status, resp2.url, None)
            except urllib.error.HTTPError as e2:
                return (e2.code, url, f"HTTP {e2.code}")
            except Exception as e2:
                return (None, url, str(e2))
        return (e.code, url, f"HTTP {e.code}")
    except urllib.error.URLError as e:
        return (None, url, f"URLError: {e.reason}")
    except Exception as e:
        return (None, url, str(e))


def fetch_youtube_info(url):
    """
    Use yt-dlp to fetch title and description for a YouTube URL.
    Returns (title_str, description_str, error_str).
    error_str is None on success.
    """
    ytdlp = shutil.which("yt-dlp")
    if not ytdlp:
        return (None, None, "yt-dlp not found — install with: pip3 install yt-dlp")

    try:
        result = subprocess.run(
            [ytdlp, "--no-download", "--print", "%(title)s|||%(description)s", url],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            err = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "yt-dlp error"
            return (None, None, err)
        output = result.stdout.strip()
        if "|||" in output:
            title, description = output.split("|||", 1)
        else:
            title = output
            description = ""
        return (title.strip(), description.strip(), None)
    except subprocess.TimeoutExpired:
        return (None, None, "yt-dlp timed out after 30s")
    except Exception as e:
        return (None, None, str(e))

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

def load_file(fname):
    path = DATA_DIR / fname
    text = path.read_text(encoding="utf-8")
    data = load_yaml(text)
    items = data.get("items", []) if data else []
    # Attach source file name
    for item in items:
        item["_source_file"] = fname
    return items


def collect_all_items():
    all_items = []
    for fname in YAML_FILES:
        items = load_file(fname)
        log(f"  Loaded {len(items):3d} items from {fname}")
        all_items.extend(items)
    return all_items

# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def collect_urls(items):
    """
    Returns list of (item, field_name, url).
    Deduplicates URLs but keeps track of all items referencing them.
    """
    seen = {}  # url -> [(item, field)]
    for item in items:
        for field in ("url", "video_url"):
            url = item.get(field)
            if url and not url.startswith("mailto:"):
                if url not in seen:
                    seen[url] = []
                seen[url].append((item, field))
    return seen  # url -> [(item, field), ...]


def run_url_checks(url_map):
    """Returns dict: url -> (status, final_url, error)"""
    results = {}
    urls = list(url_map.keys())
    log(f"\n[URL check] Checking {len(urls)} unique URLs with {MAX_WORKERS} workers...")

    def worker(url):
        result = check_url(url)
        return url, result

    done = 0
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(worker, u): u for u in urls}
        for fut in as_completed(futures):
            url, result = fut.result()
            results[url] = result
            done += 1
            status, final_url, err = result
            icon = "✓" if err is None and status and status < 400 else "✗"
            if done % 20 == 0 or icon == "✗":
                log(f"  [{done}/{len(urls)}] {icon} {status or 'ERR'} {url[:80]}")

    log(f"  Done — {len(urls)} URLs checked.")
    return results


def run_youtube_checks(items):
    """
    Returns list of (item, yt_title, yt_description, error).
    Uses yt-dlp for reliable title + description extraction.
    Falls back gracefully if yt-dlp is unavailable.
    """
    yt_items = [i for i in items if is_youtube(i.get("video_url", ""))]
    log(f"\n[YouTube] Checking {len(yt_items)} YouTube video_url items via yt-dlp...")

    # Check yt-dlp availability once
    if not shutil.which("yt-dlp"):
        log("  WARNING: yt-dlp not found. Skipping YouTube checks.")
        log("  Install with: pip3 install yt-dlp")
        return [(item, None, None, "yt-dlp not available") for item in yt_items]

    results = []

    def worker(item):
        url = item["video_url"]
        title, description, err = fetch_youtube_info(url)
        return item, title, description, err

    done = 0
    with ThreadPoolExecutor(max_workers=4) as ex:  # keep concurrency lower for yt-dlp
        futures = {ex.submit(worker, i): i for i in yt_items}
        for fut in as_completed(futures):
            item, title, description, err = fut.result()
            results.append((item, title, description, err))
            done += 1
            icon = "✗" if err else "✓"
            if done % 5 == 0 or err:
                log(f"  [{done}/{len(yt_items)}] {icon} {item.get('title', '')[:60]}")

    log(f"  Done — {len(yt_items)} YouTube items checked.")
    return results


def check_stubs(items):
    flags = []
    for item in items:
        desc = item.get("description") or ""
        source = item.get("source") or ""
        if "TODO" in desc.upper():
            flags.append((item, "description contains TODO"))
        if source == "roam-stub":
            flags.append((item, "source == 'roam-stub'"))
    return flags


def check_missing_fields(items):
    flags = []
    for item in items:
        desc = item.get("description") or ""
        video_url = item.get("video_url") or ""
        if video_url and not desc:
            flags.append((item, "has video_url but no description"))
        if desc and len(desc.strip()) < 20:
            flags.append((item, f"description suspiciously short ({len(desc.strip())} chars): {desc.strip()!r}"))
    return flags

# ---------------------------------------------------------------------------
# Report builder
# ---------------------------------------------------------------------------

def item_label(item):
    title = item.get("title", "(no title)")
    src = item.get("_source_file", "?")
    date = item.get("date", "")
    return f"**{title}** [{src}, {date}]"


def build_report(
    items,
    url_results,    # url -> (status, final_url, error)
    url_map,        # url -> [(item, field), ...]
    yt_results,     # [(item, yt_title, yt_description, error)]
    stub_flags,
    field_flags,
):
    lines = []
    lines.append("# Data Validation Report")
    lines.append(f"\nGenerated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"\nFiles checked: {', '.join(YAML_FILES)}")
    lines.append(f"\nTotal items: {len(items)}")
    lines.append(f"\nTotal unique URLs checked: {len(url_results)}")
    lines.append("")

    # --- 1. URL Liveness ---
    lines.append("## 1. URL Liveness\n")
    dead_urls = {
        url: (status, final_url, err)
        for url, (status, final_url, err) in url_results.items()
        if err is not None or (status and status >= 400)
    }

    if not dead_urls:
        lines.append("All URLs returned 2xx/3xx. ✓\n")
    else:
        lines.append(f"**{len(dead_urls)} problematic URL(s) found:**\n")
        for url, (status, final_url, err) in sorted(dead_urls.items()):
            lines.append(f"- `{url}`")
            lines.append(f"  - Status: `{status or 'ERROR'}` — {err or ''}")
            for item, field in url_map.get(url, []):
                lines.append(f"  - Item ({field}): {item_label(item)}")
        lines.append("")

    # Redirects (final_url differs significantly)
    redirect_notes = []
    for url, (status, final_url, err) in url_results.items():
        if err is None and final_url and final_url != url:
            # Only flag if domain changed or path changed significantly
            orig_parsed = urllib.parse.urlparse(url)
            final_parsed = urllib.parse.urlparse(final_url)
            if orig_parsed.netloc != final_parsed.netloc:
                redirect_notes.append((url, final_url))
    if redirect_notes:
        lines.append(f"### Redirects (domain changed, {len(redirect_notes)} URLs)\n")
        for orig, final in redirect_notes[:30]:
            lines.append(f"- `{orig}`")
            lines.append(f"  → `{final}`")
            for item, field in url_map.get(orig, []):
                lines.append(f"  - Item ({field}): {item_label(item)}")
        lines.append("")

    # --- 2. YouTube Validation (title + description via yt-dlp) ---
    lines.append("## 2. YouTube Validation\n")
    lines.append("_Fetched via `yt-dlp --no-download --print \"%(title)s|||%(description)s\"`_\n")

    title_mismatches = []
    desc_mismatches = []
    yt_errors = []

    for item, yt_title, yt_desc, err in yt_results:
        if err:
            yt_errors.append((item, err))
            continue

        yaml_title = item.get("title", "")
        yaml_desc  = item.get("description", "")

        # Title check: flag if < 60% overlap
        title_overlap = token_overlap(yaml_title, yt_title or "")
        if title_overlap < 0.6:
            title_mismatches.append((item, yaml_title, yt_title, title_overlap))

        # Description check: flag if < 30% of YAML description words found in YT description
        if yaml_desc and yt_desc is not None:
            desc_overlap = token_overlap(yaml_desc, yt_desc)
            if desc_overlap < 0.3:
                desc_mismatches.append((item, yaml_desc, yt_desc, desc_overlap))

    # Title results
    lines.append("### Title Match (threshold: 60% word overlap)\n")
    if title_mismatches:
        lines.append(f"**{len(title_mismatches)} title mismatch(es):**\n")
        for item, yaml_title, yt_title, overlap in sorted(title_mismatches, key=lambda x: x[3]):
            lines.append(f"- {item_label(item)}")
            lines.append(f"  - YAML title : `{yaml_title}`")
            lines.append(f"  - YouTube    : `{yt_title}`")
            lines.append(f"  - Overlap    : {overlap:.0%}")
            lines.append(f"  - URL: {item.get('video_url', '')}")
        lines.append("")
    else:
        lines.append("All YouTube titles match (≥ 60% word overlap). ✓\n")

    # Description results
    lines.append("### Description Match (threshold: 30% of YAML words in YouTube description)\n")
    if desc_mismatches:
        lines.append(f"**{len(desc_mismatches)} description mismatch(es):**\n")
        for item, yaml_desc, yt_desc, overlap in sorted(desc_mismatches, key=lambda x: x[3]):
            yt_preview = (yt_desc or "")[:200].replace("\n", " ")
            lines.append(f"- {item_label(item)}")
            lines.append(f"  - YAML desc  : `{yaml_desc}`")
            lines.append(f"  - YT desc    : `{yt_preview}...`")
            lines.append(f"  - Overlap    : {overlap:.0%}")
            lines.append(f"  - URL: {item.get('video_url', '')}")
        lines.append("")
    else:
        lines.append("All YouTube descriptions have sufficient overlap (≥ 30%). ✓\n")

    if yt_errors:
        lines.append(f"### Fetch Errors ({len(yt_errors)})\n")
        for item, err in yt_errors:
            lines.append(f"- {item_label(item)}: {err}")
    lines.append("")

    # --- 3. Stubs / TODOs ---
    lines.append("## 3. Stub / TODO Detection\n")
    if not stub_flags:
        lines.append("No TODO descriptions or roam-stub sources found. ✓\n")
    else:
        lines.append(f"**{len(stub_flags)} stub/TODO item(s):**\n")
        for item, reason in stub_flags:
            lines.append(f"- {item_label(item)}: {reason}")
        lines.append("")

    # --- 4. Missing Key Fields ---
    lines.append("## 4. Missing / Short Key Fields\n")
    if not field_flags:
        lines.append("No missing or suspiciously short fields found. ✓\n")
    else:
        lines.append(f"**{len(field_flags)} item(s) with field issues:**\n")
        for item, reason in field_flags:
            lines.append(f"- {item_label(item)}: {reason}")
        lines.append("")

    # --- Summary ---
    lines.append("## Summary\n")
    total_issues = (len(dead_urls) + len(title_mismatches) + len(desc_mismatches)
                    + len(stub_flags) + len(field_flags) + len(yt_errors))
    lines.append(f"| Check | Issues |")
    lines.append(f"|-------|--------|")
    lines.append(f"| URL liveness | {len(dead_urls)} dead, {len(redirect_notes)} cross-domain redirects |")
    lines.append(f"| YouTube title match | {len(title_mismatches)} mismatches, {len(yt_errors)} fetch errors |")
    lines.append(f"| YouTube description match | {len(desc_mismatches)} mismatches |")
    lines.append(f"| Stub / TODO | {len(stub_flags)} |")
    lines.append(f"| Missing / short fields | {len(field_flags)} |")
    lines.append(f"| **Total issues** | **{total_issues}** |")
    lines.append("")

    return "\n".join(lines)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    log("=== validate-data.py ===")
    log(f"Repo root : {REPO_ROOT}")
    log(f"Data dir  : {DATA_DIR}")
    log(f"Report    : {REPORT}")
    log(f"YAML      : {YAML_MODULE}")
    log("")

    # Load
    log("[Load] Reading YAML files...")
    items = collect_all_items()
    log(f"  Total items: {len(items)}")

    # Collect URLs
    url_map = collect_urls(items)
    log(f"  Unique URLs to check: {len(url_map)}")

    # URL liveness
    url_results = run_url_checks(url_map)

    # YouTube titles
    yt_results = run_youtube_checks(items)

    # Stubs
    log("\n[Stubs] Checking for TODO / roam-stub...")
    stub_flags = check_stubs(items)
    log(f"  Found {len(stub_flags)} stub/TODO flags.")

    # Missing fields
    log("\n[Fields] Checking for missing/short fields...")
    field_flags = check_missing_fields(items)
    log(f"  Found {len(field_flags)} field issues.")

    # Build report
    log("\n[Report] Writing markdown report...")
    SCRATCH.mkdir(parents=True, exist_ok=True)
    report_text = build_report(
        items, url_results, url_map, yt_results, stub_flags, field_flags
    )
    REPORT.write_text(report_text, encoding="utf-8")
    log(f"  Written: {REPORT}")

    # Print summary to stdout
    log("\n=== SUMMARY ===")
    dead = sum(1 for url, (s, fu, e) in url_results.items() if e is not None or (s and s >= 400))
    yt_title_mismatch = sum(
        1 for item, yt_title, yt_desc, err in yt_results
        if not err and token_overlap(item.get("title", ""), yt_title or "") < 0.6
    )
    yt_desc_mismatch = sum(
        1 for item, yt_title, yt_desc, err in yt_results
        if not err and item.get("description") and token_overlap(item.get("description", ""), yt_desc or "") < 0.3
    )
    log(f"  Dead/erroring URLs       : {dead}")
    log(f"  YouTube title mismatches : {yt_title_mismatch}")
    log(f"  YouTube desc mismatches  : {yt_desc_mismatch}")
    log(f"  Stub/TODO items          : {len(stub_flags)}")
    log(f"  Field issues             : {len(field_flags)}")
    log(f"\nFull report: {REPORT}")


def youtube_only():
    """Run just the YouTube validation section and update the report."""
    log("=== validate-data.py --youtube-only ===")
    log(f"Repo root : {REPO_ROOT}")

    log("\n[Load] Reading YAML files...")
    items = collect_all_items()
    log(f"  Total items: {len(items)}")

    yt_results = run_youtube_checks(items)

    # Build just the YouTube section
    lines = []
    lines.append("## YouTube Validation\n")
    lines.append("_Fetched via `yt-dlp --no-download --print \"%(title)s|||%(description)s\"`_\n")
    lines.append(f"_Run: {time.strftime('%Y-%m-%d %H:%M:%S')}_\n")

    title_mismatches = []
    desc_mismatches = []
    yt_errors = []

    for item, yt_title, yt_desc, err in yt_results:
        if err:
            yt_errors.append((item, err))
            continue
        yaml_title = item.get("title", "")
        yaml_desc  = item.get("description", "")

        title_overlap = token_overlap(yaml_title, yt_title or "")
        if title_overlap < 0.6:
            title_mismatches.append((item, yaml_title, yt_title, title_overlap))

        if yaml_desc and yt_desc is not None:
            desc_overlap = token_overlap(yaml_desc, yt_desc)
            if desc_overlap < 0.3:
                desc_mismatches.append((item, yaml_desc, yt_desc, desc_overlap))

    lines.append("### Title Match (threshold: 60% word overlap)\n")
    if title_mismatches:
        lines.append(f"**{len(title_mismatches)} title mismatch(es):**\n")
        for item, yaml_title, yt_title, overlap in sorted(title_mismatches, key=lambda x: x[3]):
            lines.append(f"- {item_label(item)}")
            lines.append(f"  - YAML title : `{yaml_title}`")
            lines.append(f"  - YouTube    : `{yt_title}`")
            lines.append(f"  - Overlap    : {overlap:.0%}")
            lines.append(f"  - URL: {item.get('video_url', '')}")
        lines.append("")
    else:
        lines.append("All YouTube titles match (≥ 60% word overlap). ✓\n")

    lines.append("### Description Match (threshold: 30% of YAML words in YouTube description)\n")
    if desc_mismatches:
        lines.append(f"**{len(desc_mismatches)} description mismatch(es):**\n")
        for item, yaml_desc, yt_desc, overlap in sorted(desc_mismatches, key=lambda x: x[3]):
            yt_preview = (yt_desc or "")[:200].replace("\n", " ")
            lines.append(f"- {item_label(item)}")
            lines.append(f"  - YAML desc  : `{yaml_desc}`")
            lines.append(f"  - YT desc    : `{yt_preview}...`")
            lines.append(f"  - Overlap    : {overlap:.0%}")
            lines.append(f"  - URL: {item.get('video_url', '')}")
        lines.append("")
    else:
        lines.append("All YouTube descriptions have sufficient overlap (≥ 30%). ✓\n")

    if yt_errors:
        lines.append(f"### Fetch Errors ({len(yt_errors)})\n")
        for item, err in yt_errors:
            lines.append(f"- {item_label(item)}: {err}")

    yt_section = "\n".join(lines)
    log("\n--- YouTube Validation Results ---")
    log(yt_section)

    # Update or append the YouTube Validation section in the report
    SCRATCH.mkdir(parents=True, exist_ok=True)
    if REPORT.exists():
        existing = REPORT.read_text(encoding="utf-8")
        # Replace existing ## YouTube Validation section if present
        pattern = r"(## YouTube Validation\n.*?)(?=\n## |\Z)"
        if re.search(pattern, existing, re.DOTALL):
            updated = re.sub(pattern, yt_section, existing, flags=re.DOTALL)
        else:
            updated = existing.rstrip("\n") + "\n\n" + yt_section
        REPORT.write_text(updated, encoding="utf-8")
    else:
        REPORT.write_text(yt_section, encoding="utf-8")

    log(f"\nReport updated: {REPORT}")
    log(f"\n=== YOUTUBE SUMMARY ===")
    log(f"  Items checked            : {len(yt_results)}")
    log(f"  Title mismatches (< 60%) : {len(title_mismatches)}")
    log(f"  Desc mismatches  (< 30%) : {len(desc_mismatches)}")
    log(f"  Fetch errors             : {len(yt_errors)}")


if __name__ == "__main__":
    if "--youtube-only" in sys.argv:
        youtube_only()
    else:
        main()
