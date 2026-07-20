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


def vector(values: object) -> list[float]:
    return [round(float(value), 9) for value in values]


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
    objects: list[dict[str, object]] = []
    for object_ in sorted(bpy.data.objects, key=lambda item: item.name):
        entry: dict[str, object] = {
            "name": object_.name,
            "type": object_.type,
            "parent": object_.parent.name if object_.parent else None,
            "collections": sorted(
                collection.name for collection in object_.users_collection
            ),
            "location": vector(object_.location),
            "rotation_euler": vector(object_.rotation_euler),
            "scale": vector(object_.scale),
            "matrix_determinant": round(float(object_.matrix_world.determinant()), 9),
            "modifiers": [
                {"name": modifier.name, "type": modifier.type}
                for modifier in object_.modifiers
            ],
            "custom_properties": sorted(set(object_.keys()) - {"_RNA_UI"}),
        }
        if object_.type == "MESH":
            mesh = object_.data
            entry["mesh"] = {
                "name": mesh.name,
                "vertices": len(mesh.vertices),
                "edges": len(mesh.edges),
                "polygons": len(mesh.polygons),
                "loops": len(mesh.loops),
                "uv_layers": [layer.name for layer in mesh.uv_layers],
                "color_attributes": [
                    {
                        "name": attribute.name,
                        "data_type": attribute.data_type,
                        "domain": attribute.domain,
                    }
                    for attribute in mesh.color_attributes
                ],
                "attributes": [
                    {
                        "name": attribute.name,
                        "data_type": attribute.data_type,
                        "domain": attribute.domain,
                        "count": len(attribute.data),
                    }
                    for attribute in mesh.attributes
                    if not attribute.is_internal
                ],
                "materials": [
                    material.name if material else None for material in mesh.materials
                ],
                "shape_keys": (
                    [block.name for block in mesh.shape_keys.key_blocks]
                    if mesh.shape_keys
                    else []
                ),
            }
        objects.append(entry)

    report = {
        "$schema": Path(
            os.path.relpath(ROOT / "lab/schemas/mesh-report.schema.json", output.parent)
        ).as_posix(),
        "schema_version": "1.0.0",
        "id": args.id,
        "captured_at": datetime.now(UTC).isoformat(),
        "blender_version": bpy.app.version_string,
        "source": {
            "basename": source.name if source else None,
            "sha256": sha256(source) if source and source.is_file() else None,
        },
        "scene": {
            "name": bpy.context.scene.name,
            "unit_system": bpy.context.scene.unit_settings.system,
            "unit_scale_length": bpy.context.scene.unit_settings.scale_length,
            "object_count": len(objects),
        },
        "objects": objects,
        "materials": sorted(material.name for material in bpy.data.materials),
        "images": sorted(
            (
                {
                    "name": image.name,
                    "source": image.source,
                    "basename": Path(image.filepath).name if image.filepath else None,
                }
                for image in bpy.data.images
            ),
            key=lambda item: item["name"],
        ),
        "scope": "non-mutating structural inventory; no visual-quality claim",
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
