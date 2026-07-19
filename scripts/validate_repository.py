"""Validate the small, deterministic invariants of the VirtualAuto repository."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

try:
    import jsonschema
except ModuleNotFoundError:  # CI installs it; local bootstrap may not have it yet.
    jsonschema = None

try:
    import yaml
except ModuleNotFoundError:  # CI installs it; local bootstrap may not have it yet.
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_PATHS = (
    "README.md",
    ".gitignore",
    "docs/PROJECT_DOCTRINE.md",
    "knowledge/README.md",
    "external/README.md",
    "external/tools.lock.json",
    "experiments/TEMPLATE.md",
    "schemas/experiment.schema.json",
    "schemas/evidence.schema.json",
    "schemas/observation.schema.json",
)


def fail(message: str) -> None:
    raise ValueError(message)


def validate_json() -> None:
    for path in ROOT.rglob("*.json"):
        with path.open(encoding="utf-8") as handle:
            json.load(handle)

    if jsonschema is not None:
        lock_path = ROOT / "external/tools.lock.json"
        schema_path = ROOT / "schemas/external-tool.schema.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = jsonschema.Draft202012Validator(
            schema, format_checker=jsonschema.FormatChecker()
        )
        validator.validate(lock)
    elif os.environ.get("VIRTUALAUTO_STRICT_VALIDATION") == "1":
        fail("jsonschema is required for strict validation")
    else:
        print("warning: jsonschema unavailable; schema validation skipped")


def validate_yaml() -> None:
    if yaml is None:
        if os.environ.get("VIRTUALAUTO_STRICT_VALIDATION") == "1":
            fail("PyYAML is required for strict validation")
        print("warning: PyYAML unavailable; YAML parsing skipped")
        return
    for pattern in ("*.yml", "*.yaml"):
        for path in ROOT.rglob(pattern):
            with path.open(encoding="utf-8") as handle:
                yaml.safe_load(handle)


def validate_structure() -> None:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).is_file()]
    if missing:
        fail(f"Missing required paths: {', '.join(missing)}")

    lock = json.loads((ROOT / "external/tools.lock.json").read_text(encoding="utf-8"))
    ids = [tool["id"] for tool in lock["tools"]]
    if len(ids) != len(set(ids)):
        fail("Duplicate external tool IDs")

    for tool in lock["tools"]:
        if not re.fullmatch(r"[0-9a-f]{40}", tool["commit"]):
            fail(f"Invalid commit pin for {tool['id']}")


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
    validation_errors = [OSError, ValueError, json.JSONDecodeError]
    if yaml is not None:
        validation_errors.append(yaml.YAMLError)
    if jsonschema is not None:
        validation_errors.append(jsonschema.ValidationError)
    try:
        validate_json()
        validate_yaml()
        validate_structure()
        validate_local_markdown_links()
    except tuple(validation_errors) as error:
        print(f"validation failed: {error}", file=sys.stderr)
        return 1
    print("repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
