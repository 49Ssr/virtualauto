# Blender implementation

Executable Blender work is organised by responsibility. Each artifact must
declare its Blender version, inputs, outputs, coordinate spaces, ownership,
diagnostics, performance assumptions, and validation status.

- [`addon/virtualauto_blender/`](addon/virtualauto_blender/) contains the first
  artist-facing development add-on.
- [`scripts/`](scripts/README.md) contains Blender-hosted headless entrypoints.
- [Verified Blender 5.0.1 Windows toolchain record](toolchains/BLD-BLENDER-501-WINDOWS-X64.json)

`virtualauto blender-smoke` is the first accepted structural path. It creates a
temporary original fixture; it does not use or validate an automotive asset.

## Execution boundary

`src/virtualauto/` contains no `bpy` import. The ordinary CLI can validate
schemas, inspect paths, register sources, record evidence, and orchestrate tools
on a machine without Blender. Blender API calls belong only in scripts launched
inside a separate headless Blender process or, in future, a Blender add-on.

## Artist interface

Headless execution is the reproducibility layer, not the intended look-
development interface. The development add-on provides one real vertical slice:
a 3D View sidebar that summarizes the active mesh and exports the same class of
non-destructive structural inventory used by the headless workflow.

It remains deliberately narrow. It does not compile materials or claim to
recover DriveClub parameters. A distributable Blender Extension package is also
deferred until the repository's own software licence is explicitly selected;
the current code is tested as a repository-hosted development add-on.

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
