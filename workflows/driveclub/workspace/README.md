# Private DriveClub workspace

Each named utility owns an `input/` and `output/` boundary. The contents are
ignored locally and must never be committed.

| Stage | Input | Output | Current status |
| --- | --- | --- | --- |
| `shadpkg` | Lawfully accessible `.pkg` | Accessible package filesystem | Research-only; not wrapped |
| `driveclubfs` | `game.ndx`/`game.dat` and `game*.dat` | Indexed filesystem tree | Guarded VirtualAuto wrapper |
| `rpk` | Selected `.rpk` plus dependencies/top-mips | Resource catalogue/payloads | Blocked pending hardening |
| `blender` | Semantic intermediate and lawful derived data | `.blend`, reports, renders | Future archaeology stage |

Prefer immutable source inputs. Start each conversion in an empty output
directory, and retain generated manifests beside the outputs.

These boundaries are deliberate custody points, not a requirement to copy every
payload between every stage. DriveClubFS and the package/resource utilities are
external file-oriented programs, so VirtualAuto cannot truthfully replace their
interfaces with `BytesIO`. A wrapper may pass an output path directly into the
next compatible stage, or use an ignored temporary directory, after that path is
validated and the transformation is recorded. It must not overwrite the prior
stage's immutable input or silently discard unknown files.

If profiling later identifies material I/O cost, optimise the measured stage.
Do not remove auditable boundaries merely because an in-memory design sounds
cleaner in the abstract.
