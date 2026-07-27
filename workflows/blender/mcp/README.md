# Live Blender control

VirtualAuto uses Blender's official MCP connector as a pinned transport and
keeps project policy, evidence, and future typed automotive operations in this
repository. The upstream connector is not copied into VirtualAuto.

## Exact upstream

[`upstream.lock.json`](upstream.lock.json) records the release, source commit,
download checksums, compatibility boundary, and security assumptions. The
current live target is Blender 5.2.0 LTS because the official extension requires
Blender 5.1 or newer. The existing 5.0.1 headless evidence remains historical
and is not silently relabelled as live-MCP validation.

## Local installation

1. Download the add-on URL in the lock and verify its SHA-256.
2. Install it through Blender's extension installer and enable online access.
3. Install the matching server from the pinned source tag into an isolated
   environment. The default Windows location expected by
   [`launch_server.py`](launch_server.py) is
   `%USERPROFILE%\VirtualAutoTools\blender-mcp\venv`.
4. Restart Blender with a saved working copy. The upstream extension auto-starts
   its loopback bridge on port 9876 unless its preferences were changed.
5. Run the read-only handshake:

   ```text
   python workflows/blender/mcp/probe_bridge.py
   ```

To verify the complete stdio MCP path rather than only the Blender socket, run
[`smoke_client.py`](smoke_client.py) with the isolated server environment's
Python while Blender is listening.

The launcher also accepts `VIRTUALAUTO_BLENDER_MCP_SERVER` when the isolated
server lives elsewhere.

## Codex policy

The project-scoped [Codex configuration](../../../.codex/config.toml) exposes
interactive Blender tools, including raw Blender Python, but excludes background
`*_for_cli` tools. Raw execution is broad authority: Blender's upstream
`WeakSandboxForLLM` is explicitly not a security boundary.

For every new working session:

1. Open a copy, not the only authoritative `.blend`.
2. Save an incremental checkpoint.
3. Prove the bridge with the read-only probe and path check.
4. Inspect relevant objects, materials, images, and current selection.
5. Make scoped mutations with named targets and retain before/after evidence.
6. Save only after the intended result is verified.

The bridge is infrastructure, not proof that a generated material, node graph,
or geometry edit is physically or artistically correct.
