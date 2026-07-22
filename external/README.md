# External tools

External repositories are treated as versioned research instruments. A tool
record documents purpose, provenance, inputs, outputs, limitations, licensing,
and the upstream revision evaluated by VirtualAuto.

The machine-readable lock distinguishes records from integrated instruments.
DriveClubFS, ShadPKG, LibOrbisPkg, and 010GameTemplates are exact-commit
submodules.
DriveClubFS is integrated with its placeholder MIT authorship explicitly marked
as an unresolved anomaly because it is the central filesystem instrument and is
used only behind VirtualAuto-owned guards. PkgToolBox remains blocked because no
license file was found at its reviewed commit.

ShadPKG is present as a pinned source-level research reference, not an approved
executable dependency. Its root MIT declarations conflict with widespread
`GPL-2.0-or-later` SPDX headers in the reviewed source, and its extraction output
boundary has not yet been proven safe by VirtualAuto. LibOrbisPkg is the
independent, LGPL-3.0 comparison instrument used to validate package structure
and confirm encrypted-payload boundaries.

Clone integrated instruments with:

```text
git submodule update --init --recursive
```

A submodule pin establishes source provenance, not functional validation.

## Records

- [DriveClubFS](DriveClubFS.md)
- [PkgToolBox](PkgToolBox.md)
- [ShadPKG](ShadPKG.md)
- [LibOrbisPkg](LibOrbisPkg.md)
- [010GameTemplates](010GameTemplates.md)
- [Machine-readable lock record](tools.lock.json)
