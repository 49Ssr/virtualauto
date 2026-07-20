"""Register immutable private source assets without copying or exposing them."""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path

from .paths import repository_root, resolve_repository_output

ASSET_ID = re.compile(r"^AST-[A-Z0-9]+(?:-[A-Z0-9]+)+$")
SOURCE_KINDS = {
    "original",
    "game-package",
    "extracted-resource",
    "third-party-export",
    "scan",
    "photograph",
    "measurement",
    "document",
    "other",
}
RIGHTS_STATUSES = {
    "original",
    "licensed",
    "lawfully-accessed-private",
    "reference-only",
    "unknown",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def atomic_json_write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, path)


def register_source_asset(
    *,
    input_path: str | Path,
    output_path: str | Path,
    asset_id: str,
    title: str,
    source_kind: str,
    format_name: str,
    provenance: str,
    rights_status: str,
    storage_reference: str,
    notes: str | None = None,
    overwrite: bool = False,
    root: Path | None = None,
) -> dict[str, object]:
    root = root or repository_root()
    source = Path(input_path).expanduser().resolve()
    if not source.is_file():
        raise ValueError(f"Private source asset is not a file: {source}")
    if not ASSET_ID.fullmatch(asset_id):
        raise ValueError("Asset ID must match AST-[A-Z0-9]+(?:-[A-Z0-9]+)+")
    if source_kind not in SOURCE_KINDS:
        raise ValueError(f"Unsupported source kind: {source_kind}")
    if rights_status not in RIGHTS_STATUSES:
        raise ValueError(f"Unsupported rights status: {rights_status}")
    if len(provenance.strip()) < 10:
        raise ValueError("Provenance must contain at least ten characters")
    if not storage_reference or any(
        separator in storage_reference for separator in ("/", "\\")
    ):
        raise ValueError(
            "Storage reference must be an opaque label, not a filesystem path"
        )

    output = resolve_repository_output(root, output_path)
    if output.exists() and not overwrite:
        raise ValueError(f"Asset record already exists: {output.relative_to(root)}")

    schema = Path(
        os.path.relpath(root / "lab/schemas/source-asset.schema.json", output.parent)
    )
    record: dict[str, object] = {
        "$schema": schema.as_posix(),
        "schema_version": "1.0.0",
        "id": asset_id,
        "title": title,
        "source_kind": source_kind,
        "format": format_name,
        "provenance": provenance,
        "rights_status": rights_status,
        "custody_status": "external-private-storage",
        "storage_reference": storage_reference,
        "sha256": sha256_file(source),
        "byte_size": source.stat().st_size,
        "recorded_at": datetime.now(UTC).isoformat(),
        "derived_from": [],
        "immutable": True,
        "notes": notes,
    }
    atomic_json_write(output, record)
    return record
