"""Validate deterministic invariants of the VirtualAuto repository.

This validator is intentionally conservative. It checks repository structure,
JSON Schema contracts, local references, cross-record IDs, evidence locations,
and prohibited source-asset leakage. It does not claim that research conclusions
or Blender implementations are scientifically correct.
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    import jsonschema
except ModuleNotFoundError:  # CI installs it; local bootstrap may not have it.
    jsonschema = None

try:
    import yaml
except ModuleNotFoundError:  # CI installs it; local bootstrap may not have it.
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
REQUIRED_PATHS = (
    "README.md",
    ".gitignore",
    "CONTRIBUTING.md",
    "docs/PROJECT_DOCTRINE.md",
    "docs/REPOSITORY_ARCHITECTURE.md",
    "docs/AI_RETRIEVAL_PROTOCOL.md",
    "docs/RIGHTS_AND_ASSET_BOUNDARIES.md",
    "knowledge/README.md",
    "external/README.md",
    "external/tools.lock.json",
    "experiments/TEMPLATE.md",
    "schemas/experiment.schema.json",
    "schemas/evidence.schema.json",
    "schemas/observation.schema.json",
    "schemas/source-asset.schema.json",
    "schemas/transformation.schema.json",
    "schemas/unknown-field.schema.json",
    "schemas/claim.schema.json",
    "schemas/node-contract.schema.json",
    "examples/README.md",
)
FORBIDDEN_DIRECTORIES = {".vs", "raw_assets", "extracted", "converted_assets", "package_dumps"}
FORBIDDEN_SUFFIXES = {
    ".pkg",
    ".dat",
    ".idx",
    ".ndx",
    ".rpk",
    ".dds",
    ".fbx",
    ".obj",
    ".gltf",
    ".glb",
    ".exr",
    ".hdr",
    ".blend",
    ".blend1",
}
ID_KIND_BY_PREFIX = {
    "EXP-": "experiment",
    "EVD-": "evidence",
    "OBS-": "observation",
    "AST-": "asset",
    "TRN-": "transformation",
    "UNK-": "unknown",
    "CLM-": "claim",
    "NODE-": "node",
}


def fail(message: str) -> None:
    raise ValueError(message)


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        fail(f"Expected JSON object: {path.relative_to(ROOT)}")
    return data


def validate_required_structure() -> None:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).is_file()]
    if missing:
        fail(f"Missing required paths: {', '.join(missing)}")


def validate_no_prohibited_artifacts() -> None:
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in FORBIDDEN_DIRECTORIES for part in relative.parts):
            fail(f"Prohibited repository directory: {relative}")
        if path.is_file() and path.suffix.lower() in FORBIDDEN_SUFFIXES:
            fail(f"Prohibited source or large binary artifact: {relative}")


def validate_json_syntax() -> None:
    for path in ROOT.rglob("*.json"):
        read_json(path)


def validate_schema_documents() -> dict[Path, dict[str, Any]]:
    if jsonschema is None:
        if os.environ.get("VIRTUALAUTO_STRICT_VALIDATION") == "1":
            fail("jsonschema is required for strict validation")
        print("warning: jsonschema unavailable; schema validation skipped")
        return {}

    schemas: dict[Path, dict[str, Any]] = {}
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        schema = read_json(path)
        jsonschema.Draft202012Validator.check_schema(schema)
        schemas[path.resolve()] = schema
    return schemas


def resolve_local_schema(instance_path: Path, schema_ref: str) -> Path:
    if re.match(r"^[a-z][a-z0-9+.-]*:", schema_ref, re.I):
        fail(
            f"Repository manifest uses a non-local schema reference: "
            f"{instance_path.relative_to(ROOT)} -> {schema_ref}"
        )
    resolved = (instance_path.parent / schema_ref).resolve()
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError:
        fail(f"Schema reference escapes repository: {instance_path.relative_to(ROOT)}")
    if not resolved.is_file():
        fail(f"Missing schema for {instance_path.relative_to(ROOT)}: {schema_ref}")
    return resolved


def validate_manifest_instances(
    schemas: dict[Path, dict[str, Any]],
) -> list[tuple[Path, dict[str, Any]]]:
    manifests: list[tuple[Path, dict[str, Any]]] = []
    if jsonschema is None:
        return manifests

    for path in sorted(ROOT.rglob("*.json")):
        if SCHEMA_DIR in path.parents:
            continue
        instance = read_json(path)
        schema_ref = instance.get("$schema")
        if schema_ref is None:
            continue
        if not isinstance(schema_ref, str):
            fail(f"$schema must be a string: {path.relative_to(ROOT)}")
        schema_path = resolve_local_schema(path, schema_ref)
        schema = schemas.get(schema_path)
        if schema is None:
            schema = read_json(schema_path)
            jsonschema.Draft202012Validator.check_schema(schema)
        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )
        errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.path))
        if errors:
            detail = "; ".join(
                f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
                for error in errors[:5]
            )
            fail(f"Schema validation failed for {path.relative_to(ROOT)}: {detail}")
        manifests.append((path, instance))
    return manifests


def record_kind(record_id: str) -> str | None:
    for prefix, kind in ID_KIND_BY_PREFIX.items():
        if record_id.startswith(prefix):
            return kind
    return None


def validate_record_references(manifests: list[tuple[Path, dict[str, Any]]]) -> None:
    records: dict[str, tuple[str, Path, dict[str, Any]]] = {}
    by_kind: dict[str, set[str]] = defaultdict(set)

    lock = read_json(ROOT / "external/tools.lock.json")
    external_ids = {tool["id"] for tool in lock["tools"]}

    for path, record in manifests:
        record_id = record.get("id")
        if not isinstance(record_id, str):
            continue
        kind = record_kind(record_id)
        if kind is None:
            continue
        if record_id in records:
            previous = records[record_id][1].relative_to(ROOT)
            fail(f"Duplicate record ID {record_id}: {previous} and {path.relative_to(ROOT)}")
        records[record_id] = (kind, path, record)
        by_kind[kind].add(record_id)

    def require_reference(owner: str, target: str | None, kind: str) -> None:
        if target is None:
            return
        if target not in by_kind[kind]:
            fail(f"{owner} references missing {kind} ID: {target}")

    def require_many(owner: str, targets: list[str] | None, kind: str) -> None:
        for target in targets or []:
            require_reference(owner, target, kind)

    for record_id, (kind, path, record) in records.items():
        owner = f"{record_id} ({path.relative_to(ROOT)})"
        if kind == "evidence":
            require_reference(owner, record.get("experiment_id"), "experiment")
            require_many(owner, record.get("observation_ids"), "observation")
            repository_path = record.get("repository_path")
            if repository_path:
                resolved = (ROOT / repository_path).resolve()
                try:
                    resolved.relative_to(ROOT.resolve())
                except ValueError:
                    fail(f"Evidence path escapes repository: {owner}")
                if not resolved.is_file():
                    fail(f"Evidence path does not exist: {owner} -> {repository_path}")
        elif kind == "observation":
            require_reference(owner, record.get("experiment_id"), "experiment")
            require_many(owner, record.get("evidence_ids"), "evidence")
        elif kind == "asset":
            require_many(owner, record.get("derived_from"), "asset")
        elif kind == "transformation":
            require_many(owner, record.get("input_asset_ids"), "asset")
            require_many(owner, record.get("output_asset_ids"), "asset")
            require_many(owner, record.get("preserved_unknowns"), "unknown")
            require_reference(owner, record.get("log_evidence_id"), "evidence")
            external_tool_id = record.get("tool", {}).get("external_tool_id")
            if external_tool_id is not None and external_tool_id not in external_ids:
                fail(f"{owner} references missing external tool ID: {external_tool_id}")
        elif kind == "unknown":
            require_reference(owner, record.get("source_asset_id"), "asset")
            require_many(owner, record.get("raw_evidence_ids"), "evidence")
        elif kind == "claim":
            require_many(owner, record.get("evidence_ids"), "evidence")
            require_many(owner, record.get("experiment_ids"), "experiment")
            for source_id in record.get("source_ids", []):
                if source_id.startswith("EXT-") and source_id not in external_ids:
                    fail(f"{owner} references missing external source ID: {source_id}")
        elif kind == "node":
            require_many(owner, record.get("experiment_ids"), "experiment")


def validate_external_tool_records() -> None:
    lock = read_json(ROOT / "external/tools.lock.json")
    ids = [tool["id"] for tool in lock["tools"]]
    if len(ids) != len(set(ids)):
        fail("Duplicate external tool IDs")

    for tool in lock["tools"]:
        if not re.fullmatch(r"[0-9a-f]{40}", tool["commit"]):
            fail(f"Invalid commit pin for {tool['id']}")
        record_path = ROOT / tool["record_path"]
        if not record_path.is_file():
            fail(f"Missing external tool record for {tool['id']}: {tool['record_path']}")


def validate_yaml() -> None:
    if yaml is None:
        if os.environ.get("VIRTUALAUTO_STRICT_VALIDATION") == "1":
            fail("PyYAML is required for strict validation")
        print("warning: PyYAML unavailable; YAML parsing skipped")
        return
    for pattern in ("*.yml", "*.yaml"):
        for path in ROOT.rglob(pattern):
            with path.open(encoding="utf-8") as handle:
                document = yaml.safe_load(handle)
            if document is None:
                fail(f"Empty YAML document: {path.relative_to(ROOT)}")


def validate_local_markdown_links() -> None:
    link_pattern = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            target = target.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"Local link escapes repository: {path.relative_to(ROOT)} -> {target}")
            if not resolved.exists():
                fail(f"Broken local link: {path.relative_to(ROOT)} -> {target}")


def main() -> int:
    validation_errors: list[type[BaseException]] = [
        OSError,
        ValueError,
        json.JSONDecodeError,
    ]
    if yaml is not None:
        validation_errors.append(yaml.YAMLError)
    if jsonschema is not None:
        validation_errors.extend([jsonschema.ValidationError, jsonschema.SchemaError])

    try:
        validate_required_structure()
        validate_no_prohibited_artifacts()
        validate_json_syntax()
        schemas = validate_schema_documents()
        manifests = validate_manifest_instances(schemas)
        validate_record_references(manifests)
        validate_external_tool_records()
        validate_yaml()
        validate_local_markdown_links()
    except tuple(validation_errors) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1

    print(
        "repository validation passed: "
        f"{len(schemas)} schemas, {len(manifests)} schema-backed manifests"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
