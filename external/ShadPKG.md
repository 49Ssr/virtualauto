# ShadPKG

## Provenance

- Upstream: <https://github.com/seregonwar/ShadPKG>
- Default branch: `main`
- Verified upstream head: `7a02c1e56b40477b26a660884deda1f3ca8d2eab`
- Verified on: 2026-07-20
- Integration state: record only; not yet a submodule
- License: MIT, as declared in the upstream README and `LICENSE` file

## Purpose

The upstream README describes a Windows C++ utility for analysing, decrypting,
and extracting PlayStation 4 PKG files, with key handling, logging, and
multi-threaded extraction.

## Documented inputs

- A PS4 `.pkg` path.
- An output directory.
- Building requires Windows 10/11 x64, Visual Studio 2022, Python 3.10+ for the
  build script, and Conan 2.x according to the README.

## Documented outputs

- Extracted file and directory trees.
- Console output and `debug_log.txt`.
- Unknown or unnamed entries exported as `entry_0x<ID>.bin`.

## Limitations and unknowns

- The README notes that patches and updates may intentionally omit files.
- Supported PKG categories and cryptographic claims are upstream claims; they
  have not yet been reproduced or security-audited by VirtualAuto.
- It is not a DriveClub resource decoder, geometry converter, or Blender
  importer.
- Use only with packages the operator is legally entitled to access.

## Intended role

Candidate package-analysis/extraction stage whose output may feed a
DriveClub-specific filesystem pipeline after independent validation.
