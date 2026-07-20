"""Create private, run-scoped workspaces outside the Git checkout."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,63}$")
STAGES = ("pkgtoolbox", "shadpkg", "driveclubfs", "rpk", "blender")


def initialise_workspace(
    directory: str | Path,
    *,
    run_id: str,
    repository: Path,
) -> dict[str, object]:
    """Create one isolated conversion run without touching source assets."""
    if not RUN_ID.fullmatch(run_id):
        raise ValueError(
            "Run ID must be 3-64 letters, digits, dots, underscores, or hyphens"
        )

    repository = repository.resolve()
    root = Path(directory).expanduser().resolve()
    try:
        root.relative_to(repository)
    except ValueError:
        pass
    else:
        raise ValueError("Private workspaces must remain outside the Git repository")

    runs = root / "runs"
    runs.mkdir(parents=True, exist_ok=True)
    run = runs / run_id
    try:
        run.mkdir()
    except FileExistsError as error:
        raise ValueError(f"Workspace run already exists: {run}") from error

    stages: dict[str, dict[str, str]] = {}
    for name in STAGES:
        input_path = run / name / "input"
        output_path = run / name / "output"
        input_path.mkdir(parents=True)
        output_path.mkdir()
        stages[name] = {
            "input": str(input_path),
            "output": str(output_path),
        }

    manifest: dict[str, object] = {
        "workspace_version": "1.0.0",
        "run_id": run_id,
        "created_at": datetime.now(UTC).isoformat(),
        "repository": str(repository),
        "run_root": str(run),
        "stages": stages,
        "policy": {
            "source_inputs_immutable": True,
            "outputs_private": True,
            "git_tracking_allowed": False,
            "automatic_deletion": False,
        },
    }
    destination = run / "workspace.json"
    destination.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return manifest
