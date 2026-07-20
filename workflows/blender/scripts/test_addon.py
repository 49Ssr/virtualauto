"""Exercise the development add-on inside Blender 5.0.1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy

BASELINE_VERSION = (5, 0, 1)
ROOT = Path(__file__).resolve().parents[3]
ADDON_ROOT = ROOT / "workflows/blender/addon"


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    return parser.parse_args(argv)


def main() -> int:
    if tuple(bpy.app.version[:3]) != BASELINE_VERSION:
        raise SystemExit(f"Expected Blender 5.0.1, got {bpy.app.version_string}")
    sys.path.insert(0, str(ADDON_ROOT))
    import virtualauto_blender

    args = parse_args()
    output = Path(args.output).resolve()
    virtualauto_blender.register()
    try:
        result = bpy.ops.virtualauto.export_inventory(
            "EXEC_DEFAULT",
            filepath=str(output),
            active_only=False,
        )
        if result != {"FINISHED"}:
            raise RuntimeError(f"Inventory operator failed: {result}")
        payload = json.loads(output.read_text(encoding="utf-8"))
        if payload["scene"]["object_count"] != 1:
            raise RuntimeError("Development add-on did not inventory the smoke object")
        if payload["objects"][0]["name"] != "VA_SmokeObject":
            raise RuntimeError("Development add-on returned the wrong smoke object")
    finally:
        virtualauto_blender.unregister()
    print(f"validated VirtualAuto development add-on: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
