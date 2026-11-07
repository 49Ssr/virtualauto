# Blender workflows

Version-specific node, Geometry Nodes, scripting, import, diagnostics, and
validation knowledge.

Compatibility is recorded per implementation. The original structural fixture
was tested in Blender 5.0.1; the current Continuum Flow Windows build was
checked in Blender 5.2.3 LTS. See the [Blender tools index](../../workflows/blender/README.md)
for the relevant entry point. Each implementation must state its tested Blender
version, render engine and remaining limits.

Node-contract schema `2.0.0` requires every input to declare whether it
participates in a procedural system. Procedural controls, coordinates, and
fields must carry an explicit coordinate contract defining mode, semantic,
scale basis, and transform ownership. UV, named-attribute, and tangent modes
also name their source attribute. This prevents an apparently complete node
specification from hiding object/UV/panel-flow assumptions.

The `1.x` contract had no accepted implementation records in this repository;
the sole example was migrated in place. Any future external `1.x` record must
be migrated deliberately rather than silently interpreted as `2.0.0`.
