# DriveClub operational pipeline

This pipeline turns a lawfully accessible DriveClub installation into a
catalogued private workspace. It does not currently decode vehicle meshes or
reconstruct Blender materials.

For the exact start-to-finish decision path, use the
[operator runbook](RUNBOOK.md).

## Stages

```text
lawful PS4 package or accessible installation
  -> package-access stage (manual; ShadPKG is not VirtualAuto-wrapped)
  -> DriveClubFS indexed-filesystem stage (guarded wrapper)
  -> RPK resource stage (blocked pending output-path hardening)
  -> VirtualAuto Blender archaeology stage
```

Working directories are under [`workspace/`](workspace/README.md). Their
contents are ignored by Git; only the contracts are tracked.

## Initial setup

```text
git submodule update --init --recursive
python -m pip install -e .
virtualauto doctor
virtualauto driveclub build
```

The pinned DriveClubFS project targets .NET 9. `build` requires a .NET 9 SDK,
not merely a runtime. Set `VIRTUALAUTO_DOTNET` when `dotnet` is not on `PATH`.

## Filesystem extraction

Place or privately link the directory containing `game.ndx` and its
`game*.dat` files at:

`workspace/driveclubfs/input/`

Then run:

```text
virtualauto driveclub list
virtualauto driveclub unpack
```

`list` is a mandatory safety preflight. It rejects absolute paths, traversal,
invalid Windows names, reserved device names, and case-insensitive collisions.
`unpack` repeats the preflight, requires an empty destination, retains upstream
logs, and records checksums for the input index/data files.

The default extracted root is:

`workspace/driveclubfs/output/filesystem/`

You may pass absolute private-storage paths with `--input` and `--output` rather
than copying a large installation into the repository checkout.

## Deliberately unavailable

The wrapper does not expose DriveClubFS `extract-rpk` or `extract-rpks` yet.
The reviewed upstream implementation writes beside its input and derives output
paths from resource names without a containment guard. VirtualAuto will add RPK
extraction only after establishing explicit input/output ownership and path
sanitisation.

ShadPKG remains a pinned external instrument, but its package/decryption claims
have not been reproduced by VirtualAuto. Use it only with data you are entitled
to access; no keys, packages, or extracted resources belong in Git.
