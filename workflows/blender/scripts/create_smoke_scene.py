"""Create a deterministic, repository-owned Blender smoke-test scene."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import bpy

BASELINE_VERSION = (5, 0, 1)


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def require_socket(node: bpy.types.Node, name: str) -> bpy.types.NodeSocket:
    socket = node.inputs.get(name)
    if socket is None:
        raise RuntimeError(f"Blender 5.0.1 socket is unavailable: {name}")
    return socket


def main() -> int:
    args = parse_args()
    if tuple(bpy.app.version[:3]) != BASELINE_VERSION:
        raise SystemExit(f"Expected Blender 5.0.1, got {bpy.app.version_string}")

    output = Path(args.output).expanduser().resolve()
    if output.suffix.lower() != ".blend":
        raise SystemExit("Smoke output must use the .blend extension")
    if output.exists() and not args.overwrite:
        raise SystemExit(f"Output exists; pass --overwrite intentionally: {output}")

    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    mesh = bpy.data.meshes.new("VA_SmokeMesh")
    mesh.from_pydata(
        [(-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0)],
        [(0, 1), (1, 2), (2, 3), (3, 0)],
        [(0, 1, 2, 3)],
    )
    mesh.update()

    uv_layer = mesh.uv_layers.new(name="UVMap")
    coordinates = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))
    for loop, coordinate in zip(uv_layer.uv, coordinates, strict=True):
        loop.vector = coordinate

    colours = mesh.color_attributes.new(
        name="va_smoke_color", type="FLOAT_COLOR", domain="CORNER"
    )
    for item in colours.data:
        item.color = (0.12, 0.36, 0.82, 1.0)

    region = mesh.attributes.new(name="va_region_id", type="INT", domain="FACE")
    region.data[0].value = 7

    material = bpy.data.materials.new("VA_SmokeMaterial")
    material.use_nodes = True
    principled = material.node_tree.nodes.get("Principled BSDF")
    if principled is None:
        raise RuntimeError("Blender 5.0.1 Principled BSDF node was not created")
    require_socket(principled, "Base Color").default_value = (0.03, 0.11, 0.32, 1.0)
    require_socket(principled, "Metallic").default_value = 0.2
    require_socket(principled, "Roughness").default_value = 0.28
    mesh.materials.append(material)

    object_ = bpy.data.objects.new("VA_SmokeObject", mesh)
    object_["virtualauto_fixture"] = "synthetic-structural-smoke-v1"
    bpy.context.collection.objects.link(object_)
    bevel = object_.modifiers.new(name="VA_SmokeBevel", type="BEVEL")
    bevel.width = 0.01
    bevel.segments = 2

    scene = bpy.context.scene
    scene.name = "VA_SmokeScene"
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    # Blender 5.0.1 exposes EEVEE through this RNA enum. Do not reuse the older
    # 4.x-facing label without runtime verification.
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 640
    scene.render.resolution_y = 360
    scene.render.resolution_percentage = 100

    bpy.context.view_layer.objects.active = object_
    object_.select_set(True)
    output.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False)
    print(f"created deterministic smoke scene: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
