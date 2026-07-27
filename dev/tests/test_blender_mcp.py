"""Contract tests for the live Blender bridge boundary."""

from __future__ import annotations

import json
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class BlenderMcpContractTests(unittest.TestCase):
    def test_upstream_is_commit_and_checksum_pinned(self) -> None:
        lock_path = ROOT / "workflows/blender/mcp/upstream.lock.json"
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
        self.assertRegex(lock["upstream"]["commit"], r"^[0-9a-f]{40}$")
        self.assertRegex(lock["release"]["addon_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(
            lock["release"]["source_archive_sha256"], r"^[0-9a-f]{64}$"
        )
        self.assertNotEqual(
            lock["release"]["source_archive_sha256"], "0" * 64
        )

    def test_codex_scope_excludes_background_file_tools(self) -> None:
        config_path = ROOT / ".codex/config.toml"
        config = tomllib.loads(config_path.read_text(encoding="utf-8"))
        tools = config["mcp_servers"]["blender"]["enabled_tools"]
        self.assertIn("execute_blender_code", tools)
        self.assertFalse(any(name.endswith("_for_cli") for name in tools))

    def test_probe_source_is_declared_read_only(self) -> None:
        probe = (ROOT / "workflows/blender/mcp/probe_bridge.py").read_text(
            encoding="utf-8"
        )
        self.assertIn("READ_ONLY_PROBE", probe)
        self.assertNotIn("bpy.ops.wm.save", probe)
        self.assertNotIn("bpy.data.objects.remove", probe)


if __name__ == "__main__":
    unittest.main()
