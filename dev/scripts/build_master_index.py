"""Build a deterministic retrieval index from the canonical automotive master.

The index is a navigation aid, never a replacement or edited derivative of the
canonical master. It contains headings, hierarchy, line ranges, anchors, and a
content-derived stable ID. No source prose is copied into the index.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MASTER = ROOT / "research/automotive_materials/Automotive_Body_RnD_Master.md"
PROVENANCE = ROOT / "research/automotive_materials/master.provenance.json"
OUTPUT = ROOT / "research/indexes/automotive_master.index.json"
GENERATOR_VERSION = "1.1.0"
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
CANONICAL_KEY = re.compile(r"^([A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+)\s+[—-]\s+")
MARKDOWN_DECORATION = re.compile(r"[`*_~]")


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
    clean = MARKDOWN_DECORATION.sub("", ascii_title).lower()
    return re.sub(r"[^a-z0-9]+", "-", clean).strip("-") or "section"


def stable_id(path_titles: list[str], occurrence: int) -> str:
    identity = "\x1f".join(path_titles + [str(occurrence)]).encode("utf-8")
    return f"SEC-{hashlib.sha256(identity).hexdigest()[:16].upper()}"


def main() -> int:
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    payload = MASTER.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != provenance["sha256"]:
        raise SystemExit(
            f"master checksum mismatch: expected {provenance['sha256']}, got {digest}"
        )
    if len(payload) != provenance["byte_size"]:
        raise SystemExit("master byte size does not match provenance")

    text = payload.decode("utf-8")
    lines = text.splitlines()
    if len(lines) != provenance["line_count"]:
        raise SystemExit("master line count does not match provenance")

    sections: list[dict[str, Any]] = []
    stack: list[dict[str, Any]] = []
    identity_counts: dict[str, int] = {}
    retrieval_key_counts: dict[str, int] = {}

    for line_number, line in enumerate(lines, start=1):
        match = HEADING.match(line)
        if not match:
            continue
        level = len(match.group(1))
        title = match.group(2).strip()

        while stack and stack[-1]["level"] >= level:
            stack.pop()
        path_titles = [item["title"] for item in stack] + [title]
        identity_key = "\x1f".join(path_titles)
        occurrence = identity_counts.get(identity_key, 0) + 1
        identity_counts[identity_key] = occurrence
        base_key = slugify(title)
        key_occurrence = retrieval_key_counts.get(base_key, 0)
        retrieval_key_counts[base_key] = key_occurrence + 1
        retrieval_key = (
            base_key if key_occurrence == 0 else f"{base_key}-{key_occurrence}"
        )

        section = {
            "id": stable_id(path_titles, occurrence),
            "level": level,
            "title": title,
            "retrieval_key": retrieval_key,
            "canonical_key": (
                canonical.group(1)
                if (canonical := CANONICAL_KEY.match(title))
                else None
            ),
            "line_start": line_number,
            "line_end": len(lines),
            "parent_id": stack[-1]["id"] if stack else None,
        }
        sections.append(section)
        stack.append(section)

    for index, section in enumerate(sections):
        for candidate in sections[index + 1 :]:
            if candidate["level"] <= section["level"]:
                section["line_end"] = candidate["line_start"] - 1
                break

    document = {
        "$schema": "../../lab/schemas/master-index.schema.json",
        "index_version": "1.1.0",
        "generator_version": GENERATOR_VERSION,
        "canonical_artifact_id": provenance["id"],
        "source_path": provenance["repository_path"],
        "source_sha256": digest,
        "source_byte_size": len(payload),
        "source_line_count": len(lines),
        "section_count": len(sections),
        "sections": sections,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(document, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote {len(sections)} sections to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
