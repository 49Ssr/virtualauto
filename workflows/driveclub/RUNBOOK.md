# DriveClub operator runbook

This runbook distinguishes what VirtualAuto can execute now from stages that
remain research-only. Use only packages and installations you are entitled to
access. Never commit game data, keys, credentials, or extracted assets.

## 1. Identify the starting point

| Available source | Start here |
| --- | --- |
| Accessible root containing `game.ndx` and `game*.dat` | DriveClubFS stage |
| Older root containing an embedded-index `game.dat` | DriveClubFS stage |
| `.pkg` only | Package-access stage; currently manual and unvalidated |
| Third-party FBX/OBJ export only | Register it as a private source and run Blender inventory; it cannot prove original semantics |

ShadPKG is pinned for source-level study, but VirtualAuto does not execute it.
Its license declarations conflict, its RIF branch contains an explicit TODO,
and this audit has not established canonical containment for all extracted
paths. PkgToolBox remains record-only because no upstream license was found at
the verified pin.

## 2. Initialize the instruments

From the repository root:

```text
git submodule update --init --recursive
python -m pip install -e .
virtualauto doctor
```

Install a .NET 9 SDK or point `VIRTUALAUTO_DOTNET` at a private/local SDK, then:

```text
virtualauto driveclub build
```

The build must report `build/external/DriveClubFS/DriveClubFS.dll`. The command
verifies the exact submodule commit before compiling.

## 3. Create a private run and supply the indexed filesystem

Create the utility-specific boundaries outside the repository:

```text
virtualauto workspace init D:\VirtualAutoWorkspace --run-id dc-f40-001
```

Place or link the accessible files into the generated `driveclubfs/input`
directory, or pass another absolute `--input` path. A modern input is
expected to resemble:

```text
game.ndx
game000.dat
game001.dat
...
```

Do not rename or edit the source files. The older embedded-index form uses
`game.dat`.

## 4. Preflight before extraction

```text
virtualauto driveclub list --input D:\VirtualAutoWorkspace\runs\dc-f40-001\driveclubfs\input --output D:\VirtualAutoWorkspace\runs\dc-f40-001\driveclubfs\output\files.json
```

This parses the upstream listing and rejects absolute paths, traversal,
ambiguous separators, invalid Windows names, reserved names, case-insensitive
collisions, and missing indexed data files. It does not extract payloads.

## 5. Unpack the filesystem

```text
virtualauto driveclub unpack --input D:\VirtualAutoWorkspace\runs\dc-f40-001\driveclubfs\input --output D:\VirtualAutoWorkspace\runs\dc-f40-001\driveclubfs\output\filesystem
```

The destination must be absent or empty and must not overlap the input tree.
The wrapper checks listed output size against free space, records source hashes,
runs the pinned tool, verifies every expected path and byte size, rejects
unexpected files, and retains logs plus manifests under `_virtualauto/`.

Do not use `--skip-checksum-verification` unless a documented experiment
requires it. Older formats may not contain checksums, and upstream can disable
that check internally; the manifest records the request rather than claiming a
verification the tool did not perform.

## 6. What the result is—and is not

A successful filesystem unpack establishes only that the indexed payload tree
was reproduced under the wrapper's structural checks. It does not establish:

- correct RPK resource interpretation;
- recovered mesh, material, UV, tangent, rig, or LOD semantics;
- a Blender-ready model;
- manufacturer-accurate paint;
- permission to redistribute extracted assets.

The next operational target is a guarded RPK catalogue/extractor with explicit
output ownership. Until that exists, keep selected `.rpk` inputs under the
private run's `rpk/input/` boundary and do not invoke the upstream bulk RPK
extractors through VirtualAuto.
