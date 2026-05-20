"""Additive yaml sync helper.

Each sync script targets one of data/{talks,podcasts,writing,videos}.yaml.
On run:
  - Load existing yaml
  - For each scraped item, add only if URL is not already present
  - Sort by date desc, write back with stable header

Hand edits persist. Curated entries (source: curated) are never touched.
"""
from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

import yaml

yaml.add_representer(
    OrderedDict,
    lambda dumper, data: dumper.represent_mapping("tag:yaml.org,2002:map", data.items()),
    Dumper=yaml.SafeDumper,
)

DATA = Path(__file__).resolve().parents[1] / "data"

_HEADER_TMPL = (
    "# {fname} — auto-managed by sync scripts + hand edits.\n"
    "# Sync is ADDITIVE: scripts only add items whose url isn't already present.\n"
    "# Hand-edit titles, descriptions, types, etc. directly — they persist.\n"
    "# Schema: type, role?, title, date, url, slug?, description?, ...\n\n"
)


def load_items(target: str) -> list[dict]:
    p = DATA / target
    if not p.exists():
        return []
    d = yaml.safe_load(p.read_text()) or {}
    return d.get("items", []) or []


def merge_and_save(target: str, new_items: list[dict]) -> tuple[int, int]:
    """Add new_items into target yaml, skipping existing URLs.

    Returns (added, skipped).
    """
    existing = load_items(target)
    existing_urls = {i.get("url") for i in existing if i.get("url")}
    added = 0
    for raw in new_items:
        url = raw.get("url")
        if url and url in existing_urls:
            continue
        existing.append(raw)
        if url:
            existing_urls.add(url)
        added += 1
    existing.sort(key=lambda x: str(x.get("date") or ""), reverse=True)
    body = yaml.safe_dump(
        {"items": existing}, sort_keys=False, allow_unicode=True, width=200
    )
    (DATA / target).write_text(_HEADER_TMPL.format(fname=target) + body)
    return added, len(new_items) - added


def make_item(
    type_: str,
    title: str,
    url: str,
    date: str,
    *,
    role: str | None = None,
    slug: str | None = None,
    description: str | None = None,
    duration: str | None = None,
    episode_number: int | None = None,
    source: str,
    extra: dict | None = None,
) -> OrderedDict:
    """Build an item with stable key ordering."""
    item: OrderedDict = OrderedDict()
    item["type"] = type_
    if role:
        item["role"] = role
    item["title"] = title
    item["date"] = date
    item["url"] = url
    if slug:
        item["slug"] = slug
    if description:
        item["description"] = description
    if duration:
        item["duration"] = duration
    if episode_number is not None:
        item["episode_number"] = episode_number
    if extra:
        for k, v in extra.items():
            if v is not None and v != "":
                item[k] = v
    item["source"] = source
    return item
