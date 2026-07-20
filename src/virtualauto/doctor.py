"""Non-mutating environment diagnostics for the VirtualAuto toolchain."""

from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from .paths import repository_root


def command_output(command: list[str], cwd: Path) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, str(error)
    output = (result.stdout or result.stderr).strip()
    return result.returncode == 0, output


def blender_candidates() -> list[Path]:
    values: list[Path] = []
    configured = os.environ.get("VIRTUALAUTO_BLENDER")
    if configured:
        values.append(Path(configured))
    discovered = shutil.which("blender")
    if discovered:
        values.append(Path(discovered))
    if os.name == "nt":
        values.extend(Path("C:/Program Files/Blender Foundation").glob("*/blender.exe"))
        values.extend(Path("C:/tmp").glob("blender-5.0.1*/**/blender.exe"))
    unique: list[Path] = []
    seen: set[Path] = set()
    for value in values:
        resolved = value.expanduser().resolve()
        if resolved not in seen and resolved.is_file():
            unique.append(resolved)
            seen.add(resolved)
    return unique


def diagnose(root: Path | None = None) -> dict[str, object]:
    root = root or repository_root()
    git_ok, git_version = command_output(["git", "--version"], root)
    lfs_ok, lfs_version = command_output(["git", "lfs", "version"], root)
    sdk_ok, sdk_output = command_output(["dotnet", "--list-sdks"], root)
    sdk_lines = [line for line in sdk_output.splitlines() if line.strip()]
    sdk_ok = sdk_ok and bool(sdk_lines)

    blender_results: list[dict[str, object]] = []
    for candidate in blender_candidates():
        ok, output = command_output([str(candidate), "--version"], root)
        first_line = output.splitlines()[0] if output else ""
        blender_results.append(
            {
                "path": str(candidate),
                "available": ok,
                "version_line": first_line,
                "baseline_5_0_1": ok and first_line.startswith("Blender 5.0.1"),
            }
        )

    submodule_ok, submodules = command_output(["git", "submodule", "status"], root)
    return {
        "virtualauto_root": str(root),
        "host": platform.platform(),
        "python": sys.version.split()[0],
        "git": {"available": git_ok, "version": git_version},
        "git_lfs": {"available": lfs_ok, "version": lfs_version},
        "dotnet_sdk": {"available": sdk_ok, "versions": sdk_lines},
        "blender": blender_results,
        "baseline_blender_available": any(
            item["baseline_5_0_1"] for item in blender_results
        ),
        "submodules": {
            "query_succeeded": submodule_ok,
            "status": [line for line in submodules.splitlines() if line.strip()],
        },
        "canonical_master_available": (
            root / "knowledge/automotive_materials/Automotive_Body_RnD_Master.md"
        ).is_file(),
        "master_index_available": (
            root / "generated/automotive_master.index.json"
        ).is_file(),
    }
