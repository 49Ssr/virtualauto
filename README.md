# VirtualAuto

An evidence-driven automotive Blender and asset-archaeology laboratory.

VirtualAuto connects source provenance, semantic recovery, physically grounded
materials, Blender implementation, and retained validation evidence. It does
not contain proprietary DriveClub packages or extracted game assets.

## Repository map

| Area | Use it for |
| --- | --- |
| [`research/`](research/README.md) | Automotive knowledge, project records, and the authoritative R&D master |
| [`workflows/`](workflows/README.md) | DriveClub extraction and Blender operating procedures |
| [`lab/`](lab/README.md) | Experiments, evidence, schemas, examples, and governance |
| [`external/`](external/README.md) | Audited and pinned third-party research instruments |
| [`dev/`](dev/README.md) | Repository maintenance scripts and tests |
| [`src/virtualauto/`](src/virtualauto/) | VirtualAuto's guarded command-line implementation |

The full ownership rules are documented in the
[repository architecture](lab/governance/REPOSITORY_ARCHITECTURE.md).

## Current baseline

- Blender baseline: `5.0.1`
- First archaeology target: DriveClub Ferrari F40
- Pinned operational extractor: DriveClubFS
- Repository state: guarded extraction, deterministic research retrieval, a
  Blender asset-audit panel, and the first accepted coordinate-math invariant;
  no claim of completed DriveClub model conversion or production material

The exact Automotive Body R&D v5 master is preserved at
[Automotive_Body_RnD_Master.md](research/automotive_materials/Automotive_Body_RnD_Master.md).
Its generated [heading index](research/indexes/automotive_master.index.json) is
only a retrieval aid and never replaces the master.

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
