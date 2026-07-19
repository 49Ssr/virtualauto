# DriveClub source register

Sources are pinned where possible. A source entry records what it supports and
what it does not establish.

## SRC-DC-001 — DriveClubFS README

- Type: `SRC-UPSTREAM-DOC`
- Repository: <https://github.com/Nenkai/DriveClubFS>
- Pinned commit: `836d5f09677dd7f30b92991a0f32e029487ae5cd`
- File: <https://github.com/Nenkai/DriveClubFS/blob/836d5f09677dd7f30b92991a0f32e029487ae5cd/README.md>
- Supports: `.ndx + .dat` filesystem unpacking; RPK extraction claims for binary,
  XML, and textures; listed DriveClub build support; link to format templates.
- Does not establish: complete mesh, material, shader, hierarchy, or Blender
  conversion support.

## SRC-DC-002 — ResourceIdentifier and ResourceTypeId

- Type: `SRC-CODE`
- File: <https://github.com/Nenkai/DriveClubFS/blob/836d5f09677dd7f30b92991a0f32e029487ae5cd/DriveClubFS.Resources/ResourceIdentifier.cs>
- Supports: 64-bit identifier split; enumerated resource type IDs including
  stream format, vertex/index/pixel buffers, shader, material, mesh, hierarchy,
  GPU programs, attribute sets, vehicle custom data, top mips, and vehicle
  particles.
- Does not establish: internal payload semantics for those types.

## SRC-DC-003 — ResourceInfo

- Type: `SRC-CODE`
- File: <https://github.com/Nenkai/DriveClubFS/blob/836d5f09677dd7f30b92991a0f32e029487ae5cd/DriveClubFS.Resources/ResourceInfo.cs>
- Supports: resource size, offset, dependencies, names, and source-asset paths.
- Does not establish: whether all references or aliases are resolved across
  packs.

## SRC-DC-004 — ResourcePack

- Type: `SRC-CODE`
- File: <https://github.com/Nenkai/DriveClubFS/blob/836d5f09677dd7f30b92991a0f32e029487ae5cd/DriveClubFS.Resources/ResourcePack.cs>
- Supports: RPK header validation, resource information block parsing, name and
  source pools, root identity, possible required-pack names, and the currently
  implemented data decoders.
- Boundary: generic data construction is implemented for pixel buffers, BIN,
  XML, and top-mips resources in the inspected revision.

## SRC-DC-005 — DriveClubFS command-line extraction

- Type: `SRC-CODE`
- File: <https://github.com/Nenkai/DriveClubFS/blob/836d5f09677dd7f30b92991a0f32e029487ae5cd/DriveClubFS/Program.cs>
- Supports: filesystem commands; RPK traversal; explicit extraction cases for
  pixel buffers, BIN, and XML; DDS generation and pixel-format mapping.
- Boundary: the inspected switch does not export mesh, material, shader, or
  hierarchy resources semantically.

## SRC-DC-006 — 010GameTemplates

- Type: `SRC-UPSTREAM-DOC` and executable-format lead
- Repository: <https://github.com/Nenkai/010GameTemplates>
- Pinned commit: `7749b2b6d6f8c66b15e09464e61d2224df21b88a`
- Relevant files:
  - <https://github.com/Nenkai/010GameTemplates/blob/7749b2b6d6f8c66b15e09464e61d2224df21b88a/Evolution%20Studios/DriveClub/EvoIndexFile.bt>
  - <https://github.com/Nenkai/010GameTemplates/blob/7749b2b6d6f8c66b15e09464e61d2224df21b88a/Evolution%20Studios/DriveClub/EvoDatChunk.bt>
  - <https://github.com/Nenkai/010GameTemplates/blob/7749b2b6d6f8c66b15e09464e61d2224df21b88a/Evolution%20Studios/RPK_ResourcePack.bt>
- Supports: inspectable binary-template knowledge for Evolution Studios and
  DriveClub formats.
- Does not establish: complete support for every revision or semantic accuracy
  of every field. Templates require sample-based validation.

## SRC-DC-007 — ResHax DriveClub PS4 thread

- Type: `SRC-COMMUNITY`
- URL: <https://reshax.com/topic/719-driveclub-ps4/>
- Coverage: community work from 2024 through 2026 involving package/filesystem
  extraction, RPK resource IDs, mesh and stream experiments, Noesis scripts,
  UVs, normals, hierarchy, material names, index rebasing, and parser failures.
- Useful leads retained by VirtualAuto:
  - base/update merge behaviour may matter;
  - mesh resources may reference independent position, element, and index
    buffers;
  - observed strides and element layouts vary;
  - multiple UV streams exist in at least some investigated samples;
  - subset indices may require explicit rebasing;
  - hierarchy resources may supply part transforms;
  - material names expose state- and part-like tokens;
  - one control-flow error caused later meshes to be skipped.
- Does not establish: a stable specification, universal stride layout, verified
  normal encoding, complete material semantics, or production-ready converter.
- Rights boundary: the thread contains links to community-provided files and
  extracted material. VirtualAuto records the discussion only and does not copy
  or redistribute those assets.

## SRC-DC-008 — DriveClubFS license record

- Type: `SRC-CODE-METADATA`
- File: <https://github.com/Nenkai/DriveClubFS/blob/836d5f09677dd7f30b92991a0f32e029487ae5cd/LICENSE.txt>
- Supports: MIT license text is present.
- Anomaly: the copyright line retains `[year] [fullname]` placeholders.
- Boundary: the software licence does not grant rights to DriveClub assets.

## OBS-DC-USER-001 — Existing F40 export report

- Type: `OBS-USER`
- Retained artifact: none in repository
- Report: the user has an already-exported DriveClub-derived F40 that appears
  unusually detailed but has problematic UV behaviour.
- Supports: selecting the F40 as a diagnostic target and registering UV/export
  questions.
- Does not establish: original DriveClub UV semantics, source mesh topology,
  exporter correctness, material parameter fidelity, or package provenance.

## Source promotion rule

A community observation becomes a VirtualAuto claim only after:

1. the exact sample and build are registered;
2. source bytes and parser revision are retained privately;
3. the behaviour is reproduced;
4. alternative interpretations are tested;
5. evidence and observation records are committed;
6. the claim states its sample and version boundaries.
