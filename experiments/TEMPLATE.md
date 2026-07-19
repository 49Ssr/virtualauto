# EXP-<DOMAIN>-<NUMBER>: <title>

Create a matching JSON manifest using
[`experiment.schema.json`](../schemas/experiment.schema.json). This Markdown
record explains the reasoning and retained result; the JSON record supplies
machine-checkable fields.

## Status

`planned | active | blocked | accepted | rejected | superseded`

## Question

State one answerable question. Avoid combining material identity, geometry,
camera, and post-processing into one experiment unless the interaction itself is
the target.

## Evidence basis

- Source IDs:
- Existing evidence IDs:
- Relevant observation IDs:
- Known contradictions:
- Version and sample boundaries:

## Hypothesis

State a falsifiable prediction and the mechanism that would produce it.

## Assumptions

List every assumption that limits generalization, including:

- source build or asset revision;
- Blender version and render engine;
- coordinate system and physical scale;
- resolved versus subpixel features;
- clean, damaged, wet, repaired, or aged state;
- camera, lighting, colour management, and post-processing state.

## Controlled variables

- Blender version:
- Render engine:
- Scene and asset revision:
- Input checksums:
- Camera and lighting:
- Colour management:
- Sampling and denoising:
- Random seed:
- Hardware where performance is measured:

## Owned variable

Identify the one primary variable or branch changed by this experiment and the
system that owns it.

## Procedure

1. Register immutable inputs and exact tool revisions.
2. Establish and retain the baseline.
3. Change the owned variable only.
4. Capture branch-off, branch-only, exaggerated, target, and combined states
   where applicable.
5. Capture value diagnostics separately from radiance-contribution variants.
6. Repeat required still, motion, scale, engine, and fresh-file checks.
7. Record failures and unexpected observations before interpreting them.

## Acceptance criteria

- Quantitative:
- Visual:
- Temporal:
- Performance:
- Compatibility:
- Fresh-file reproducibility:
- Held-out condition:

## Failure criteria

- Conditions that falsify the hypothesis:
- Confounding artefacts to rule out:
- Conditions that make the result inconclusive:

## Required evidence

- Artifact types:
- Repository or private-storage locations:
- Checksums and byte sizes:
- Observation records:
- Logs and node/mesh dumps:

## Result

Untested. Complete only from retained evidence. Describe measurements and raw
observations before interpretation.

## Decision

`pending | accept | reject | revise | supersede`

State the smallest next action. Rejection is a retained result and must not
remove the original hypothesis or evidence.
