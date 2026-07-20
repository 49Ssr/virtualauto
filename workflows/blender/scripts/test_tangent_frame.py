"""Validate the panel-relative orthonormal-frame construction in Blender."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy
from mathutils import Vector

BASELINE_VERSION = (5, 0, 1)
TOLERANCE = 1.0e-7


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)


def tangent_frame(normal: Vector, tangent: Vector) -> tuple[Vector, Vector, Vector]:
    normal = normal.normalized()
    projected = tangent - normal * normal.dot(tangent)
    if projected.length_squared <= 1.0e-20:
        axes = (
            Vector((1.0, 0.0, 0.0)),
            Vector((0.0, 1.0, 0.0)),
            Vector((0.0, 0.0, 1.0)),
        )
        fallback = min(axes, key=lambda axis: abs(normal.dot(axis)))
        projected = fallback - normal * normal.dot(fallback)
    tangent = projected.normalized()
    bitangent = normal.cross(tangent).normalized()
    tangent = bitangent.cross(normal).normalized()
    return normal, tangent, bitangent


def metrics(normal: Vector, tangent: Vector) -> dict[str, float]:
    normal, tangent, bitangent = tangent_frame(normal, tangent)
    return {
        "normal_length_error": abs(normal.length - 1.0),
        "tangent_length_error": abs(tangent.length - 1.0),
        "bitangent_length_error": abs(bitangent.length - 1.0),
        "normal_tangent_dot": abs(normal.dot(tangent)),
        "normal_bitangent_dot": abs(normal.dot(bitangent)),
        "tangent_bitangent_dot": abs(tangent.dot(bitangent)),
        "handedness_error": abs(tangent.cross(bitangent).dot(normal) - 1.0),
    }


def main() -> int:
    args = parse_args()
    if tuple(bpy.app.version[:3]) != BASELINE_VERSION:
        raise SystemExit(f"Expected Blender 5.0.1, got {bpy.app.version_string}")
    cases = {
        "orthogonal": metrics(Vector((0, 0, 1)), Vector((1, 0, 0))),
        "contaminated": metrics(Vector((0.2, 0.1, 1.0)), Vector((1, 0, 0.8))),
        "parallel_fallback": metrics(Vector((0, 0, 1)), Vector((0, 0, 4))),
        "oblique": metrics(Vector((-0.5, 0.8, 0.3)), Vector((0.3, 0.9, -0.2))),
    }
    maximum_error = max(value for case in cases.values() for value in case.values())
    passed = maximum_error <= TOLERANCE
    report = {
        "test_id": "MATH-VA-TANGENT-FRAME-001",
        "blender_version": bpy.app.version_string,
        "tolerance": TOLERANCE,
        "cases": cases,
        "maximum_error": maximum_error,
        "passed": passed,
        "scope": (
            "mathematical frame invariant only; no claim about shader appearance, "
            "mesh tangents, or carbon-fibre validation"
        ),
    }
    output = Path(args.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    if not passed:
        raise RuntimeError(f"Tangent-frame invariant failed: {maximum_error}")
    print(f"validated tangent-frame invariant: {maximum_error:.3e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
