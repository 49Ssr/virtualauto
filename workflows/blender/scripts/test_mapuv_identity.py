"""Falsify Blender compositor Map UV coordinate conventions.

The test compares two generated identity maps against an unmodified float
source image. Blender 5.2 reproduces the source exactly when pixel centres are
encoded as ``(x + 0.5) / width`` and ``(y + 0.5) / height``. The script creates
temporary datablocks, renders three tiny compositor passes, writes one JSON
report, and removes its temporary data without saving the blend file.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from array import array
from pathlib import Path

import bpy

PREFIX = "VA_TMP_MAPUV_IDENTITY"
WIDTH = 64
HEIGHT = 32


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def clear_temporary() -> None:
    for datablocks in (
        bpy.data.scenes,
        bpy.data.node_groups,
        bpy.data.images,
        bpy.data.objects,
        bpy.data.cameras,
        bpy.data.meshes,
    ):
        for datablock in list(datablocks):
            if datablock.name.startswith(PREFIX):
                datablocks.remove(datablock)


def new_float_image(name: str, pixels: array) -> bpy.types.Image:
    image = bpy.data.images.new(
        name,
        width=WIDTH,
        height=HEIGHT,
        alpha=True,
        float_buffer=True,
    )
    image.colorspace_settings.name = "Non-Color"
    image.pixels.foreach_set(pixels)
    image.update()
    return image


def capture_render(scene: bpy.types.Scene, label: str) -> array:
    path = Path(bpy.app.tempdir) / f"va_mapuv_identity_{label}.exr"
    scene.render.filepath = str(path)
    operator_result = (
        bpy.ops.render.render(write_still=True)
        if bpy.context.window is not None
        else bpy.ops.render.render(write_still=True, scene=scene.name)
    )
    if "FINISHED" not in operator_result:
        raise RuntimeError(f"Render failed: {sorted(operator_result)}")
    render_result = bpy.data.images.load(str(path), check_existing=False)
    if tuple(render_result.size) != (WIDTH, HEIGHT):
        actual = tuple(render_result.size)
        raise RuntimeError(
            f"Map UV identity gate returned the wrong render domain: {actual}"
        )
    values = array("f", [0.0]) * (WIDTH * HEIGHT * 4)
    render_result.pixels.foreach_get(values)
    bpy.data.images.remove(render_result)
    path.unlink(missing_ok=True)
    return values


def compare(reference: array, candidate: array) -> dict[str, float]:
    squared_error = 0.0
    absolute_error = 0.0
    maximum_error = 0.0
    sample_count = WIDTH * HEIGHT * 3
    for pixel in range(WIDTH * HEIGHT):
        for channel in range(3):
            index = pixel * 4 + channel
            difference = abs(candidate[index] - reference[index])
            squared_error += difference * difference
            absolute_error += difference
            maximum_error = max(maximum_error, difference)
    mse = squared_error / sample_count
    return {
        "mse_rgb": mse,
        "psnr_db": math.inf if mse == 0.0 else 10.0 * math.log10(1.0 / mse),
        "absolute_difference_mean": absolute_error / sample_count,
        "absolute_difference_max": maximum_error,
    }


def main() -> int:
    args = parse_args()
    output = Path(args.output).resolve()
    if output.exists() and not args.overwrite:
        raise SystemExit(f"Output exists; use --overwrite intentionally: {output}")
    clear_temporary()

    source_pixels = array("f")
    edge_domain_pixels = array("f")
    pixel_centre_pixels = array("f")
    for y in range(HEIGHT):
        for x in range(WIDTH):
            checker = 0.20 if ((x // 3 + y // 2) % 2) else 0.0
            source_pixels.extend(
                (
                    min(1.0, x / (WIDTH - 1) * 0.8 + checker),
                    min(1.0, y / (HEIGHT - 1) * 0.8 + checker),
                    ((x * 17 + y * 31) % 97) / 96.0,
                    1.0,
                )
            )
            edge_domain_pixels.extend(
                (x / (WIDTH - 1), y / (HEIGHT - 1), 1.0, 1.0)
            )
            pixel_centre_pixels.extend(
                ((x + 0.5) / WIDTH, (y + 0.5) / HEIGHT, 1.0, 1.0)
            )

    source = new_float_image(PREFIX + "_SOURCE", source_pixels)
    edge_domain = new_float_image(PREFIX + "_EDGE_DOMAIN", edge_domain_pixels)
    pixel_centre = new_float_image(PREFIX + "_PIXEL_CENTRE", pixel_centre_pixels)

    scene = bpy.data.scenes.new(PREFIX)
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = WIDTH
    scene.render.resolution_y = HEIGHT
    scene.render.resolution_percentage = 100
    scene.render.use_compositing = True
    scene.render.use_sequencer = False
    scene.render.image_settings.file_format = "OPEN_EXR"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "32"
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"
    scene.view_settings.exposure = 0.0
    scene.view_settings.gamma = 1.0

    camera_data = bpy.data.cameras.new(PREFIX + "_CAMERA_DATA")
    camera = bpy.data.objects.new(PREFIX + "_CAMERA", camera_data)
    scene.collection.objects.link(camera)
    scene.camera = camera
    mesh = bpy.data.meshes.new(PREFIX + "_PLANE_MESH")
    mesh.from_pydata(
        [(-1.0, -1.0, -3.0), (1.0, -1.0, -3.0), (1.0, 1.0, -3.0), (-1.0, 1.0, -3.0)],
        [],
        [(0, 1, 2, 3)],
    )
    plane = bpy.data.objects.new(PREFIX + "_PLANE", mesh)
    scene.collection.objects.link(plane)

    tree = bpy.data.node_groups.new(PREFIX + "_TREE", "CompositorNodeTree")
    tree.interface.new_socket(
        name="Image", in_out="OUTPUT", socket_type="NodeSocketColor"
    )
    scene.compositing_node_group = tree
    source_node = tree.nodes.new("CompositorNodeImage")
    source_node.image = source
    uv_node = tree.nodes.new("CompositorNodeImage")
    remap = tree.nodes.new("CompositorNodeMapUV")
    output_node = tree.nodes.new("NodeGroupOutput")
    tree.links.new(source_node.outputs["Image"], remap.inputs["Image"])
    tree.links.new(uv_node.outputs["Image"], remap.inputs["UV"])

    tree.links.new(source_node.outputs["Image"], output_node.inputs["Image"])
    window = bpy.context.window
    previous_scene = window.scene if window is not None else None
    if window is not None:
        window.scene = scene
    try:
        reference = capture_render(scene, "source")
        tree.links.remove(output_node.inputs["Image"].links[0])
        tree.links.new(remap.outputs["Image"], output_node.inputs["Image"])

        uv_node.image = edge_domain
        edge_result = capture_render(scene, "edge")
        uv_node.image = pixel_centre
        centre_result = capture_render(scene, "centre")
    finally:
        if window is not None and previous_scene is not None:
            window.scene = previous_scene

    report = {
        "schema_version": "1.0.0",
        "blender_version": ".".join(str(value) for value in bpy.app.version[:3]),
        "resolution": [WIDTH, HEIGHT],
        "edge_domain_x_over_width_minus_one": compare(reference, edge_result),
        "pixel_centre_domain": compare(reference, centre_result),
    }
    report["status"] = (
        "passed"
        if report["pixel_centre_domain"]["mse_rgb"] == 0.0
        and report["edge_domain_x_over_width_minus_one"]["mse_rgb"] > 0.0
        else "failed"
    )
    scene.compositing_node_group = None
    clear_temporary()
    report["cleanup_complete"] = not any(
        datablock.name.startswith(PREFIX)
        for datablocks in (
            bpy.data.scenes,
            bpy.data.node_groups,
            bpy.data.images,
            bpy.data.objects,
            bpy.data.cameras,
            bpy.data.meshes,
        )
        for datablock in datablocks
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "output": str(output)}))
    return 0 if report["status"] == "passed" and report["cleanup_complete"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
