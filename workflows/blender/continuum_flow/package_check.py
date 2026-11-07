# SPDX-License-Identifier: GPL-3.0-or-later
"""Install the actual ZIP in an isolated factory Blender profile."""

import argparse
import importlib
import json
import sys
from pathlib import Path

import addon_utils
import bpy

parser = argparse.ArgumentParser()
parser.add_argument("--work", type=Path, required=True)
parser.add_argument("--zip", type=Path, required=True)
args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])
directory = args.work / "package-profile/extensions/variant"
directory.mkdir(parents=True, exist_ok=True)
bpy.ops.preferences.extension_repo_add(
    name="VirtualAuto package check",
    type="LOCAL",
    use_custom_directory=True,
    custom_directory=str(directory),
)
repo = next(
    r
    for r in bpy.context.preferences.extensions.repos
    if r.name == "VirtualAuto package check"
)
answer = bpy.ops.extensions.package_install_files(
    filepath=str(args.zip),
    repo=repo.module,
    enable_on_install=True,
    overwrite=True,
)
assert answer == {"FINISHED"}, answer
name = "bl_ext." + repo.module + ".continuum_flow"
assert addon_utils.check(name) == (True, True), addon_utils.check(name)
module = importlib.import_module(name + ".Internal.Core.solver.solver_status")
devices = module.refresh_opencl_devices()["GPU"]
assert devices, "Installed extension did not find an OpenCL GPU"
report = {
    "blender": bpy.app.version_string,
    "archive": args.zip.name,
    "extension_enabled": True,
    "gpu_devices": [d["device_name"] for d in devices],
    "profile": str(args.work / "package-profile"),
}
(args.work / "package_verification.json").write_text(
    json.dumps(report, indent=2), encoding="utf-8"
)
print(json.dumps(report), flush=True)
