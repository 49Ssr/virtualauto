# Repository architecture

VirtualAuto separates authoritative knowledge, executable implementation,
evidence, and third-party instruments so that each can evolve without erasing
its provenance.

## Top-level ownership

| Path | Owns | Does not own |
| --- | --- | --- |
| `knowledge/` | Reviewed technical knowledge and archaeology records | Executable Blender truth or raw source assets |
| `blender/` | Versioned builders, contracts, diagnostics, and implementation code | Unsupported physical claims |
| `experiments/` | Falsifiable plans and decisions | Unreviewed asset dumps |
| `evidence/` | Small lawful evidence manifests and retained records | Automatic conclusions |
| `schemas/` | Machine-readable record contracts | Domain conclusions |
| `external/` | Pinned records for third-party research instruments | Blind trust in upstream behaviour |
| `tools/` | VirtualAuto-owned utilities | Vendored proprietary data |
| `examples/` | Executable schema documentation using fictionalized records | Evidence that a real extraction or render occurred |
| `docs/` | Governance, boundaries, and retrieval rules | The automotive R&D master itself |

## Authoritative master and retrieval views

The unified automotive master remains the canonical human and research source.
It lives at:

`knowledge/automotive_materials/Automotive_Body_RnD_Master.md`

Focused retrieval files live under `generated/` only when a deterministic
generator can reproduce them from the canonical master. Every generated index
must declare:

- source master SHA-256;
- content-derived section ID;
- source line range;
- generator version;

Generated files are never manually edited. A clean regeneration must produce no
diff.

## Record graph

VirtualAuto's core provenance graph is:

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

Unknown binary or vertex semantics are retained as `UNK` records and linked to
source assets, evidence, and transformations.

This is not a mandatory chronological order. Raw observations can precede an
experiment, and claims can remain hypotheses indefinitely. The graph exists to
make those states explicit.

## External tools

`external/tools.lock.json` is the machine-readable index. Individual Markdown
records explain purpose, documented inputs and outputs, license state,
limitations, and intended role. A pinned commit means "this revision was
reviewed"; it does not mean the tool was successfully executed.

Submodules require a separate pull request. They must be pinned to exact commits
and justified by reproducibility value, legal compatibility, and maintenance
cost.

## Large and restricted files

Raw packages, extracted resources, third-party models, textures, captures,
large renders, and private `.blend` files remain outside Git. Repository records
may store checksums, byte sizes, private storage references, and lawful small
derivatives. See [rights and asset boundaries](RIGHTS_AND_ASSET_BOUNDARIES.md).

## Change control

- Stable IDs are not repurposed.
- Superseded records remain traceable.
- Unknown fields are preserved before interpretation.
- Destructive conversions require a loss assessment.
- Blender work advances through `P0` to `P5`; research depth alone does not
  increase the implementation grade.
- The default branch contains accepted infrastructure and explicitly labelled
  research states, not claims of completion.
