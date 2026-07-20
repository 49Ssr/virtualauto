# Repository architecture

VirtualAuto uses six visible domain areas plus the packaged implementation.
The layout is intentionally shallow: detailed categories live behind a README,
not at the repository root.

## Top-level ownership

| Path | Owns | Does not own |
| --- | --- | --- |
| `research/` | Reviewed automotive knowledge, project records, archaeology, and generated retrieval indexes | Executable truth or private assets |
| `workflows/` | Operator-facing DriveClub and Blender procedures, scripts, and ignored workspaces | General governance or third-party source code |
| `lab/` | Governance, schemas, experiments, evidence, and schema examples | The canonical research master or production source assets |
| `external/` | Audited records and exact-commit third-party instruments | Automatic trust in upstream behaviour |
| `dev/` | Repository maintenance scripts, fixtures, and tests | Automotive domain workflows |
| `src/virtualauto/` | Packaged guards and command-line implementation | Vendor implementations or scientific conclusions |
| `.github/` | Repository automation and contribution controls | Domain knowledge |

Directories such as `build/`, `tmp/`, and private workflow workspaces may exist
locally but are ignored and are not part of the published root.

## Canonical research and indexes

The unified automotive master is the canonical human and research source:

`research/automotive_materials/Automotive_Body_RnD_Master.md`

Deterministic navigation artifacts live under `research/indexes/`. They declare
the master checksum, source line ranges, and generator version. They are never
manually edited and never outrank or replace the master.

## Lab record graph

```text
source asset (AST)
    -> transformation (TRN)
    -> derived source asset (AST)
    -> evidence (EVD)
    -> observation (OBS)
    -> experiment (EXP)
    -> claim (CLM)
    -> Blender node contract (NODE)
```

Unknown binary or vertex semantics remain explicit `UNK` records. This graph
captures traceability, not a compulsory chronology.

## Workflow ownership

Geometry-derived state belongs in workflow preprocessing where practical;
optical transport remains in the shader; fixed configuration belongs in
versioned records. Each workflow documents its input, output, destructive
boundaries, and evidence requirements.

DriveClub private inputs and extracted outputs live in a run-scoped workspace
outside the checkout. The repository contains only the workspace contract and
the command that creates those folders.

External command-line tools own file-oriented formats and therefore retain
explicit input/output custody boundaries. VirtualAuto may use temporary storage
internally, but it must not pretend an external process can consume an in-memory
Python stream when its reviewed interface requires files. Containerization is a
deployment option only after the tool's platform, runtime, licensing, and data-
access requirements are established.

The portable core under `src/virtualauto/` must remain importable without
Blender. `bpy` is confined to Blender-hosted entrypoints. A future artist-facing
add-on is an adapter over tested contracts, not a second implementation of the
pipeline.

The supported human command surface is `virtualauto`, even when it launches an
internal maintenance script or Blender-hosted entrypoint. `dev/scripts/` owns
repository-generation and validation internals; `workflows/blender/scripts/`
owns code that must execute inside Blender. Moving either into the portable
package would blur runtime ownership without improving the user interface.

## Human and machine state

Human status Markdown owns narrative, priorities, unknowns, and decisions.
Schema-backed JSON owns executable parameters, measured values, transformations,
and evidence identity. A status page links those records by stable ID; it must
not become a second executable parameter store. Generated Markdown may be added
when a record has a useful human view, but prose is not regenerated merely to
create the illusion of one format owning every kind of knowledge.

## External instruments

`external/tools.lock.json` is the machine-readable registry. Each tool record
states purpose, reviewed revision, inputs, outputs, limitations, license state,
and integration status. A pinned commit proves identity only—not correctness,
safety, or successful execution.

## Restricted and binary files

Raw packages, extracted resources, third-party models, textures, captures,
large renders, and private `.blend` files stay outside Git. Narrow original
regression fixtures are governed by the
[binary asset policy](BINARY_ASSET_POLICY.md) and
[rights boundary](RIGHTS_AND_ASSET_BOUNDARIES.md).

## Change control

- Stable IDs are not repurposed.
- Superseded and rejected records remain traceable.
- Unknown fields are preserved before interpretation.
- Destructive conversions require a loss assessment.
- Generated views are reproducible from the canonical source.
- Structural validation never masquerades as physical validation.
