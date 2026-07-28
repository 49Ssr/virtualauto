"""Audit a loaded Blender scene against a camera/compositor contract.

Run from Blender with arguments after ``--``. The script is read-only: it does
not save, render, create nodes, or change the scene. A mismatch returns a
non-zero exit status after writing a complete report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from array import array
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import bpy

ROOT = Path(__file__).resolve().parents[3]


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def resolved_path(value: str) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def add_check(
    checks: list[dict[str, Any]],
    *,
    identifier: str,
    expected: Any,
    actual: Any,
    passed: bool,
) -> None:
    checks.append(
        {
            "id": identifier,
            "passed": bool(passed),
            "expected": expected,
            "actual": actual,
        }
    )


def close(actual: float, expected: float, tolerance: float = 1e-6) -> bool:
    return math.isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance)


def float32_le_sha256(values: array) -> str:
    canonical = values
    if sys.byteorder != "little":
        canonical = array("f", values)
        canonical.byteswap()
    return hashlib.sha256(canonical.tobytes()).hexdigest()


def compositor_group(scene: bpy.types.Scene) -> bpy.types.NodeTree | None:
    group = getattr(scene, "compositing_node_group", None)
    if group is not None:
        return group
    return getattr(scene, "node_tree", None)


def main() -> int:
    args = parse_args()
    contract_path = resolved_path(args.contract)
    output_path = resolved_path(args.output)
    if not contract_path.is_file():
        raise SystemExit(f"Camera contract does not exist: {contract_path}")
    if output_path.exists() and not args.overwrite:
        raise SystemExit(
            f"Audit output exists; use --overwrite intentionally: {output_path}"
        )

    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    scene = bpy.context.scene
    camera_object = scene.camera
    camera_data = camera_object.data if camera_object else None
    checks: list[dict[str, Any]] = []

    expected_version = contract["blender_version"]
    actual_version = ".".join(str(value) for value in bpy.app.version[:3])
    add_check(
        checks,
        identifier="blender.version",
        expected=expected_version,
        actual=actual_version,
        passed=actual_version == expected_version,
    )

    camera = contract["camera"]
    add_check(
        checks,
        identifier="camera.object_name",
        expected=camera["object_name"],
        actual=camera_object.name if camera_object else None,
        passed=(
            camera_object is not None
            and camera_object.name == camera["object_name"]
        ),
    )
    if camera_data is not None:
        for key, actual in (
            ("focal_length_mm", float(camera_data.lens)),
            ("sensor_width_mm", float(camera_data.sensor_width)),
            ("sensor_height_mm", float(camera_data.sensor_height)),
            ("aperture_f_number", float(camera_data.dof.aperture_fstop)),
        ):
            expected = float(camera[key])
            add_check(
                checks,
                identifier=f"camera.{key}",
                expected=expected,
                actual=actual,
                passed=close(actual, expected),
            )
        expected_focus = camera.get("focus_object")
        actual_focus = (
            camera_data.dof.focus_object.name
            if camera_data.dof.focus_object is not None
            else None
        )
        add_check(
            checks,
            identifier="camera.focus_object",
            expected=expected_focus,
            actual=actual_focus,
            passed=actual_focus == expected_focus,
        )

    scale = scene.render.resolution_percentage / 100.0
    resolution = [
        round(scene.render.resolution_x * scale),
        round(scene.render.resolution_y * scale),
    ]
    add_check(
        checks,
        identifier="render.effective_resolution",
        expected=contract["render"]["effective_resolution"],
        actual=resolution,
        passed=resolution == contract["render"]["effective_resolution"],
    )
    add_check(
        checks,
        identifier="render.engine",
        expected=contract["render"]["engine"],
        actual=scene.render.engine,
        passed=scene.render.engine == contract["render"]["engine"],
    )
    cycles = scene.cycles
    render_contract = contract["render"]
    render_values = (
        ("device", cycles.device),
        ("samples", int(cycles.samples)),
        ("adaptive_sampling", bool(cycles.use_adaptive_sampling)),
        ("adaptive_threshold", float(cycles.adaptive_threshold)),
        ("denoising", bool(cycles.use_denoising)),
        ("denoiser", cycles.denoiser),
        ("compositor_device", scene.render.compositor_device),
        ("compositor_precision", scene.render.compositor_precision),
    )
    for key, actual in render_values:
        expected = render_contract[key]
        passed = (
            close(actual, expected)
            if isinstance(expected, float)
            else actual == expected
        )
        add_check(
            checks,
            identifier=f"render.{key}",
            expected=expected,
            actual=actual,
            passed=passed,
        )

    colour = contract["colour_management"]
    for key, actual in (
        ("view_transform", scene.view_settings.view_transform),
        ("look", scene.view_settings.look),
        ("exposure", float(scene.view_settings.exposure)),
        ("gamma", float(scene.view_settings.gamma)),
    ):
        expected = colour[key]
        passed = (
            close(actual, expected)
            if isinstance(expected, (int, float))
            else actual == expected
        )
        add_check(
            checks,
            identifier=f"colour_management.{key}",
            expected=expected,
            actual=actual,
            passed=passed,
        )

    group = compositor_group(scene)
    compositor = contract["compositor"]
    add_check(
        checks,
        identifier="compositor.node_group",
        expected=compositor["node_group"],
        actual=group.name if group else None,
        passed=group is not None and group.name == compositor["node_group"],
    )
    nodes = group.nodes if group else None
    for expected_node in compositor["required_nodes"]:
        node = nodes.get(expected_node["name"]) if nodes else None
        add_check(
            checks,
            identifier=f"compositor.node.{expected_node['name']}.exists",
            expected=True,
            actual=node is not None,
            passed=node is not None,
        )
        if node is None:
            continue
        add_check(
            checks,
            identifier=f"compositor.node.{node.name}.muted",
            expected=expected_node["muted"],
            actual=bool(node.mute),
            passed=bool(node.mute) == expected_node["muted"],
        )
        property_name = expected_node.get("status_property")
        if property_name:
            actual = node.get(property_name)
            expected = expected_node.get("status_value")
            add_check(
                checks,
                identifier=f"compositor.node.{node.name}.{property_name}",
                expected=expected,
                actual=actual,
                passed=actual == expected,
            )

    for value_check in compositor["value_checks"]:
        node = nodes.get(value_check["node"]) if nodes else None
        identifier = value_check["input_identifier"]
        socket = None
        if node is not None:
            socket = next(
                (item for item in node.inputs if item.identifier == identifier),
                None,
            )
        actual = float(socket.default_value) if socket is not None else None
        expected = float(value_check["expected"])
        tolerance = float(value_check["tolerance"])
        add_check(
            checks,
            identifier=(
                f"compositor.node.{value_check['node']}.input.{identifier}"
            ),
            expected=expected,
            actual=actual,
            passed=actual is not None and close(actual, expected, tolerance),
        )

    for image_check in compositor["image_checks"]:
        node = nodes.get(image_check["node"]) if nodes else None
        image = getattr(node, "image", None) if node is not None else None
        expected_name = image_check["image_name"]
        actual_name = image.name if image is not None else None
        add_check(
            checks,
            identifier=f"compositor.node.{image_check['node']}.image_name",
            expected=expected_name,
            actual=actual_name,
            passed=actual_name == expected_name,
        )
        if image is None:
            continue
        expected_size = [image_check["width"], image_check["height"]]
        actual_size = [int(image.size[0]), int(image.size[1])]
        add_check(
            checks,
            identifier=f"compositor.image.{expected_name}.size",
            expected=expected_size,
            actual=actual_size,
            passed=actual_size == expected_size,
        )
        expected_packed = bool(image_check["packed"])
        actual_packed = image.packed_file is not None
        add_check(
            checks,
            identifier=f"compositor.image.{expected_name}.packed",
            expected=expected_packed,
            actual=actual_packed,
            passed=actual_packed == expected_packed,
        )
        pixel_values = array("f", [0.0]) * (actual_size[0] * actual_size[1] * 4)
        image.pixels.foreach_get(pixel_values)
        actual_hash = float32_le_sha256(pixel_values)
        expected_hash = image_check["float32_sha256_native_little_endian"]
        add_check(
            checks,
            identifier=f"compositor.image.{expected_name}.float32_sha256",
            expected=expected_hash,
            actual=actual_hash,
            passed=actual_hash == expected_hash,
        )

    failed = [check["id"] for check in checks if not check["passed"]]
    report = {
        "schema_version": "1.0.0",
        "contract_id": contract["id"],
        "contract_path": contract_path.relative_to(ROOT).as_posix()
        if contract_path.is_relative_to(ROOT)
        else contract_path.name,
        "captured_at": datetime.now(UTC).isoformat(),
        "scene_file": Path(bpy.data.filepath).name if bpy.data.filepath else None,
        "status": "passed" if not failed else "failed",
        "failed_checks": failed,
        "checks": checks,
        "notes": [
            "This is a read-only state audit, not visual or optical validation.",
            "A passed audit only establishes that the scene matches the "
            "qualified contract."
        ],
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"status": report["status"], "output": str(output_path)}))
    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())
