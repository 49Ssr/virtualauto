# DriveClub operational pipeline

This pipeline turns a lawfully accessible DriveClub installation into a
catalogued private workspace. It does not currently decode vehicle meshes or
reconstruct Blender materials.

For the exact start-to-finish decision path, use the
[operator runbook](RUNBOOK.md).

## Stages

```text
lawfully accessible numbered PKG fragments or complete package
  -> guarded structural inspection and byte-exact assembly
  -> package payload-access stage (ShadPKG is not VirtualAuto-wrapped)
  -> DriveClubFS indexed-filesystem stage (guarded wrapper)
  -> RPK resource stage (blocked pending output-path hardening)
  -> VirtualAuto Blender archaeology stage
```

Private run directories are created outside Git using the
[workspace contract](WORKSPACE.md).

## Initial setup

```text
git submodule update --init --recursive
python -m pip install -e .
virtualauto doctor
virtualauto driveclub build
```

The pinned DriveClubFS project targets .NET 9. `build` requires a .NET 9 SDK,
not merely a runtime. Set `VIRTUALAUTO_DOTNET` when `dotnet` is not on `PATH`.

## Package-fragment assembly

Numbered package fragments can first be inspected and assembled without
altering them:

```text
virtualauto pkg inspect --input D:\VirtualAutoWorkspace\runs\dc-f40-001\pkg\input
virtualauto pkg assemble --input D:\VirtualAutoWorkspace\runs\dc-f40-001\pkg\input --output D:\VirtualAutoWorkspace\runs\dc-f40-001\pkg\output\driveclub.pkg
```

This establishes container structure and byte continuity only. It does not
decrypt the payload or replace the need for a base installation when the PKG is
an update.

## Filesystem extraction

Create a unique private run, then place or link the accessible `game.ndx` and
`game*.dat` files into the generated DriveClubFS input boundary:

```text
virtualauto workspace init D:\VirtualAutoWorkspace --run-id dc-f40-001
virtualauto driveclub list --input D:\VirtualAutoWorkspace\runs\dc-f40-001\driveclubfs\input --output D:\VirtualAutoWorkspace\runs\dc-f40-001\driveclubfs\output\files.json
virtualauto driveclub unpack --input D:\VirtualAutoWorkspace\runs\dc-f40-001\driveclubfs\input --output D:\VirtualAutoWorkspace\runs\dc-f40-001\driveclubfs\output\filesystem
```

`list` is a mandatory safety preflight. It rejects absolute paths, traversal,
invalid Windows names, reserved device names, and case-insensitive collisions.
`unpack` repeats the preflight, requires an empty destination, retains upstream
logs, and records checksums for the input index/data files.

Inputs and outputs are explicit so a command cannot silently select an old run.
Large installations remain outside the repository checkout.

## Deliberately unavailable

The wrapper does not expose DriveClubFS `extract-rpk` or `extract-rpks` yet.
The reviewed upstream implementation writes beside its input and derives output
paths from resource names without a containment guard. VirtualAuto will add RPK
extraction only after establishing explicit input/output ownership and path
sanitisation.

ShadPKG remains a pinned external instrument, but its package/decryption claims
have not been reproduced by VirtualAuto. Use it only with data you are entitled
to access; no keys, packages, or extracted resources belong in Git.
