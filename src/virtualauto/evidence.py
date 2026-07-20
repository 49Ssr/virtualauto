"""Create evidence records from retained repository artifacts.

This module automates hashes and metadata only. It never infers an observation,
claim, or scientific conclusion from an artifact.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path

from .paths import repository_root, resolve_repository_output

EVIDENCE_ID = re.compile(r"^EVD-[A-Z0-9]+(?:-[A-Z0-9]+)+$")
EXPERIMENT_ID = re.compile(r"^EXP-[A-Z0-9]+(?:-[A-Z0-9]+)+$")
ARTIFACT_TYPES = {
    "image",
    "video",
    "exr",
    "blend",
    "mesh-report",
    "node-dump",
    "log",
    "measurement",
    "binary-layout",
    "other",
}
RIGHTS_STATUSES = {"original", "licensed", "reference-only", "unknown"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def record_evidence(
    *,
    artifact: str | Path,
    evidence_id: str,
    experiment_id: str | None,
    artifact_type: str,
    provenance: str,
    rights_status: str,
    output: str | Path | None = None,
    blender_version: str | None = None,
    render_engine: str | None = None,
    scene_revision: str | None = None,
    retention_note: str | None = None,
    overwrite: bool = False,
    root: Path | None = None,
) -> dict[str, object]:
    root = (root or repository_root()).resolve()
    source = Path(artifact)
    if not source.is_absolute():
        source = root / source
    source = source.resolve()
    if not source.is_file():
        raise ValueError(f"Evidence artifact is not a file: {source}")
    try:
        relative_source = source.relative_to(root)
    except ValueError as error:
        raise ValueError(
            "Evidence artifact must remain inside the repository"
        ) from error
    if not relative_source.as_posix().startswith("lab/evidence/"):
        raise ValueError(
            "Evidence artifacts must be retained under lab/evidence; use "
            "register-source for private external assets"
        )
    if relative_source.as_posix().startswith("lab/evidence/records/"):
        raise ValueError("An evidence record cannot record another evidence record")
    if not EVIDENCE_ID.fullmatch(evidence_id):
        raise ValueError("Evidence ID must match EVD-[A-Z0-9]+(?:-[A-Z0-9]+)+")
    if experiment_id is not None and not EXPERIMENT_ID.fullmatch(experiment_id):
        raise ValueError("Experiment ID must match EXP-[A-Z0-9]+(?:-[A-Z0-9]+)+")
    if artifact_type not in ARTIFACT_TYPES:
        raise ValueError(f"Unsupported artifact type: {artifact_type}")
    if rights_status not in RIGHTS_STATUSES:
        raise ValueError(f"Unsupported rights status: {rights_status}")
    if len(provenance.strip()) < 5:
        raise ValueError("Provenance must contain at least five characters")

    destination = resolve_repository_output(
        root,
        output or f"lab/evidence/records/{evidence_id}.json",
    )
    if destination.exists() and not overwrite:
        raise ValueError(
            f"Evidence record already exists: {destination.relative_to(root)}"
        )
    schema = Path(
        os.path.relpath(root / "lab/schemas/evidence.schema.json", destination.parent)
    ).as_posix()
    record: dict[str, object] = {
        "$schema": schema,
        "schema_version": "1.1.0",
        "id": evidence_id,
        "experiment_id": experiment_id,
        "artifact_type": artifact_type,
        "repository_path": relative_source.as_posix(),
        "external_reference": None,
        "sha256": sha256_file(source),
        "byte_size": source.stat().st_size,
        "provenance": provenance,
        "recorded_at": datetime.now(UTC).isoformat(),
        "blender_version": blender_version,
        "render_engine": render_engine,
        "scene_revision": scene_revision,
        "observation_ids": [],
        "rights_status": rights_status,
        "retention_note": retention_note,
    }
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    temporary.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, destination)
    return record
