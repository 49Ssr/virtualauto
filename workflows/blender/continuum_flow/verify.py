# SPDX-License-Identifier: GPL-3.0-or-later
"""Exercise the real OpenCL solver and Blender VDB importer in factory Blender."""

import argparse
import copy
import importlib
import importlib.util
import json
import sys
import time
from pathlib import Path
from zipfile import ZipFile

import bpy


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

    config = export.build_config_dict(context=bpy.context, simulation_node=simulation)
    assert config["simulation"]["sources"][0]["smoke"]["value"] > 0
    directory, config = export.export_config_dict(config)
    start = time.perf_counter()
    main(config)
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
    result = loader.VDBResultManager()
    result.load_bake(directory, start_frame_index=41, simulation_node=simulation)
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
    zero_start.load_bake(directory, start_frame_index=0, simulation_node=simulation)
    scene.frame_set(0)
    zero_volume = zero_start.volume_object.evaluated_get(
        bpy.context.evaluated_depsgraph_get()
    ).data
    zero_volume.grids.load()
    assert Path(zero_volume.grids.frame_filepath).name == files[0].name

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
        "preview_buffers": buffer_check,
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
