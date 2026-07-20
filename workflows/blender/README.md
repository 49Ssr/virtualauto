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
