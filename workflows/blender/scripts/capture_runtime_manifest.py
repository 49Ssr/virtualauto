"""Capture a conservative Blender execution manifest.

Run from Blender with arguments after `--`. This script records runtime state;
it does not render, mutate the scene, or claim visual validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

import bpy

BASELINE_VERSION = (5, 0, 1)
ROOT = Path(__file__).resolve().parents[3]
RUN_ID = re.compile(r"^RUN-[A-Z0-9]+(?:-[A-Z0-9]+)+$")


def decoded(value: object) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument(
        "--output",
        default="lab/evidence/manifests/blender-run.json",
    )
    parser.add_argument("--allow-version-mismatch", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    if not RUN_ID.fullmatch(args.id):
        raise SystemExit("Run ID must match RUN-[A-Z0-9]+(?:-[A-Z0-9]+)+")

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
        raise SystemExit(
            f"Output already exists; use --overwrite intentionally: {output}"
        )

    schema_path = ROOT / "lab/schemas/blender-run.schema.json"
    schema_ref = Path(os.path.relpath(schema_path, output.parent)).as_posix()

    actual_version = tuple(bpy.app.version[:3])
    if actual_version != BASELINE_VERSION and not args.allow_version_mismatch:
        raise SystemExit(
            "Blender version mismatch: expected 5.0.1, "
            f"got {'.'.join(map(str, actual_version))}"
        )

    scene = bpy.context.scene
    blend_path = Path(bpy.data.filepath) if bpy.data.filepath else None
    source_sha256 = (
        file_sha256(blend_path) if blend_path and blend_path.is_file() else None
    )

    samples = None
    denoising = None
    device = None
    cycles = getattr(scene, "cycles", None)
    if cycles is not None:
        samples = getattr(cycles, "samples", None)
        denoising = getattr(cycles, "use_denoising", None)
        device = getattr(cycles, "device", None)

    ocio_path = os.environ.get("OCIO")
    ocio_sha256 = None
    if ocio_path:
        candidate = Path(ocio_path)
        if candidate.is_file():
            ocio_sha256 = file_sha256(candidate)

    manifest = {
        "$schema": schema_ref,
        "schema_version": "1.0.0",
        "id": args.id,
        "status": "captured",
        "captured_at": datetime.now(UTC).isoformat(),
        "blender": {
            "version": bpy.app.version_string,
            "version_tuple": list(actual_version),
            "build_hash": decoded(getattr(bpy.app, "build_hash", "unavailable")),
            "build_branch": decoded(getattr(bpy.app, "build_branch", "unavailable")),
            "build_type": decoded(getattr(bpy.app, "build_type", "unavailable")),
        },
        "host": {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
        },
        "scene": {
            "name": scene.name,
            "source_path": blend_path.name if blend_path else None,
            "source_sha256": source_sha256,
        },
        "render": {
            "engine": scene.render.engine,
            "resolution_x": scene.render.resolution_x,
            "resolution_y": scene.render.resolution_y,
            "resolution_percentage": scene.render.resolution_percentage,
            "frame": scene.frame_current,
            "samples": samples,
            "denoising": denoising,
            "device": device,
        },
        "colour_management": {
            "display_device": scene.display_settings.display_device,
            "view_transform": scene.view_settings.view_transform,
            "look": scene.view_settings.look,
            "exposure": scene.view_settings.exposure,
            "gamma": scene.view_settings.gamma,
            "ocio_config_sha256": ocio_sha256,
        },
        "evidence_state": "runtime-metadata-only",
        "notes": [
            "This manifest records runtime metadata only; it is not render or "
            "visual evidence.",
            "ocio_config_sha256 records only a checksum of an explicit OCIO override.",
        ],
    }

    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(output)
    print(f"wrote Blender runtime manifest: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
