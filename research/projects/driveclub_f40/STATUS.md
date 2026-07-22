# DriveClub Ferrari F40 archaeology status

## State

`active research; 1.28 update acquired, base installation pending`

## Current baseline

- Blender production baseline: `5.0.1`
- Original package or installed root: a private European `CUSA00003` 1.28
  update has been structurally validated and byte-exactly assembled; the base
  package or installed root is not yet available
- Existing third-party export: reported in private possession; not registered or
  committed
- Retained evidence: none
- Archaeology plan: [F40 target plan](../../asset_archaeology/driveclub/F40_TARGET.md)
- Private-source registration command: implemented and unit-tested
- Blender structural inventory: executed successfully on a synthetic 5.0.1 fixture
- DriveClubFS, ShadPKG, and 010GameTemplates: pinned as exact-commit
  submodules; DriveClubFS has not yet been validated against an accessible
  indexed DriveClub filesystem
- DriveClubFS build: reproduced from the pinned source with .NET SDK 9.0.316;
  build warnings were retained as upstream findings, not silently treated as
  VirtualAuto validation
- Split-PKG inspector/assembler: implemented and tested; the real five-part
  1.28 update passed consecutive-index, single-header, uniform-chunk,
  declared-size, and immutable-source checks, then produced a checksummed
  19,191,300,096-byte private package
- Indexed-filesystem wrapper: path-preflight and output verification are
  implemented and unit-tested; no real DriveClub filesystem has been supplied

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

## Package findings

`OBS-INSTRUMENT`, retained in the private run workspace rather than Git:

- content ID: `EP9000-CUSA00003_00-XXXXXXXDRIVECLUB`;
- `APP_VER`: `01.28`;
- `TARGET_APP_VER`: `01.27`;
- `CATEGORY`: `gp`;
- combined and header-declared byte size: `19,191,300,096`;
- combined SHA-256:
  `1fb9d39c3e596f9fae0ecf53a6bad54ff5775c60e8c9a30ac67a9819c1da10e0`.

These establish local byte custody and update identity. They do not establish
distribution authenticity, payload decryption, a complete base installation,
or permission to redistribute the package.

## Blockers

- matching base package or an installed-and-updated root remains necessary;
- package payload access has not passed VirtualAuto's containment and
  reproducibility requirements;
- exact existing-export provenance and exporter are unknown;
- no fresh Blender 5.0.1 forensic report exists;
- original mesh/material/hierarchy resources have not been catalogued;
- DriveClub mesh and element-stream semantics remain incomplete.

## Runtime configuration boundary

- Machine-readable F40 project manifest: not implemented
- Material or asset compiler: not implemented
- Panel Colour Offset: unknown; no source or calibration record
- Bumper Gloss Mismatch: unknown; no source or calibration record
- Geometry attributes written from project overrides: none

This Markdown status is deliberately not an executable parameter source. A
future manifest may drive a compiler only after each value has units,
provenance, confidence, ownership, and one of the states `OEM-disclosed`,
`measured`, `calibrated`, or `artist-default`. Until then, the CLI must leave
these values unresolved rather than inventing plausible defaults.

## Next smallest actions

1. Register the existing export as an immutable private source asset with
   checksum and import provenance.
2. Run a non-destructive Blender 5.0.1 inventory of objects, mesh counts,
   attributes, UV layers, material slots, hierarchy, and custom normals.
3. Capture indexed-grid views for every UV layer without editing the mesh.
4. When original files are available, catalogue the F40 resource dependency
   graph before writing a model converter.

The operational tooling is ready for step 1 and for a guarded filesystem unpack
once an accessible `game.ndx`/`game*.dat` set is available. No F40 record has
been fabricated: private packages, exports, and extracted data remain absent
from this checkout.

## Changelog

### 2026-07-22

- Validated the five numbered fragments of the European 1.28 update without
  modifying them.
- Read the retained package header and `param.sfo`, identifying the package as
  an update from 1.27 to 1.28 rather than a base installation.
- Assembled a new private package through the guarded PKG stage and retained
  fragment/output hashes plus the operation manifest outside Git.
- Kept package payload extraction blocked pending a reviewed, contained access
  path and a matching base/root source.

### 2026-07-20

- Established the F40 as VirtualAuto's first DriveClub archaeology target.
- Recorded the existing export only as an unverified user observation.
- Deferred material recreation and geometry cleanup until source semantics can
  be separated from exporter damage.
- Added a tested private-source registrar and non-mutating Blender 5.0.1
  inventory path without claiming that either has run on the F40.
- Pinned DriveClubFS and reproduced its .NET 9 build without claiming a real
  game-data extraction.
- Added private per-stage workspaces plus guarded filesystem listing and unpack
  commands.
- Consolidated repository navigation into `research/`, `workflows/`, `lab/`, and
  `dev/`; reran the Blender 5.0.1 synthetic smoke path and corrected custom
  property enumeration against the live Blender API.
- Defined the non-fabrication boundary for future project overrides and material
  compilation; no F40 optical parameter was promoted from status prose.
