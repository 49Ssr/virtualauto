# External tools

External repositories are treated as versioned research instruments. A tool
record documents purpose, provenance, inputs, outputs, limitations, licensing,
and the upstream revision evaluated by VirtualAuto.

The machine-readable lock distinguishes records from integrated instruments.
ShadPKG and 010GameTemplates are pinned submodules because their exact reviewed
commits contain MIT license files and have direct archaeology value. DriveClubFS
remains record-only because its MIT text retains placeholder authorship; PkgToolBox
remains blocked because no license file was found at its reviewed commit.

Clone integrated instruments with:

```text
git submodule update --init --recursive
```

A submodule pin establishes source provenance, not functional validation.

## Records

- [DriveClubFS](DriveClubFS.md)
- [PkgToolBox](PkgToolBox.md)
- [ShadPKG](ShadPKG.md)
- [010GameTemplates](010GameTemplates.md)
- [Machine-readable lock record](tools.lock.json)
