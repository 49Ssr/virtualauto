# Blender implementation

Executable Blender work is organised by responsibility. Each artifact must
declare its Blender version, inputs, outputs, coordinate spaces, ownership,
diagnostics, performance assumptions, and validation status.

- [`node_groups/`](node_groups/README.md)
- [`geometry_nodes/`](geometry_nodes/README.md)
- [`scripts/`](scripts/README.md)
- [`diagnostics/`](diagnostics/README.md)
- [`assets/`](assets/README.md)
- [Verified Blender 5.0.1 Windows toolchain record](toolchains/BLD-BLENDER-501-WINDOWS-X64.json)

`virtualauto blender-smoke` is the first accepted structural path. It creates a
temporary original fixture; it does not use or validate an automotive asset.

## Execution boundary

`src/virtualauto/` contains no `bpy` import. The ordinary CLI can validate
schemas, inspect paths, register sources, record evidence, and orchestrate tools
on a machine without Blender. Blender API calls belong only in scripts launched
inside a separate headless Blender process or, in future, a Blender add-on.

## Artist interface roadmap

Headless execution is the reproducibility layer, not the intended look-
development interface. A future add-on should remain a thin Blender adapter:

1. display project and material configuration with source/confidence labels;
2. call tested builders rather than duplicate their math in UI operators;
3. expose Beauty and diagnostic modes in the viewport;
4. write explicit project overrides and evidence records;
5. keep `bpy` isolated from the portable core package.

No add-on is claimed yet. In particular, "pull F40 parameters" cannot exist
until lawful source parameters or measured/calibrated replacements have been
registered and a material compiler has an accepted contract.
