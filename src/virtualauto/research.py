"""Deterministic retrieval from the append-only automotive master."""

from __future__ import annotations

import json
from pathlib import Path

from .paths import repository_root

PREFIX_PRIORITY = ("CP12-", "ABR5-", "ABR4-", "ABR3-", "ABR2-", "ABR-")


def section_priority(section: dict[str, object]) -> tuple[int, int]:
    canonical_key = section["canonical_key"]
    if canonical_key is None:
        return len(PREFIX_PRIORITY) + 1, section["line_start"]
    for index, prefix in enumerate(PREFIX_PRIORITY):
        if canonical_key.startswith(prefix):
            return index, section["line_start"]
    return len(PREFIX_PRIORITY), section["line_start"]


def load_research(root: Path | None = None) -> tuple[dict[str, object], list[str]]:
    root = root or repository_root()
    index = json.loads(
        (root / "research/indexes/automotive_master.index.json").read_text(
            encoding="utf-8"
        )
    )
    master = (
        root / "research/automotive_materials/Automotive_Body_RnD_Master.md"
    ).read_text(encoding="utf-8").splitlines()
    if index["source_line_count"] != len(master):
        raise ValueError("Research index and canonical master line counts differ")
    return index, master


def get_section(identifier: str, root: Path | None = None) -> dict[str, object]:
    index, master = load_research(root)
    matches = [
        section
        for section in index["sections"]
        if identifier
        in {
            section["id"],
            section["retrieval_key"],
            section["canonical_key"],
        }
    ]
    if not matches:
        raise ValueError(f"No canonical research section matches: {identifier}")
    if len(matches) != 1:
        raise ValueError(f"Research identifier is ambiguous: {identifier}")
    section = matches[0]
    start = section["line_start"]
    end = section["line_end"]
    return {
        "source_path": index["source_path"],
        "source_sha256": index["source_sha256"],
        "section": section,
        "content": "\n".join(master[start - 1 : end]),
    }


def find_sections(
    query: str,
    *,
    prefix: str | None = None,
    include_untagged: bool = False,
    limit: int = 20,
    root: Path | None = None,
) -> list[dict[str, object]]:
    index, _ = load_research(root)
    needle = query.casefold().strip()
    if not needle:
        raise ValueError("Research query cannot be empty")
    if not 1 <= limit <= 100:
        raise ValueError("Research result limit must be between 1 and 100")
    candidates: list[dict[str, object]] = []
    for section in index["sections"]:
        canonical_key = section["canonical_key"]
        if not include_untagged and canonical_key is None:
            continue
        if prefix and (canonical_key is None or not canonical_key.startswith(prefix)):
            continue
        if needle not in section["title"].casefold():
            continue
        candidates.append(section)
    candidates.sort(key=section_priority)
    return candidates[:limit]
