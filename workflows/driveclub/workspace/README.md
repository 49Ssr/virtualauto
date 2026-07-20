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
