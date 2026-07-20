# PkgToolBox

## Provenance

- Upstream: <https://github.com/seregonwar/PkgToolBox>
- Default branch: `main`
- Verified upstream head: `eaba67631b88c686d681c790420d66b6e630e529`
- Verified on: 2026-07-20
- Integration state: record only; not yet a submodule
- License record: **unverified**. No root `LICENSE` file was present at the
  verified revision and the README did not declare a software license.

## Purpose

The upstream README describes a Python/PySide6 graphical tool for inspecting
and manipulating PS4 PKG files, including information, file navigation,
extraction, injection, header modification, and content dumping.

## Documented inputs

- PS4 `.pkg` files.
- Some features rely on `orbis-pub-cmd.exe` from the OpenOrbis toolchain.

## Documented outputs

- Selected files or complete content dumps from packages.
- Modified packages or package contents for explicitly supported operations.
- Human-readable information through the GUI, hex reader, and text reader.

## Limitations and unknowns

- The README contains internally mixed PS5 support status: it lists PS5
  navigation support as completed while also listing full PS5 PKG support as
  planned. Do not generalise its PS5 coverage.
- The documented environment is Python 3.13+, PySide6, PyInstaller, and for
  advanced operations OpenOrbis tooling. Cross-platform support is listed as
  planned.
- VirtualAuto has not tested package variants, encryption requirements, or the
  safety and fidelity of editing operations.
- Because licensing is unresolved, do not vendor, fork, or add this repository
  as a submodule until permission is clarified.
- Use only with packages the operator is legally entitled to access.

## Intended role

Candidate package inspection and controlled extraction front end. It is not
assumed to replace DriveClub-specific filesystem or resource decoding.
