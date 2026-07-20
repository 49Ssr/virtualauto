"""Inventory Blender scene structure without mutating the source asset."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

import bpy

BASELINE_VERSION = (5, 0, 1)
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "workflows/blender/addon"))
from virtualauto_blender.inventory import build_inventory  # noqa: E402

REPORT_ID = re.compile(r"^RPT-[A-Z0-9]+(?:-[A-Z0-9]+)+$")


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    args = parse_args()
    if tuple(bpy.app.version[:3]) != BASELINE_VERSION:
        raise SystemExit(f"Expected Blender 5.0.1, got {bpy.app.version_string}")
    if not REPORT_ID.fullmatch(args.id):
        raise SystemExit("Report ID must match RPT-[A-Z0-9]+(?:-[A-Z0-9]+)+")

    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output = output.resolve()
    try:
        output.relative_to(ROOT)
    except ValueError as error:
        raise SystemExit(
            "Output path must remain inside the VirtualAuto repository"
        ) from error
    if output.exists() and not args.overwrite:
        raise SystemExit(f"Output exists; pass --overwrite intentionally: {output}")

    source = Path(bpy.data.filepath).resolve() if bpy.data.filepath else None
    inventory = build_inventory(active_only=False)
    report = {
        "$schema": Path(
            os.path.relpath(ROOT / "lab/schemas/mesh-report.schema.json", output.parent)
        ).as_posix(),
        "schema_version": "1.0.0",
        "id": args.id,
        "captured_at": datetime.now(UTC).isoformat(),
        "blender_version": inventory["blender_version"],
        "source": {
            "basename": source.name if source else None,
            "sha256": sha256(source) if source and source.is_file() else None,
        },
        "scene": inventory["scene"],
        "objects": inventory["objects"],
        "materials": inventory["materials"],
        "images": inventory["images"],
        "scope": inventory["scope"],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(output)
    print(f"wrote Blender asset inventory: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
