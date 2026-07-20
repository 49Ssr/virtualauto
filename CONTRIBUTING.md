# Contributing to VirtualAuto

VirtualAuto is an evidence-driven research and Blender engineering repository.
Changes should make the project more reproducible, more inspectable, or easier
to falsify. Volume alone is not progress.

## Before changing the repository

1. Identify the owned domain: knowledge, archaeology, Blender implementation,
   experiment, evidence, schema, or external instrument.
2. Separate direct observations from interpretations and sourced claims.
3. State what is unknown and what the change deliberately does not establish.
4. Confirm that no extracted game data, private captures, licensed source assets,
   credentials, or local workspace databases are included.

## Branches and pull requests

Use a focused branch. Pull requests should include:

- purpose and affected domain;
- source and provenance changes;
- validation performed;
- limitations and unresolved questions;
- any migration or compatibility impact;
- explicit confirmation that prohibited assets are absent.

Do not merge a research hypothesis by rewriting it as validated knowledge.
Retain rejected experiments and superseded records when they remain useful
provenance.

## Machine-readable records

JSON records must declare a local `$schema` and pass
`scripts/validate_repository.py`. IDs are stable once published. Corrections
should update status or create a superseding record rather than silently
reusing an ID for a different meaning.

## Blender implementations

The production baseline is Blender `5.0.1` unless a record explicitly says
otherwise. An implementation must declare exact node or API dependencies,
inputs, outputs, spaces, units, engine scope, diagnostics, limitations, and
practicality status. Source inspection alone does not qualify a node group as
executed.

## External repositories

Treat external code as a versioned research instrument. Record the exact commit,
license state, documented input/output boundary, and VirtualAuto validation
state before adding a submodule or depending on behaviour.

## Local validation

```text
python -m pip install -e .
virtualauto build-index
virtualauto validate
python -m unittest discover -s tests -v
```

A passing validator proves structural consistency only. It does not prove a
physical model, reverse-engineered semantic, or render result is correct.
