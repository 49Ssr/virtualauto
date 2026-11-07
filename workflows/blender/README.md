# Blender tools

Start with the tool for the task. Compatibility and test results belong to
each workflow; the historical Blender 5.0.1 fixture is not the current version
requirement for every tool.

- [`addon/virtualauto_blender/`](addon/virtualauto_blender/) contains the first
  artist-facing development add-on.
- [`scripts/`](scripts/README.md) contains Blender-hosted headless entrypoints.
- [Continuum Flow variant](../../external/ContinuumFlow.md) contains the small
  source patch, repeatable Windows package build and Blender/OpenCL checks.
- [`mcp/`](mcp/README.md) pins and operates the official live Blender bridge.
- [Verified Blender 5.0.1 Windows toolchain record](toolchains/BLD-BLENDER-501-WINDOWS-X64.json)

`virtualauto blender-smoke` runs the original Blender 5.0.1 structural smoke
test. It creates a temporary synthetic scene, not a smoke/fluid simulation.
For fire and smoke simulation use `virtualauto continuum build` and the
Continuum record above; its Windows package was checked in Blender 5.2.3 LTS.

## Execution boundary

`src/virtualauto/` contains no `bpy` import. The ordinary CLI can validate
schemas, inspect paths, register sources, record evidence, and orchestrate tools
on a machine without Blender. Blender API calls belong only in scripts launched
inside Blender, either in a separate background process, through the live
connector, or in an add-on.

## Artist interface

Headless execution is the reproducibility layer, not the intended look-
development interface. The development add-on provides one real vertical slice:
a 3D View sidebar that summarizes the active mesh and exports the same class of
non-destructive structural inventory used by the headless workflow.

It remains deliberately narrow. It does not compile materials or claim to
recover DriveClub parameters. A distributable Blender Extension package is also
deferred until the repository's own software licence is explicitly selected;
the current code is tested as a repository-hosted development add-on.

## Live control

Interactive Blender 5.2 control uses the separately installed official Blender
MCP connector. It does not import `bpy` into the ordinary VirtualAuto CLI. The
first connection to any asset is read-only, and broad edits require a saved
working copy plus a named checkpoint. See the [live-control runbook](mcp/README.md).

## Future shader and Geometry Nodes ownership

- Shader-node builders own optical transport and must follow node contracts.
- Geometry Nodes owns geometry-derived process, edge, drape, and confidence
  fields when an accepted implementation exists.
- Diagnostic modes must expose intermediate fields without replacing formal
  AOV or contribution-render evidence.
- Small original regression `.blend` files, when justified, live only under
  `dev/tests/fixtures/blender/` with LFS and provenance.

"Pull F40 parameters" cannot exist until lawful source parameters or
measured/calibrated replacements are registered and a compiler has an accepted
contract.
