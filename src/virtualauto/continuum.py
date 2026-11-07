"""Build the Windows Continuum Flow variant from upstream plus a small patch."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

EXTRA_REQUIREMENTS = ("platformdirs==4.14.5", "typing_extensions==4.16.0")


def build(root: Path) -> Path:
    tools = json.loads((root / "external/tools.lock.json").read_text(encoding="utf-8"))[
        "tools"
    ]
    tool = next(item for item in tools if item["id"] == "EXT-CONTINUUM-FLOW")
    pin = tool["commit"]
    upstream = f"https://github.com/{tool['repository']}.git"
    work = root / "build/continuum-flow"
    checkout = work / "upstream"
    if not checkout.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--sparse",
                "--no-checkout",
                upstream,
                str(checkout),
            ],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(checkout), "fetch", "--depth=1", "origin", pin],
            check=True,
        )
    paths = subprocess.check_output(
        [
            "git",
            "-C",
            str(checkout),
            "ls-tree",
            "-r",
            "--name-only",
            pin,
            "--",
            "Internal",
            "Solver",
            "__init__.py",
            "blender_manifest.toml",
            "license.txt",
        ],
        text=True,
    ).splitlines()
    for name in ("baseline", "candidate"):
        destination = work / name
        for relative in paths:
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(
                subprocess.check_output(
                    ["git", "-C", str(checkout), "show", f"{pin}:{relative}"]
                )
            )

    candidate = work / "candidate"
    patch = root / "workflows/blender/continuum_flow/changes.patch"
    subprocess.run(
        [
            "git",
            "apply",
            f"--directory={candidate.relative_to(root).as_posix()}",
            str(patch),
        ],
        cwd=root,
        check=True,
    )
    manifest_path = candidate / "blender_manifest.toml"
    manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    version = manifest["version"]
    wheels = work / "wheels"
    wheels.mkdir(parents=True, exist_ok=True)
    requirements = [
        f"{Path(path).name.split('-')[0]}=={Path(path).name.split('-')[1]}"
        for path in manifest["wheels"]
        if path.startswith("./wheels/")
    ]
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "download",
            "--only-binary=:all:",
            "--no-deps",
            "--python-version",
            "313",
            "--implementation",
            "cp",
            "--abi",
            "cp313",
            "--platform",
            "win_amd64",
            "--dest",
            str(wheels),
            *requirements,
            *EXTRA_REQUIREMENTS,
        ],
        check=True,
    )
    for requirement in EXTRA_REQUIREMENTS:
        distribution, dependency_version = requirement.split("==")
        wheel = next(wheels.glob(f"{distribution}-{dependency_version}-*.whl"))
        manifest["wheels"].append(f"./wheels/{wheel.name}")
    text = manifest_path.read_text(encoding="utf-8")
    start = text.index("wheels = [")
    end = text.index("]", start) + 1
    wheel_list = (
        "wheels = [\n"
        + "".join(f"    {json.dumps(path)},\n" for path in manifest["wheels"])
        + "]"
    )
    manifest_path.write_text(text[:start] + wheel_list + text[end:], encoding="utf-8")
    tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    for relative in manifest["wheels"]:
        target = candidate / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if relative.startswith("./custom_wheels/"):
            target.write_bytes(
                subprocess.check_output(
                    ["git", "-C", str(checkout), "show", f"{pin}:{relative[2:]}"]
                )
            )
        else:
            target.write_bytes((wheels / target.name).read_bytes())
    changes = (
        f"Continuum Flow - VirtualAuto {version}\n"
        "Based on Lutz Rohlfing's Continuum Flow 0.4.0 at " + pin + ".\n"
        "Modified 2026-11-07 by VirtualAuto contributors, GPL-3.0-or-later.\n\n"
        "Changes: reuse OpenCL preview staging buffers; "
        "edit preview appearance during a bake; "
        "align VDB sequence playback with the requested start frame; "
        "limit exported frames to the requested duration; "
        "export evaluated meshes and load volumes without changing mode or selection; "
        "retain the chosen output material across bakes; "
        "reject surface voxels outside a triangle's geometric tolerance; "
        "skip animation timeline sampling for constant controls.\n"
        "The fluid-solve/combustion kernels and node identifiers are unchanged.\n"
        "Source changes and build instructions: "
        "VirtualAuto external/ContinuumFlow.md.\n"
        "Local development build. The bundled native VDB writer's source and licence "
        "have not been traced; this package is not cleared "
        "for public redistribution.\n"
    )
    (candidate / "VIRTUALAUTO_CHANGES.txt").write_text(changes, encoding="utf-8")
    archive = root / f"dist/continuum_flow-{version}-virtualauto-windows-x64.zip"
    archive.parent.mkdir(parents=True, exist_ok=True)
    files = paths + manifest["wheels"] + ["VIRTUALAUTO_CHANGES.txt"]
    with ZipFile(archive, "w", ZIP_DEFLATED) as package:
        for relative in files:
            package.write(candidate / relative, relative.lstrip("./"))
    return archive


def check(root: Path, blender: str) -> int:
    work = root / "build/continuum-flow"
    version = tomllib.loads(
        (work / "candidate/blender_manifest.toml").read_text(encoding="utf-8")
    )["version"]
    environment = os.environ.copy()
    environment["BLENDER_USER_RESOURCES"] = str(work / "package-profile")
    result = subprocess.run(
        [
            blender,
            "--background",
            "--factory-startup",
            "--python-exit-code",
            "1",
            "--python",
            str(root / "workflows/blender/continuum_flow/verify.py"),
            "--",
            "--work",
            str(root / "build/continuum-flow"),
        ],
        cwd=root,
        env=environment,
        check=False,
    ).returncode
    if result:
        return result
    return subprocess.run(
        [
            blender,
            "--background",
            "--factory-startup",
            "--python-exit-code",
            "1",
            "--python",
            str(root / "workflows/blender/continuum_flow/package_check.py"),
            "--",
            "--work",
            str(work),
            "--zip",
            str(root / f"dist/continuum_flow-{version}-virtualauto-windows-x64.zip"),
        ],
        cwd=root,
        env=environment,
        check=False,
    ).returncode
