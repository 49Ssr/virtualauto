"""Repository path discovery without assuming a particular checkout location."""

from __future__ import annotations

import os
from pathlib import Path

MARKERS = ("pyproject.toml", "docs/PROJECT_DOCTRINE.md", "schemas")


def is_repository_root(path: Path) -> bool:
    return all((path / marker).exists() for marker in MARKERS)


def repository_root(start: Path | None = None) -> Path:
    configured = os.environ.get("VIRTUALAUTO_ROOT")
    if configured:
        candidate = Path(configured).expanduser().resolve()
        if not is_repository_root(candidate):
            raise ValueError(
                f"VIRTUALAUTO_ROOT is not a VirtualAuto checkout: {candidate}"
            )
        return candidate

    origins = [start or Path.cwd(), Path(__file__).resolve()]
    for origin in origins:
        candidate = origin.resolve()
        if candidate.is_file():
            candidate = candidate.parent
        for parent in (candidate, *candidate.parents):
            if is_repository_root(parent):
                return parent
    raise ValueError("Could not locate the VirtualAuto repository root")


def resolve_repository_output(root: Path, value: str | Path) -> Path:
    output = Path(value)
    if not output.is_absolute():
        output = root / output
    output = output.resolve()
    try:
        output.relative_to(root.resolve())
    except ValueError as error:
        raise ValueError(
            f"Output path must remain inside the repository: {output}"
        ) from error
    return output
