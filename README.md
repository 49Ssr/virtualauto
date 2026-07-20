# VirtualAuto

Research-driven automotive Blender workflow laboratory.

VirtualAuto builds a reproducible path from source-asset archaeology to
physically grounded automotive reconstruction, Blender implementation, and
retained validation evidence.

```text
source asset
    -> provenance and rights boundary
    -> resource archaeology
    -> semantic intermediate
    -> Blender reconstruction
    -> physically based implementation
    -> controlled validation
```

The goal is not merely an attractive render. The repository preserves why an
asset, material, node system, or conversion decision exists and what evidence
would prove it wrong.

## Production baseline

- Blender: `5.0.1`
- Forward reference: Blender `5.2 LTS` only when explicitly labelled
- Repository stage: foundation and first archaeology research
- Current first target: DriveClub Ferrari F40 source and export diagnostics

No DriveClub package, extracted resource, model, texture, or proprietary game
data is committed here.

## Start here

- [Project doctrine](docs/PROJECT_DOCTRINE.md)
- [Repository architecture](docs/REPOSITORY_ARCHITECTURE.md)
- [AI retrieval protocol](docs/AI_RETRIEVAL_PROTOCOL.md)
- [Rights and asset boundaries](docs/RIGHTS_AND_ASSET_BOUNDARIES.md)
- [Contribution workflow](CONTRIBUTING.md)
- [Project status and changelogs](projects/README.md)
- [Knowledge index](knowledge/README.md)
- [Blender implementation index](blender/README.md)
- [Experiment system](experiments/README.md)
- [External research instruments](external/README.md)
- [Validated schema examples](examples/README.md)

## Active research

### DriveClub archaeology

The initial DriveClub module records what is visible in pinned upstream code,
what the reverse-engineering community has reported, and what remains unknown.
It explicitly avoids pretending that filesystem extraction already equals a
Blender-ready vehicle converter.

- [Domain status and evidence labels](knowledge/asset_archaeology/driveclub/README.md)
- [Extraction-to-Blender pipeline](knowledge/asset_archaeology/driveclub/PIPELINE.md)
- [Resource model](knowledge/asset_archaeology/driveclub/RESOURCE_MODEL.md)
- [Failure modes](knowledge/asset_archaeology/driveclub/FAILURE_MODES.md)
- [DriveClubFS gap audit](knowledge/asset_archaeology/driveclub/TOOL_GAP_AUDIT.md)
- [F40 target plan](knowledge/asset_archaeology/driveclub/F40_TARGET.md)
- [Open questions](knowledge/asset_archaeology/driveclub/OPEN_QUESTIONS.md)
- [Source register](knowledge/asset_archaeology/driveclub/SOURCE_REGISTER.md)

### Automotive body and materials master

The exact v5 unified master is available in the project artifact workspace but
has not yet been transferred into Git. Its verified status and controlled import
gate are recorded in
[MASTER_IMPORT_STATUS.md](knowledge/automotive_materials/MASTER_IMPORT_STATUS.md).
No summarized replacement is presented as the master.

## Core principles

### Evidence over assumption

Every important claim records source, confidence, scope, limitations, and a
validation path. Direct observation, interpretation, implementation, and
production qualification are separate states.

### Unknown data is preserved

Unknown mesh attributes, binary fields, material flags, and dependency edges are
retained before interpretation. Convenient formats such as FBX are derived
outputs, not automatic sources of truth.

### Research is not implementation

```text
lead
 -> sourced claim or hypothesis
 -> implementation contract
 -> controlled prototype
 -> retained observation
 -> production qualification
```

A paper, forum post, source-code function, or node diagram does not prove that a
workflow runs correctly in Blender.

### External tools are instruments

DriveClubFS, ShadPKG, PkgToolBox, and 010GameTemplates are recorded at exact
upstream commits with purpose, limitations, license state, and integration
status. Submodules are added only through a separate reviewed decision.

## Repository validation

```bash
python -m pip install jsonschema PyYAML
VIRTUALAUTO_STRICT_VALIDATION=1 python scripts/validate_repository.py
```

Validation checks schemas, cross-record references, local links, repository
structure, evidence locations, tool pins, and prohibited asset leakage. A pass
proves structural consistency, not physical or reverse-engineering correctness.
