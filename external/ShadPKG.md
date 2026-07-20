# ShadPKG

## Provenance

- Upstream: <https://github.com/seregonwar/ShadPKG>
- Default branch: `main`
- Verified upstream head: `7a02c1e56b40477b26a660884deda1f3ca8d2eab`
- Verified on: 2026-07-20
- Integration state: pinned submodule at `external/vendor/ShadPKG`
- License state: conflicting declarations. The root README and `LICENSE` say
  MIT, while the reviewed `main.cpp` and more than one hundred reviewed C/C++
  files declare `GPL-2.0-or-later` through SPDX headers.

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
- The README's legacy two-positional-argument invocation does not match the
  reviewed program's current command grammar, which begins with an `extract`
  verb. Use source-level CLI help as the current upstream description.
- The reviewed RIF branch validates a supplied RIF and then reaches an explicit
  TODO where integration with PKG decryption is not implemented. Do not infer
  that the RIF option is operational merely because it is accepted by the CLI.
- PFS names are combined into extraction paths in the reviewed implementation;
  no complete canonical output-containment proof has been established by this
  audit. VirtualAuto therefore does not wrap or automatically execute ShadPKG.
- Supported PKG categories and cryptographic claims are upstream claims; they
  have not yet been reproduced or security-audited by VirtualAuto.
- It is not a DriveClub resource decoder, geometry converter, or Blender
  importer.
- Use only with packages the operator is legally entitled to access.

## Intended role

Pinned source-level research instrument whose output may eventually feed a
DriveClub-specific filesystem pipeline after license clarification, output-path
hardening, and independent validation. Pinning does not authorize execution or
validate its cryptographic, safety, or compatibility claims.
