# 010GameTemplates

## Provenance

- Upstream: <https://github.com/Nenkai/010GameTemplates>
- Default branch: `main`
- Verified upstream head: `7749b2b6d6f8c66b15e09464e61d2224df21b88a`
- Verified on: 2026-07-20
- Integration state: record only; not yet a submodule
- License: MIT, as declared in the upstream `LICENSE` file

## Purpose

A collection of 010 Editor binary templates for multiple games and engines.
The upstream README includes Driveclub among the covered titles, and the
DriveClubFS README points to the repository's
`Evolution Studios/DriveClub` directory as format documentation.

## Documented inputs

- Binary files matching a provided template's intended format.
- 010 Editor or a compatible environment capable of running 010 binary
  templates.

## Documented outputs

- Structured interpretation of fields described by a selected template inside
  the editor.
- Format knowledge useful for independent parsers and forensic notes.

## Limitations and unknowns

- The repository is a heterogeneous template collection, not a unified
  conversion pipeline.
- A template's presence does not prove complete format coverage, support for
  every game revision, or semantic correctness for every field.
- It does not itself establish Blender-ready geometry or materials.
- VirtualAuto has not yet executed the Driveclub templates against a controlled
  sample.

## Intended role

Executable format documentation and hypothesis source for the archaeology
stage. Findings must be independently checked before becoming importer logic.
