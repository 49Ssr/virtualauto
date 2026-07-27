"""Build a non-destructive F40 glass-diagnostic environment in Blender 5.0.1.

The values in this script are deterministic implementation defaults. They are not
radiometric measurements or a recreation of DriveClub lighting.

The script never edits the vehicle. It creates one owned collection, a dedicated
World datablock, diagnostic geometry, broad reflection sources, and a camera. The
result remains P2-buildable until executed and observed in Blender 5.0.1 with
retained evidence.
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

BASELINE_VERSION = (5, 0, 1)
COLLECTION_NAME = "VA_ENV_F40_GLASS_DIAGNOSTIC"
WORLD_NAME = "VA_ENV_F40_GLASS_WORLD"


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", help="Optional .blend output path")
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help=f"Remove and rebuild only the {COLLECTION_NAME} collection",
    )
    return parser.parse_args(argv)


def require_socket(node: bpy.types.Node, name: str) -> bpy.types.NodeSocket:
    socket = node.inputs.get(name)
    if socket is None:
        raise RuntimeError(f"Blender 5.0.1 socket is unavailable: {node.name}.{name}")
    return socket


def remove_owned_collection() -> None:
    collection = bpy.data.collections.get(COLLECTION_NAME)
    if collection is None:
        return
    for object_ in list(collection.all_objects):
        bpy.data.objects.remove(object_, do_unlink=True)
    bpy.data.collections.remove(collection)


def create_owned_collection(replace_existing: bool) -> bpy.types.Collection:
    existing = bpy.data.collections.get(COLLECTION_NAME)
    if existing is not None:
        if not replace_existing:
            raise SystemExit(
                f"{COLLECTION_NAME} already exists; pass --replace-existing intentionally"
            )
        remove_owned_collection()

    collection = bpy.data.collections.new(COLLECTION_NAME)
    bpy.context.scene.collection.children.link(collection)
    collection["virtualauto_status"] = "P2-buildable-unexecuted-by-repository"
    collection["virtualauto_role"] = "F40 glass and normal diagnostic corridor"
    collection["virtualauto_values"] = "deterministic implementation defaults"
    return collection


def move_to_collection(
    object_: bpy.types.Object, collection: bpy.types.Collection
) -> None:
    for source in list(object_.users_collection):
        source.objects.unlink(object_)
    collection.objects.link(object_)


def make_principled_material(
    name: str,
    base_color: tuple[float, float, float, float],
    roughness: float,
    metallic: float = 0.0,
) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    principled = material.node_tree.nodes.get("Principled BSDF")
    if principled is None:
        raise RuntimeError("Blender 5.0.1 Principled BSDF was not created")
    require_socket(principled, "Base Color").default_value = base_color
    require_socket(principled, "Roughness").default_value = roughness
    require_socket(principled, "Metallic").default_value = metallic
    material["virtualauto_parameter_state"] = "implementation-default"
    return material


def make_emission_material(
    name: str,
    color: tuple[float, float, float, float],
    strength: float,
) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    require_socket(emission, "Color").default_value = color
    require_socket(emission, "Strength").default_value = strength
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    material["virtualauto_parameter_state"] = "implementation-default"
    return material


def make_glass_material(name: str) -> bpy.types.Material:
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    glass = nodes.new("ShaderNodeBsdfGlass")
    require_socket(glass, "Color").default_value = (1.0, 1.0, 1.0, 1.0)
    require_socket(glass, "Roughness").default_value = 0.0
    require_socket(glass, "IOR").default_value = 1.5
    links.new(glass.outputs["BSDF"], output.inputs["Surface"])
    material["virtualauto_parameter_state"] = "implementation-default"
    return material


def add_cube(
    collection: bpy.types.Collection,
    name: str,
    location: tuple[float, float, float],
    dimensions: tuple[float, float, float],
    material: bpy.types.Material,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    object_ = bpy.context.object
    if object_ is None:
        raise RuntimeError(f"Failed to create {name}")
    object_.name = name
    object_.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    object_.data.materials.append(material)
    object_["virtualauto_owned"] = True
    move_to_collection(object_, collection)
    return object_


def add_uv_sphere(
    collection: bpy.types.Collection,
    name: str,
    location: tuple[float, float, float],
    radius: float,
    material: bpy.types.Material,
) -> bpy.types.Object:
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=64,
        ring_count=32,
        radius=radius,
        location=location,
    )
    object_ = bpy.context.object
    if object_ is None:
        raise RuntimeError(f"Failed to create {name}")
    object_.name = name
    object_.data.materials.append(material)
    for polygon in object_.data.polygons:
        polygon.use_smooth = True
    object_["virtualauto_owned"] = True
    move_to_collection(object_, collection)
    return object_


def add_area_light(
    collection: bpy.types.Collection,
    name: str,
    location: tuple[float, float, float],
    target: tuple[float, float, float],
    energy: float,
    size: float,
) -> bpy.types.Object:
    data = bpy.data.lights.new(name=name, type="AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    object_ = bpy.data.objects.new(name, data)
    object_.location = location
    direction = Vector(target) - object_.location
    object_.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    object_["virtualauto_parameter_state"] = "implementation-default"
    collection.objects.link(object_)
    return object_


def add_camera(
    collection: bpy.types.Collection,
    location: tuple[float, float, float],
    target: tuple[float, float, float],
) -> bpy.types.Object:
    data = bpy.data.cameras.new("VA_ENV_DIAG_Camera")
    data.lens = 50.0
    data.sensor_width = 36.0
    object_ = bpy.data.objects.new("VA_ENV_DIAG_Camera", data)
    object_.location = location
    direction = Vector(target) - object_.location
    object_.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    object_["virtualauto_parameter_state"] = "implementation-default"
    collection.objects.link(object_)
    return object_


def make_world(scene: bpy.types.Scene) -> bpy.types.World:
    previous = scene.world.name if scene.world is not None else ""
    world = bpy.data.worlds.get(WORLD_NAME) or bpy.data.worlds.new(WORLD_NAME)
    world.use_nodes = True
    background = world.node_tree.nodes.get("Background")
    if background is None:
        raise RuntimeError("Blender 5.0.1 Background node is unavailable")
    require_socket(background, "Color").default_value = (0.18, 0.18, 0.18, 1.0)
    require_socket(background, "Strength").default_value = 0.35
    world["virtualauto_parameter_state"] = "implementation-default"
    world["virtualauto_role"] = "neutral far-field diagnostic fill"
    scene["virtualauto_previous_world"] = previous
    scene.world = world
    return world


def build(collection: bpy.types.Collection) -> None:
    road = make_principled_material(
        "VA_ENV_DIAG_Road_Mat", (0.035, 0.035, 0.035, 1.0), 0.72
    )
    grey = make_principled_material(
        "VA_ENV_DIAG_Grey18_Mat", (0.18, 0.18, 0.18, 1.0), 0.5
    )
    chrome = make_principled_material(
        "VA_ENV_DIAG_Chrome_Mat", (0.8, 0.8, 0.8, 1.0), 0.04, metallic=1.0
    )
    black_gloss = make_principled_material(
        "VA_ENV_DIAG_BlackGloss_Mat", (0.005, 0.005, 0.005, 1.0), 0.08
    )
    absorber = make_principled_material(
        "VA_ENV_DIAG_Absorber_Mat", (0.002, 0.002, 0.002, 1.0), 1.0
    )
    bright_a = make_emission_material(
        "VA_ENV_DIAG_BrightA_Mat", (1.0, 1.0, 1.0, 1.0), 3.0
    )
    bright_b = make_emission_material(
        "VA_ENV_DIAG_BrightB_Mat", (0.65, 0.72, 0.85, 1.0), 1.5
    )
    glass = make_glass_material("VA_ENV_DIAG_GlassProxy_Mat")

    add_cube(collection, "VA_ENV_DIAG_Road", (0.0, 0.0, -0.075), (30.0, 20.0, 0.15), road)
    add_cube(collection, "VA_ENV_DIAG_LeftBand", (-5.5, 0.5, 2.0), (0.08, 7.0, 3.2), bright_a)
    add_cube(collection, "VA_ENV_DIAG_RightBand", (5.0, 1.5, 1.7), (0.08, 3.5, 2.2), bright_b)
    add_cube(collection, "VA_ENV_DIAG_RightAbsorber", (5.2, -3.2, 1.7), (0.10, 3.0, 3.2), absorber)

    add_uv_sphere(collection, "VA_ENV_DIAG_Chrome", (-2.0, 4.2, 0.65), 0.65, chrome)
    add_uv_sphere(collection, "VA_ENV_DIAG_Grey18", (0.0, 4.2, 0.65), 0.65, grey)
    add_uv_sphere(collection, "VA_ENV_DIAG_BlackGloss", (2.0, 4.2, 0.65), 0.65, black_gloss)
    add_uv_sphere(collection, "VA_ENV_DIAG_GlassProxy", (4.0, 4.2, 0.65), 0.65, glass)

    add_area_light(
        collection,
        "VA_ENV_DIAG_OverheadFill",
        (0.0, 0.0, 8.0),
        (0.0, 0.0, 0.8),
        energy=700.0,
        size=7.0,
    )

    camera = add_camera(collection, (8.0, -11.0, 3.2), (0.0, 0.0, 1.0))
    bpy.context.scene["virtualauto_previous_camera"] = (
        bpy.context.scene.camera.name if bpy.context.scene.camera else ""
    )
    bpy.context.scene.camera = camera


def main() -> int:
    args = parse_args()
    if tuple(bpy.app.version[:3]) != BASELINE_VERSION:
        raise SystemExit(f"Expected Blender 5.0.1, got {bpy.app.version_string}")

    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    scene["virtualauto_previous_render_engine"] = scene.render.engine
    scene.render.engine = "CYCLES"
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100

    collection = create_owned_collection(args.replace_existing)
    make_world(scene)
    build(collection)

    if args.output:
        output = Path(args.output).expanduser().resolve()
        if output.suffix.lower() != ".blend":
            raise SystemExit("Output must use the .blend extension")
        output.parent.mkdir(parents=True, exist_ok=True)
        bpy.ops.wm.save_as_mainfile(filepath=str(output), check_existing=False)
        print(f"saved F40 glass diagnostic corridor: {output}")
    else:
        print("built F40 glass diagnostic corridor in the current file")

    print("status: P2-buildable; execution is not evidence until retained separately")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
