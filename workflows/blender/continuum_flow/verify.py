# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise the real OpenCL solver and Blender VDB importer in factory Blender."""

import argparse
import copy
import importlib
import importlib.util
import json
import struct
import sys
import time
from pathlib import Path
from zipfile import ZipFile

import bpy
from mathutils import Vector


def check_pose_export(work, geometry_export):
    bpy.ops.mesh.primitive_cube_add(location=(7, 8, 9))
    source = bpy.context.object
    source.hide_render = True
    source.modifiers.new("Evaluated subdivision", "SUBSURF").levels = 1
    original_vertices = len(source.data.vertices)
    original_uvs = list(source.data.uv_layers.keys())
    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = source.evaluated_get(depsgraph)
    mesh = evaluated.to_mesh()
    mesh.calc_loop_triangles()
    expected = [
        tuple(
            component for index in tri.vertices for component in mesh.vertices[index].co
        )
        for tri in mesh.loop_triangles
    ]
    evaluated.to_mesh_clear()
    bpy.ops.object.armature_add()
    rig = bpy.context.object
    bpy.ops.object.mode_set(mode="POSE")
    selected = set(bpy.context.selected_objects)
    counts = (len(bpy.data.objects), len(bpy.data.meshes))
    geometry_export.export_object_as_local_stl(source, work / "pose-check", depsgraph)
    raw = (work / "pose-check" / f"{source.name}.stl").read_bytes()
    assert struct.unpack_from("<I", raw, 80)[0] == len(expected)
    records = list(struct.iter_unpack("<12fH", raw[84:]))
    assert len(records) == len(expected)
    assert all(
        abs(actual - target) < 1e-6
        for record, triangle in zip(records, expected, strict=True)
        for actual, target in zip(record[3:12], triangle, strict=True)
    )
    assert bpy.context.mode == "POSE"
    assert bpy.context.object == rig
    assert set(bpy.context.selected_objects) == selected
    assert counts == (len(bpy.data.objects), len(bpy.data.meshes))
    assert len(source.data.vertices) == original_vertices
    assert list(source.data.uv_layers.keys()) == original_uvs
    bpy.ops.object.mode_set(mode="OBJECT")
    return rig


def check_triangle_voxelization(work, context, queue, voxelizer):
    import numpy as np
    import pyopencl as cl

    triangle = np.array([[[0, 0, 0], [1, 0, 0], [0, 1, 0]]], dtype=np.float32)
    reports = {}
    for name in ("baseline", "candidate"):
        source = (work / name / "Solver/Kernel/OpenCL/voxelise_mesh.cl").read_text()
        program = cl.Program(context, source).build(options=["-cl-fast-relaxed-math"])
        kernel = program.surface
        grid = voxelizer.voxelize_triangles(context, queue, kernel, triangle, 0.1)
        values = np.empty(grid["shape"], dtype=np.uint8)
        cl.enqueue_copy(queue, values, grid["mask"]).wait()
        samples = {}
        for label, point in (
            ("inside", (0.2, 0.2, 0)),
            ("outside_triangle", (0.9, 0.9, 0)),
            ("near_edge", (0.5, 0.55, 0)),
        ):
            index = tuple(np.rint((np.array(point) - grid["origin"]) / 0.1).astype(int))
            samples[label] = int(values[index])
        assert samples["inside"] == samples["near_edge"] == 1
        assert samples["outside_triangle"] == (1 if name == "baseline" else 0)
        reports[name] = samples
        if name == "candidate":
            for points, expected_nonempty in (
                (triangle[:, ::-1, :].copy(), True),
                (np.zeros_like(triangle), False),
            ):
                other = voxelizer.voxelize_triangles(
                    context, queue, kernel, points, 0.1
                )
                result = np.empty(other["shape"], dtype=np.uint8)
                cl.enqueue_copy(queue, result, other["mask"]).wait()
                assert bool(result.any()) == expected_nonempty
    return reports


def smoke_material():
    material = bpy.data.materials.new("VDB visibility check")
    material.use_nodes = True
    tree = material.node_tree
    tree.nodes.clear()
    info = tree.nodes.new("ShaderNodeVolumeInfo")
    density = tree.nodes.new("ShaderNodeMath")
    density.operation = "MULTIPLY"
    density.inputs[1].default_value = 10.0
    absorb = tree.nodes.new("ShaderNodeVolumeAbsorption")
    absorb.inputs["Color"].default_value = (0.5, 0.05, 0.02, 1)
    output = tree.nodes.new("ShaderNodeOutputMaterial")
    tree.links.new(info.outputs["Density"], density.inputs[0])
    tree.links.new(density.outputs[0], absorb.inputs["Density"])
    tree.links.new(absorb.outputs[0], output.inputs["Volume"])
    return material


