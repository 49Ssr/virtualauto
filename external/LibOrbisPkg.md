# LibOrbisPkg

## Provenance

- Upstream: <https://github.com/OpenOrbis/LibOrbisPkg>
- Default branch: `master`
- Verified upstream revision: `c1caa3ba25097fe602c0d842a0357bf7037b0838`
- Verified on: 2026-07-22
- Integration state: pinned submodule at `external/vendor/LibOrbisPkg`
- License state: GNU LGPL version 3, declared by `README.md` and retained in
  `LICENSE.txt`

## Purpose

Independent PS4 PKG/PFS parsing library and command-line instrument. VirtualAuto
uses it as a comparison implementation for package-table inspection, digest
validation, and explicit encrypted-payload boundary detection.

## Documented inputs and outputs

- Input: one PS4 `.pkg`, PFS image, or related project file depending on the
  selected `PkgTool` verb.
- Read-only outputs include outer-entry listings and validation diagnostics.
- Write operations can extract package entries or PFS content when the required
  key material is available.

## Reproduced findings

At the pinned revision, `PkgTool` was published locally with .NET SDK 10.0.300
and run against the private DriveClub 1.28 package:

- the 42-entry outer package table was enumerated successfully;
- the complete PFS image digest, body digest, digest table, entry table groups,
  and package-header digest validated;
- the tool reported invalid content, game, header, major-parameter, and
  `NPBIND_DAT` digests under its validator rules;
- payload listing stopped with an explicit error because the PFS image is
  encrypted and no decryption key was supplied.

Those results establish useful structural evidence, not package authenticity.
The higher-level digest disagreement remains unresolved and must not be silently
relabelled as corruption while the whole PFS and body digests pass.

## Limitations

- The project primarily supports fake packages and packages for which a valid
  passcode or PFS keys are available. Its own source rejects encrypted PFS access
  when no key is supplied.
- A package-table listing is not a payload listing.
- The tool does not understand DriveClub RPK, mesh, material, or shader
  semantics.
- VirtualAuto does not commit packages, extracted content, passcodes, or keys.
- A submodule pin records the reviewed source; it does not make every command an
  approved production stage.

## Intended role

Pinned comparison instrument. VirtualAuto now owns the small, guarded operation
needed day-to-day: list the outer entry table and copy only entries explicitly
marked unencrypted. LibOrbisPkg remains available for independent validation and
future PFS work when lawful key material or an accessible installed root exists.
