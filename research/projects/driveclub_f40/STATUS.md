# DriveClub Ferrari F40 archaeology status

## State

`active research; sparse 1.28 filesystem inspected, matching base required`

## Current baseline

- Blender production baseline: `5.0.1`
- Original package or installed root: a private European `CUSA00003` 1.28
  update and a separate 1.28-labelled full-size container have been inspected;
  its extracted indexed filesystem is a sparse patch/repack composition and
  still requires the matching base contribution
- Existing third-party export: reported in private possession; not registered or
  committed
- Retained evidence: none
- Archaeology plan: [F40 target plan](../../asset_archaeology/driveclub/F40_TARGET.md)
- Private-source registration command: implemented and unit-tested
- Blender structural inventory: executed successfully on a synthetic 5.0.1 fixture
- DriveClubFS, ShadPKG, LibOrbisPkg, and 010GameTemplates: pinned as exact-commit
  submodules; a temporary, uncommitted DriveClubFS diagnostic patch read the
  accessible index far enough to expose the sparse-overlay failure mode
- DriveClubFS build: reproduced from the pinned source with .NET SDK 9.0.316;
  build warnings were retained as upstream findings, not silently treated as
  VirtualAuto validation
- Split-PKG inspector/assembler: implemented and tested; the real five-part
  1.28 update passed consecutive-index, single-header, uniform-chunk,
  declared-size, and immutable-source checks, then produced a checksummed
  19,191,300,096-byte private package
- Outer-package stage: implemented and tested; the real package yielded 39
  unencrypted outer entries with per-file SHA-256 records, while three encrypted
  entries and the PFS payload were explicitly skipped
- Indexed-filesystem wrapper: path-preflight and output verification are
  implemented and unit-tested; the new read-only structural inspector has run
  against a real filesystem and classified it without extracting payloads

## Sparse-filesystem findings

`OBS-INSTRUMENT`, retained outside Git; observed 2026-07-22:

- the extracted root contains `game.ndx`, `game.chc`, and 88 split DAT files;
- the version-4300 `DATX` index declares 8,018 records, of which 1,135 carry a
  nonzero logical size;
- all 43 DAT indices referenced by active records are present as files, but 441
  active records cross one or more zero-sized logical chunks;
- 39 parsed DAT files use a zeroed `DATA` sentinel, and both expected index
  sentinels are zeroed;
- the reusable VirtualAuto inspector therefore classifies the set as
  `overlay_or_repack_requires_base`, not as a complete extractable filesystem.

File count and apparent byte size were misleading here: the split-DAT tables
encode missing base contribution inside files that still exist. This result is
structural evidence of an incomplete base/patch composition, not proof of bad
decryption and not an authenticity judgment about the package source.

## F40 resource evidence from the sparse overlay

`OBS-INSTRUMENT`, private partial output; no resource payload is committed:

- a valid `Resource PacK file` header associated with the Ferrari F40 was found
  in the logical stream represented by `game448.dat`;
- its table names `ferrari_f40.evomeshes`, `ferrari_f40.def`,
  `ferrari_f40.hkx`, original authoring paths, and body, window, lamp,
  dashboard, and detail textures;
- 144 structurally readable resource records were catalogued before the sparse
  stream became incomplete: 76 vertex buffers, 37 pixel buffers, 26 stream
  formats, 3 index buffers, 1 material, and 1 unresolved record;
- many referenced resource ranges extend into absent base chunks, so this is a
  dependency/format breakthrough rather than a complete model extraction.

The resource table confirms that the original asset is materially richer than
the third-party FBX export. It does not yet establish individual vertex
semantics, usable UV streams, shader behaviour, or manufacturer-accurate
material values.

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

## Package-tool observations

`OBS-INSTRUMENT`, reproduced on 2026-07-22:

- ShadPKG `sfo-info` agreed with the VirtualAuto package identity.
- ShadPKG `pfs-info` crashed with access violation `0xC0000005` before listing
  files. Source review found unchecked invalid-RSA-result and missing-PFSC-magic
  paths that can feed invalid pointer arithmetic.
- LibOrbisPkg enumerated all 42 outer entries and validated the full PFS image,
  package body, digest table, entry groups, and package-header digest.
- LibOrbisPkg disagreed with five higher-level digests. This is retained as an
  unresolved validator/package-format discrepancy rather than silently treated
  as package corruption.
- LibOrbisPkg refused payload enumeration because the PFS is encrypted and no
  decryption key was supplied.
- VirtualAuto copied 39 unencrypted outer entries and skipped `.image_key`,
  `nptitle.dat`, and `npbind.dat` as encrypted. The accessible set includes
  `param.sfo`, PlayGo metadata for 96 chunks, update notes, images, delta tables,
  and trophy containers.

## Blockers

- matching `CUSA00003` base package or an installed-and-updated root remains
  necessary; the sparse 1.28 filesystem cannot reconstruct unchanged base
  chunks by itself;
- package payload access is blocked by encryption/key availability, not by the
  five-part assembly; the matching base or an accessible installed root remains
  the practical next source;
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
4. Compose a private base-plus-1.28 filesystem, rerun `driveclub inspect`, and
   require `complete_for_index` before listing or unpacking.
5. Catalogue the complete F40 RPK dependency graph before writing a model
   converter; preserve every unknown vertex and material field.

The operational tooling is ready for step 1. Filesystem unpack remains blocked
until a composed base-plus-update set passes the structural inspector. No F40
record has been fabricated: private packages, exports, partial RPK data, and
extracted assets remain absent from this checkout.

## Changelog

### 2026-07-22

- Inspected the new 1.28-labelled package and its accessible filesystem without
  committing private data.
- Identified sparse split-DAT chunks and classified the set as a patch/repack
  overlay requiring matching base content.
- Recovered a genuine partial F40 RPK table and a 144-record resource catalogue;
  stopped short of claiming model extraction because payload ranges cross
  absent base chunks.
- Added a pure-Python, read-only filesystem classifier so this condition is
  detected before DriveClubFS listing or extraction.

- Validated the five numbered fragments of the European 1.28 update without
  modifying them.
- Read the retained package header and `param.sfo`, identifying the package as
  an update from 1.27 to 1.28 rather than a base installation.
- Assembled a new private package through the guarded PKG stage and retained
  fragment/output hashes plus the operation manifest outside Git.
- Built and tested pinned ShadPKG; retained its successful SFO result, PFS crash,
  and source-level failure analysis without running its write extractor.
- Built and tested pinned LibOrbisPkg as an independent parser; retained both
  its successful whole-PFS/body validation and its higher-level digest
  disagreements.
- Added a VirtualAuto-owned, containment-checked outer-entry extractor and ran
  it on the real package. Encrypted entries and the PFS remain untouched.

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
