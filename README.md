# VirtualAuto

An evidence-driven automotive Blender and asset-archaeology laboratory.

VirtualAuto connects source provenance, semantic recovery, physically grounded
materials, environments, Blender implementation, and retained validation
evidence. It does not contain proprietary DriveClub packages or extracted game
assets.

## Repository map

| Area | Use it for |
| --- | --- |
| [`research/`](research/README.md) | Automotive materials, geometry, environment, project records, and the authoritative R&D master |
| [`workflows/`](workflows/README.md) | DriveClub extraction, Blender operation, and environment qualification procedures |
| [`lab/`](lab/README.md) | Experiments, evidence, schemas, examples, and governance |
| [`external/`](external/README.md) | Audited and pinned third-party research instruments |
| [`dev/`](dev/README.md) | Repository maintenance scripts and tests |
| [`src/virtualauto/`](src/virtualauto/) | VirtualAuto's guarded command-line implementation |

The full ownership rules are documented in the
[repository architecture](lab/governance/REPOSITORY_ARCHITECTURE.md).

## Current baseline

- Reproduced headless baseline: Blender `5.0.1`
- Interactive live-control target: Blender `5.2.0 LTS`
- First archaeology target: DriveClub Ferrari F40
- Pinned operational extractor: DriveClubFS
- Environment research: sky, atmosphere, aerosols, HDRI, roads, terrain,
  weather, surface state, built context, camera boundaries, and an initial
  schema-backed profile contract; no environment profile is yet claimed
  production-qualified
- Repository state: guarded extraction, deterministic research retrieval, a
  Blender asset-audit panel, and the first accepted coordinate-math invariant;
  no claim of completed DriveClub model conversion or production material

Live Blender control is documented in the
[MCP runbook](workflows/blender/mcp/README.md). Its official upstream connector
is pinned and installed separately; the repository does not pretend its weak
execution sandbox is a security boundary.

The exact Automotive Body R&D v5 master is preserved at
[Automotive_Body_RnD_Master.md](research/automotive_materials/Automotive_Body_RnD_Master.md).
Its generated [heading index](research/indexes/automotive_master.index.json) is
only a retrieval aid and never replaces the master.

The first-class [environment domain](research/environment/README.md) separates
far-field radiance, direct emitters, participating media, roads and terrain,
weather, finite reflection structure, and camera/display ownership. Its
[operating workflow](workflows/environment/README.md) starts with controlled
F40 windshield and paint diagnostics rather than a beauty-scene preset.

Retrieve focused, checksum-bound sections without deleting history:

```text
virtualauto research find weave --prefix ABR-COMP
virtualauto research get ABR-COMP-010
```

## DriveClub quick start

```text
git submodule update --init --recursive
python -m pip install -e .
virtualauto doctor
virtualauto driveclub build
virtualauto workspace init D:\VirtualAutoWorkspace --run-id dc-f40-001
virtualauto pkg inspect --input D:\VirtualAutoWorkspace\runs\dc-f40-001\pkg\input
virtualauto driveclub inspect --input D:\VirtualAutoWorkspace\runs\dc-f40-001\driveclubfs\input
virtualauto pkg --help
virtualauto driveclub --help
```

The private run workspace contract and exact operating sequence are in the
[DriveClub runbook](workflows/driveclub/RUNBOOK.md). Package access or extraction
does not by itself provide a Blender-ready vehicle; mesh, material, and semantic
recovery remain separate research stages.

## Validate the repository

```text
virtualauto build-index
virtualauto validate
python -m unittest discover -s dev/tests -v
```

A clean result proves structural consistency, link integrity, schema validity,
pin consistency, and restricted-asset boundaries. It does not prove a physical
model or reverse-engineered interpretation is correct.

## Operating principles

- Evidence, observation, interpretation, implementation, and validation remain
  distinct states.
- Unknown source data is preserved before interpretation.
- External tools are pinned instruments, not trusted black boxes.
- The authoritative master is append-only in spirit and checksum guarded.
- Private or copyrighted source assets stay outside Git.
- Every complex Blender solution must expose diagnostics and failure conditions.
- Evidence hashing and record metadata are automated; observations and claims
  remain deliberate human or instrument interpretations.

Start with the [project doctrine](lab/governance/PROJECT_DOCTRINE.md) before
changing research or implementation records.