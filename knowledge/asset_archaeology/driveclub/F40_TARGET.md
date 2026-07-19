# DriveClub Ferrari F40 first-target plan

The F40 is the first proposed end-to-end archaeology target because it exposes
many domains without requiring a modern active-aero or hybrid-control stack.

## Current evidence state

`OBS-USER`:

- an already-exported DriveClub-derived F40 appears substantially denser and
  more mechanically detailed than typical competing-title exports;
- the export appears relatively conventional in object, rig, and material-slot
  organization;
- its UV behaviour appears damaged, incomplete, or semantically mismatched.

No source file, screenshot, topology report, or retained measurement is present
in VirtualAuto. These observations define questions; they are not accepted
claims about the original asset.

## Why the F40 is useful

Potential coverage includes:

- highly reflective red body paint;
- black composite or polymer exterior regions;
- glass and transparent lamp assemblies;
- wheels, tyres, brake hardware, and exposed engine detail;
- interior and dashboard materials;
- panel gaps, vents, grilles, seals, and fasteners;
- hierarchy, movable panels, wheel transforms, and LOD relationships.

The target should reveal whether source fidelity is being lost at package,
resource, exporter, or Blender-import stage.

## Phase A — Register the existing export

Create an immutable `AST` record with:

- exact filename, format, checksum, and byte size;
- source and exporter information where known;
- object, mesh, polygon, vertex, material, UV, colour-attribute, armature, and
  animation counts;
- bounding box and apparent units;
- every custom property and unsupported data warning;
- no cleanup, welding, normal recalculation, or UV repair.

Capture a machine-readable Blender import report in a fresh 5.0.1 file.

## Phase B — Diagnose the existing export

Required diagnostics:

1. **Topology:** non-manifold edges, loose geometry, duplicate positions,
   degenerate faces, disconnected islands, and split-vertex statistics.
2. **Normals:** custom split-normal presence, geometric-normal disagreement,
   zero-length values, mirrored regions, and reflection-line behaviour.
3. **UVs:** all layers, finite values, bounds, island density, orientation,
   overlap, seams, and indexed-grid renders.
4. **Attributes:** every colour, tangent, skinning, and custom layer; do not
   discard unrecognized data.
5. **Materials:** exact slots, object assignments, names, texture paths, and
   values imported by the third-party exporter.
6. **Hierarchy:** parent graph, armature, pivots, transforms, and wheel or panel
   relationships.
7. **Geometry classes:** render, collision, interior, engine, glass, lamps,
   wheels, shadow/proxy, damage, and unknown.

This phase answers what the exported file contains, not what DriveClub originally
contained.

## Phase C — Acquire and catalogue original resources

When a lawful package or root installation is available:

- register base/update/build provenance;
- produce filesystem and RPK catalogues before model decoding;
- search resource names and dependency graphs for the F40 vehicle root;
- preserve every related mesh, material, shader, texture, hierarchy, custom
  data, and unknown dependency;
- compare original resource counts and relationships against the existing
  export.

The existing export becomes a comparison artifact, not a decoder specification.

## Phase D — Minimal semantic decoder

First decoder milestone:

- one selected render mesh;
- exact raw positions and indices;
- every referenced element stream preserved;
- submesh/material IDs retained;
- no normals or UVs guessed;
- deterministic intermediate output;
- byte-consumption and bounds report.

Second milestone:

- candidate normals and all UV-like streams exposed as named diagnostic
  attributes;
- hierarchy transform applied through a reversible stage;
- material dependency graph exported without recreating shaders.

## Phase E — Blender qualification

The imported semantic intermediate must pass:

- source count and checksum correspondence;
- valid indices and non-degenerate triangle threshold;
- expected vehicle bounds without arbitrary axis stretching;
- all source UV streams accessible;
- normal candidates independently toggleable;
- hierarchy and pivot sanity under wheel rotation and movable-panel tests;
- no hidden modifier or automatic cleanup required for correct placement;
- fresh-file deterministic import.

## Phase F — Physical reconstruction

Only after semantic qualification:

- identify actual part/material families;
- compare game material intent with retained names, parameters, textures, and
  in-game reference;
- replace rather than blindly copy engine approximations;
- use the Automotive Body R&D master for paint, composites, glass, metals,
  polymers, rubber, lamps, contamination, and repair states;
- preserve an unmodified recovered-material branch for comparison.

## Initial experiment backlog

| Proposed ID | Question |
| --- | --- |
| `EXP-DC-F40-IMPORT-001` | What data survives a clean Blender 5.0.1 import of the existing export? |
| `EXP-DC-F40-UV-001` | Which UV streams exist and which material regions, if any, do they explain? |
| `EXP-DC-F40-NORMAL-001` | Are visible shading failures caused by source normals, exporter decoding, transforms, or geometry? |
| `EXP-DC-F40-RESOURCE-001` | Which original RPK resources form the minimum F40 dependency graph? |
| `EXP-DC-F40-INDEX-001` | How are submesh indices based and rebased across selected F40 resources? |
| `EXP-DC-F40-HIERARCHY-001` | Which hierarchy and matrix convention reconstructs part placement? |
| `EXP-DC-F40-MATERIAL-001` | Which resource fields select materials, shaders, textures, and state variants? |

IDs remain proposals until schema-backed manifests are committed.

## Stop conditions

Pause production cleanup when:

- original and exported geometry cannot yet be distinguished;
- a decoder consumes unexplained bytes;
- a UV or normal repair would destroy alternative semantics;
- hierarchy placement requires arbitrary per-part corrections;
- material reconstruction is based only on names;
- no retained evidence can falsify the chosen interpretation.
