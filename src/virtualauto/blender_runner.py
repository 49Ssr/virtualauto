"""Guarded headless Blender process orchestration."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from .doctor import blender_candidates
from .paths import repository_root, resolve_repository_output


def find_blender(explicit: str | Path | None = None) -> Path:
    if explicit:
        candidate = Path(explicit).expanduser().resolve()
        if not candidate.is_file():
            raise ValueError(f"Blender executable does not exist: {candidate}")
        return candidate
    candidates = blender_candidates()
    baseline: list[Path] = []
    for candidate in candidates:
        try:
            result = subprocess.run(
                [str(candidate), "--version"],
                capture_output=True,
                text=True,
                check=False,
                timeout=20,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        first_line = result.stdout.splitlines()[0] if result.stdout else ""
        if result.returncode == 0 and first_line.startswith("Blender 5.0.1"):
            baseline.append(candidate)
    if not baseline:
        raise ValueError("No Blender 5.0.1 executable was found")
    return baseline[0]


def run_blender_script(
    *,
    blender: Path,
    script: Path,
    script_args: list[str],
    scene: Path | None = None,
    cwd: Path,
    timeout: int = 180,
) -> subprocess.CompletedProcess[str]:
    command = [str(blender), "--background", "--factory-startup"]
    if scene:
        command.append(str(scene))
    # Blender evaluates command-line options in order. The error-code policy must
    # be active before the Python script executes or failures can return zero.
    command.extend(["--python-exit-code", "1", "--python", str(script), "--"])
    command.extend(script_args)
    result = subprocess.run(
        command,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stdout + "\n" + result.stderr).strip()
        raise RuntimeError(f"Blender command failed ({result.returncode}):\n{detail}")
    return result


def run_smoke(
    *,
    output_directory: str | Path,
    blender_path: str | Path | None = None,
    root: Path | None = None,
    overwrite: bool = False,
) -> dict[str, Path]:
    root = root or repository_root()
    blender = find_blender(blender_path)
    output = resolve_repository_output(root, output_directory)
    output.mkdir(parents=True, exist_ok=True)
    runtime = output / "runtime.json"
    inventory = output / "inventory.json"
    log = output / "smoke.txt"
    for target in (runtime, inventory, log):
        if target.exists() and not overwrite:
            raise ValueError(
                f"Smoke evidence already exists: {target.relative_to(root)}"
            )

    temporary_root = Path(tempfile.gettempdir()).resolve()
    temporary_scene = temporary_root / "virtualauto-blender-5.0.1-smoke.blend"
    create = run_blender_script(
        blender=blender,
        script=root / "blender/scripts/create_smoke_scene.py",
        script_args=["--output", str(temporary_scene), "--overwrite"],
        cwd=root,
    )
    capture_args = [
        "--id",
        "RUN-VA-BLENDER-SMOKE-001",
        "--output",
        runtime.relative_to(root).as_posix(),
    ]
    inventory_args = [
        "--id",
        "RPT-VA-BLENDER-SMOKE-001",
        "--output",
        inventory.relative_to(root).as_posix(),
    ]
    if overwrite:
        capture_args.append("--overwrite")
        inventory_args.append("--overwrite")
    capture = run_blender_script(
        blender=blender,
        scene=temporary_scene,
        script=root / "blender/scripts/capture_runtime_manifest.py",
        script_args=capture_args,
        cwd=root,
    )
    inspect = run_blender_script(
        blender=blender,
        scene=temporary_scene,
        script=root / "blender/scripts/asset_inventory.py",
        script_args=inventory_args,
        cwd=root,
    )
    log.write_text(
        "\n\n".join(
            (
                "[create_smoke_scene]\n" + create.stdout.strip(),
                "[capture_runtime_manifest]\n" + capture.stdout.strip(),
                "[asset_inventory]\n" + inspect.stdout.strip(),
            )
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return {"runtime": runtime, "inventory": inventory, "log": log}