def check_visible_volume(work, volume_object):
    scene = bpy.context.scene
    bpy.ops.object.mode_set(mode="OBJECT")
    for obj in scene.objects:
        if obj.type in {"MESH", "VOLUME"}:
            obj.hide_render = obj != volume_object
    camera_data = bpy.data.cameras.new("VDB test camera")
    camera = bpy.data.objects.new(camera_data.name, camera_data)
    scene.collection.objects.link(camera)
    camera.location = (4, -6, 2)
    camera.rotation_euler = (
        (Vector((0, 0, 0.6)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    )
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = 3.0
    scene.camera = camera
    scene.world.use_nodes = True
    background = scene.world.node_tree.nodes.get("Background")
    background.inputs["Color"].default_value = (1, 1, 1, 1)
    background.inputs["Strength"].default_value = 1.0
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 4
    scene.cycles.seed = 0
    scene.render.resolution_x = 64
    scene.render.resolution_y = 64
    scene.render.resolution_percentage = 100
    scene.render.image_settings.media_type = "IMAGE"
    scene.render.image_settings.file_format = "PNG"
    scene.render.use_compositing = False
    pixels = []
    for visible in (True, False):
        volume_object.hide_render = not visible
        path = work / f"volume-visible-{visible}.png"
        scene.render.filepath = str(path)
        bpy.ops.render.render(write_still=True)
        image = bpy.data.images.load(str(path), check_existing=False)
        pixels.append(list(image.pixels))
        bpy.data.images.remove(image)
    difference = sum(abs(a - b) for a, b in zip(*pixels, strict=True)) / len(pixels[0])
    assert difference > 0.0001, f"VDB did not change the rendered image: {difference}"
    volume_object.hide_render = False
    return difference


def run(work):
    (work / "verification.json").unlink(missing_ok=True)
    candidate = work / "candidate"
    runtime = work / "runtime"
    if not runtime.exists():
        runtime.mkdir()
        for wheel in [
            *(candidate / "wheels").glob("*.whl"),
            *(candidate / "custom_wheels").glob("*.whl"),
        ]:
            with ZipFile(wheel) as package:
                package.extractall(runtime)
    sys.path.insert(0, str(runtime))
    spec = importlib.util.spec_from_file_location(
        "va_continuum_check",
        candidate / "__init__.py",
        submodule_search_locations=[str(candidate)],
    )
    addon = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = addon
    spec.loader.exec_module(addon)
    addon.register()
    prefix = spec.name
    export = importlib.import_module(prefix + ".Internal.Core.export.export_config")
    renderer = importlib.import_module(prefix + ".Internal.Core.volume_renderer")
    status = importlib.import_module(prefix + ".Internal.Core.solver.solver_status")
    manager = importlib.import_module(
        prefix + ".Internal.Core.solver.solver_manager"
    ).solver_manager
    loader = importlib.import_module(prefix + ".Internal.Core.load_result")
    animation_proxy = importlib.import_module(prefix + ".Internal.UI.animation_proxy")
    geometry_export = importlib.import_module(
        prefix + ".Internal.Core.export.export_geometry"
    )
    voxelizer = importlib.import_module(prefix + ".Solver.Kernel.voxelise_mesh")
    main = importlib.import_module(prefix + ".Solver.General.main").main
    devices = status.refresh_opencl_devices()["GPU"]
    assert devices, "No OpenCL GPU found"
    gpu_index = next(
        (i for i, device in enumerate(devices) if "NVIDIA" in device["device_name"]), 0
    )
    import pyopencl as cl

    device_info = devices[gpu_index]
    device = cl.get_platforms()[device_info["platform_index"]].get_devices(
        device_type=cl.device_type.GPU
    )[device_info["device_index"]]
    context = cl.Context([device])
    voxelization_check = check_triangle_voxelization(
        work, context, cl.CommandQueue(context), voxelizer
    )
    turbulence_spec = importlib.util.spec_from_file_location(
        "va_cf_turbulence_test", Path(__file__).with_name("turbulence_check.py")
    )
    turbulence_test = importlib.util.module_from_spec(turbulence_spec)
    turbulence_spec.loader.exec_module(turbulence_test)
    turbulence_report = turbulence_test.run(work, context, cl.CommandQueue(context))
    solid_spec = importlib.util.spec_from_file_location(
        "va_cf_solid_test", Path(__file__).with_name("solid_check.py")
    )
    solid_test = importlib.util.module_from_spec(solid_spec)
    solid_spec.loader.exec_module(solid_test)
    solid_report = solid_test.run(work, context, cl.CommandQueue(context))
    preview_spec = importlib.util.spec_from_file_location(
        "va_cf_preview_test", Path(__file__).with_name("preview_check.py")
    )
    preview_test = importlib.util.module_from_spec(preview_spec)
    preview_spec.loader.exec_module(preview_test)
    buffer_check = preview_test.run(work, context, cl.CommandQueue(context))

    scene = bpy.context.scene
    scene.frame_start = 41
    scene.frame_end = 47
    scene.render.fps = 24
    tree = bpy.data.node_groups.new(
        "Continuum verification", "CONTINUUM_FLOW_NODE_TREE"
    )
    types = {
        name: tree.nodes.new("CONTINUUM_FLOW_" + name.upper() + "_NODE")
        for name in (
            "domain",
            "physics",
            "simulation",
            "geometry",
            "source",
            "viewer",
            "output",
        )
    }
    domain, simulation, viewer, output = [
        types[k] for k in ("domain", "simulation", "viewer", "output")
    ]
    domain.lx = 2
    domain.ly = 2
    domain.lz = 3
    domain.resolution = 0.1
    simulation.solver_backend = "GPU"
    simulation.gpu_devices = tuple(
        i == gpu_index for i in range(status.MAX_SELECTABLE_DEVICES)
    )
    simulation.start_frame = 41
    simulation.end_frame = 47
    simulation.cfl = 3
    viewer.live_preview = False
    output.output_path = str(work / "check-cache")
    output.export_t = True
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12, ring_count=8, radius=0.25, location=(0, 0, 0.4)
    )
    types["geometry"].source_object = bpy.context.object
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0.20, 0, 0.4))
    wall = bpy.context.object
    wall.name = "Moving collision wall"
    wall.scale = (0.10, 0.8, 0.8)
    wall.keyframe_insert(data_path="location", frame=41)
    wall.location.x = 0.40
    wall.keyframe_insert(data_path="location", frame=47)
    wall_geometry = tree.nodes.new("CONTINUUM_FLOW_GEOMETRY_NODE")
    wall_geometry.source_object = wall
    wall_obstacle = tree.nodes.new("CONTINUUM_FLOW_OBSTACLE_NODE")
    tree.links.new(wall_geometry.outputs["Geometry"], wall_obstacle.inputs["Geometry"])
    tree.links.new(wall_obstacle.outputs["Obstacle"], simulation.inputs["Obstacles"])
    for name, value in (("fuel", 10.0), ("smoke", 10.0), ("temperature", 900.0)):
        scene[animation_proxy.node_proxy_key(types["source"], name)] = value
    for source, out_name, target, in_name in (
        ("domain", "Domain", "simulation", "Domain"),
        ("physics", "Physics", "simulation", "Physics"),
        ("geometry", "Geometry", "source", "Geometry"),
        ("source", "Source", "simulation", "Source"),
        ("simulation", "Result", "viewer", "Result"),
        ("simulation", "Result", "output", "Result"),
    ):
        tree.links.new(types[source].outputs[out_name], types[target].inputs[in_name])

    # Editing display controls during an active job must update the current preview.
    renderer.simulation_reference = (tree.name, simulation.name)
    viewer.live_preview = True
    status.bake_running = True
    viewer.preview_smoke_density = 7.25
    viewer.preview_flame_color = (0.7, 0.2, 0.1)
    assert renderer.smoke_density == 7.25
    assert abs(renderer.flame_color[0] - 0.7) < 1e-6
    status.bake_running = False
    viewer.live_preview = False

    sampled_frames = []

    def record_frame(scene, _depsgraph=None):
        sampled_frames.append(scene.frame_current)

    bpy.app.handlers.frame_change_post.append(record_frame)
    try:
        constant_animation = export.build_animations(types["source"], 41, 47)
    finally:
        bpy.app.handlers.frame_change_post.remove(record_frame)
    assert constant_animation == ({}, {}) and not sampled_frames

    config = export.build_config_dict(context=bpy.context, simulation_node=simulation)
    assert config["simulation"]["sources"][0]["smoke"]["value"] > 0
    rig = check_pose_export(work, geometry_export)
    directory, config = export.export_config_dict(config)
    start = time.perf_counter()
    output_module = importlib.import_module(prefix + ".Solver.Kernel.output")
    with solid_test.observe_outputs(output_module) as solid_outputs:
        main(config)
    assert sum(r["solid_cells"] for r in solid_outputs) > 0
    bake_seconds = time.perf_counter() - start
    files = sorted(Path(directory).glob("*.vdb"))
    assert len(files) == simulation.end_frame - simulation.start_frame + 1, len(files)
    baseline_spec = importlib.util.spec_from_file_location(
        prefix + ".Internal.Core.baseline_load_result",
        work / "baseline/Internal/Core/load_result.py",
    )
    baseline_loader = importlib.util.module_from_spec(baseline_spec)
    baseline_spec.loader.exec_module(baseline_loader)
    baseline_result = baseline_loader.VDBResultManager()
    baseline_result.load_bake(
        directory, start_frame_index=41, simulation_node=simulation
    )
    assert baseline_result.volume_object.data.frame_start == 1
    baseline_timeline_start = baseline_result.volume_object.data.frame_start
    material = smoke_material()
    output.volume_material = material
    bpy.context.view_layer.objects.active = rig
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    rig.select_set(True)
    bpy.ops.object.mode_set(mode="POSE")
    selection = set(bpy.context.selected_objects)
    result = loader.VDBResultManager()
    result.load_bake(
        directory,
        start_frame_index=41,
        simulation_node=simulation,
        material=output.volume_material,
    )
    assert bpy.context.mode == "POSE" and bpy.context.object == rig
    assert set(bpy.context.selected_objects) == selection
    assert result.volume_object.data.materials[0] == material
    volume = result.volume_object.data
    assert volume.frame_start == 41
    assert volume.frame_duration == len(files)
    frame_paths = []
    for frame, expected in (
        (41, files[0]),
        (42, files[1]),
        (40 + len(files), files[-1]),
    ):
        scene.frame_set(frame)
        evaluated = result.volume_object.evaluated_get(
            bpy.context.evaluated_depsgraph_get()
        ).data
        evaluated.grids.load()
        path = Path(evaluated.grids.frame_filepath)
        assert path.name == expected.name, (frame, path.name, expected.name)
        assert len(evaluated.grids) >= 2
        assert "density" in [grid.name for grid in evaluated.grids]
        assert (
            min(
                result.volume_object.evaluated_get(
                    bpy.context.evaluated_depsgraph_get()
                ).dimensions
            )
            > 0
        )
        frame_paths.append([frame, path.name])

    zero_start = loader.VDBResultManager()
    zero_start.load_bake(
        directory,
        start_frame_index=0,
        simulation_node=simulation,
        material=output.volume_material,
    )
    assert zero_start.volume_object.data.materials[0] == material
    scene.frame_set(0)
    zero_volume = zero_start.volume_object.evaluated_get(
        bpy.context.evaluated_depsgraph_get()
    ).data
    zero_volume.grids.load()
    assert Path(zero_volume.grids.frame_filepath).name == files[0].name
    scene.frame_set(47)
    render_difference = check_visible_volume(work, result.volume_object)

    # Cancellation is measured on the real worker after warm-up, not mocked.
    cancelled = copy.deepcopy(config)
    cancelled["simulation"]["settings"]["simulation_length"] = 1000
    cancelled["simulation"]["outputs"][0]["fields"] = {}
    flag = work / "cancel-check.flag"
    flag.unlink(missing_ok=True)
    cancelled.setdefault("meta", {})["cancel_flag_path"] = str(flag)
    job = manager.start_job(cancelled)
    started = time.monotonic()
    heartbeat = 0
    while int(manager.get_stats().get("frame", 0)) < 3:
        if manager.get_job_result(job) is not None:
            raise AssertionError("Cancellation test ended before cancellation request")
        assert time.monotonic() - started < 40, (
            "GPU worker did not start within the test limit"
        )
        heartbeat += 1
        time.sleep(0.01)
    requested = time.perf_counter()
    flag.write_text("1")
    answer = None
    while answer is None:
        assert time.perf_counter() - requested < 20, (
            "Cancellation exceeded the test limit"
        )
        time.sleep(0.01)
        answer = manager.get_job_result(job)
    cancel_seconds = time.perf_counter() - requested
    assert answer["success"], answer
    flag.unlink()
    report = {
        "blender": bpy.app.version_string,
        "gpu": devices[gpu_index]["device_name"],
        "bake_seconds": bake_seconds,
        "baked_frames": len(files),
        "resolution_metres": domain.resolution,
        "timeline_files": frame_paths,
        "preview_appearance_updates": True,
        "baseline_timeline_start": baseline_timeline_start,
        "frame_zero_verified": True,
        "pose_export_and_import_verified": True,
        "material_assignment_verified": True,
        "rendered_volume_pixel_difference": render_difference,
        "preview_buffers": buffer_check,
        "triangle_voxelization": voxelization_check,
        "turbulence_field": turbulence_report,
        "solid_scalar_fields": solid_report,
        "moving_obstacle_cache_outputs": solid_outputs,
        "constant_controls_frame_updates": len(sampled_frames),
        "cancel_seconds": cancel_seconds,
        "worker_heartbeat_ticks": heartbeat,
        "scope": (
            "Factory scene; small GPU bake and native VDB loading. "
            "No claim about large production playback."
        ),
    }
    (work / "verification.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report), flush=True)
    addon.unregister()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])
    try:
        run(args.work)
    except BaseException:
        import traceback

        traceback.print_exc()
        sys.stdout.flush()
        raise SystemExit(1) from None
