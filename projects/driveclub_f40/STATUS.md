# DriveClub Ferrari F40 archaeology status

## State

`active research; source acquisition pending`

## Current baseline

- Blender production baseline: `5.0.1`
- Original package or installed root: not currently registered
- Existing third-party export: reported in private possession; not registered or
  committed
- Retained evidence: none
- Archaeology plan: [F40 target plan](../../knowledge/asset_archaeology/driveclub/F40_TARGET.md)
- Private-source registration command: implemented and unit-tested
- Blender structural inventory: executed successfully on a synthetic 5.0.1 fixture
- ShadPKG and 010GameTemplates: pinned as exact-commit submodules; not yet
  validated against a lawful DriveClub sample

## Direct user observations

`OBS-USER`, no repository artifact yet:

- the DriveClub-derived F40 export appears to have a substantial polygon and
  mechanical-detail advantage over typical competing-title exports;
- object, rig, and material-slot organization appears surprisingly conventional;
- UV behaviour appears incorrect, incomplete, or disconnected from the intended
  game material system.

These reports do not establish whether the fault lies in the original resource,
third-party exporter, missing material metadata, stream selection, transforms,
or Blender import.

## Current interpretation space

Possible causes of the UV symptom include:

1. the exporter selected the wrong UV stream;
2. several UV streams or per-material transforms were flattened;
3. the original shader used object/world coordinates for some effects;
4. vertex attributes or material parameters selected mapping behaviour;
5. topology or vertex-stream alignment was damaged during export;
6. the supplied file combines render, collision, LOD, or state meshes without
   their original semantic graph.

No cause is preferred until the existing export is registered and diagnosed.

## Blockers

- lawful package or root installation must be sourced again;
- exact existing-export provenance and exporter are unknown;
- no fresh Blender 5.0.1 forensic report exists;
- original mesh/material/hierarchy resources have not been catalogued;
- DriveClub mesh and element-stream semantics remain incomplete.

## Next smallest actions

1. Register the existing export as an immutable private source asset with
   checksum and import provenance.
2. Run a non-destructive Blender 5.0.1 inventory of objects, mesh counts,
   attributes, UV layers, material slots, hierarchy, and custom normals.
3. Capture indexed-grid views for every UV layer without editing the mesh.
4. When original files are available, catalogue the F40 resource dependency
   graph before writing a model converter.

The operational tooling is ready for step 1. No F40 record has been fabricated:
the private export and original package/root remain absent from this checkout.

## Changelog

### 2026-07-20

- Established the F40 as VirtualAuto's first DriveClub archaeology target.
- Recorded the existing export only as an unverified user observation.
- Deferred material recreation and geometry cleanup until source semantics can
  be separated from exporter damage.
- Added a tested private-source registrar and non-mutating Blender 5.0.1
  inventory path without claiming that either has run on the F40.
