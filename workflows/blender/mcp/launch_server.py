"""Launch the separately installed official Blender MCP server.

This file deliberately imports no Blender or MCP package. It keeps optional
live-control dependencies outside VirtualAuto's ordinary CLI environment.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def server_candidates() -> list[Path]:
    configured = os.environ.get("VIRTUALAUTO_BLENDER_MCP_SERVER")
    values = [Path(configured).expanduser()] if configured else []
    home = Path.home()
    if os.name == "nt":
        values.append(
            home
            / "VirtualAutoTools"
            / "blender-mcp"
            / "venv"
            / "Scripts"
            / "blender-mcp.exe"
        )
    else:
        values.append(
            home
            / ".local"
            / "share"
            / "virtualauto"
            / "blender-mcp"
            / "bin"
            / "blender-mcp"
        )
    return values


def main() -> int:
    for candidate in server_candidates():
        resolved = candidate.resolve()
        if resolved.is_file():
            os.execv(str(resolved), [str(resolved), *sys.argv[1:]])
    searched = "\n  - ".join(str(path) for path in server_candidates())
    print(
        "The pinned Blender MCP server is not installed. Searched:\n  - "
        f"{searched}\nSee workflows/blender/mcp/README.md.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
