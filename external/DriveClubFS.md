# DriveClubFS

## Provenance

- Upstream: <https://github.com/Nenkai/DriveClubFS>
- Default branch: `master`
- Verified upstream head: `836d5f09677dd7f30b92991a0f32e029487ae5cd`
- Verified on: 2026-07-20
- Integration state: record only; not yet a submodule
- License record: upstream `LICENSE.txt` contains the MIT license text, but its
  copyright line retains `[year] [fullname]` placeholders. Preserve that fact
  during any future license review.

## Purpose

The upstream README describes DriveClubFS as an unpacker for Evolution Studios'
filesystem, primarily DriveClub. It also documents extraction of binary
resources, XML, and textures from DriveClub `.rpk` resource packs.

## Documented inputs

- A paired `.ndx` index and `.dat` data file.
- DriveClub `.rpk` resource packs for supported resource extraction.
- The README lists DriveClub versions 1.00, 1.28, and NPXX51272
  alpha/prototype as supported.

## Documented outputs

- Files unpacked from the indexed filesystem.
- Extracted binary resources, XML, and textures from supported `.rpk` packs.

## Limitations and unknowns

- It is not documented as a Blender model importer or a complete vehicle
  geometry converter.
- The record does not establish lossless preservation of mesh semantics,
  materials, vertex attributes, rigs, or LOD relationships.
- Compatibility claims are upstream claims and have not yet been reproduced by
  VirtualAuto.
- Use only with data the operator is legally entitled to access.

## Intended role

Filesystem and resource extraction stage before semantic catalogue, format
analysis, and any Blender reconstruction.
