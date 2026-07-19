# VirtualAuto

Research-driven automotive Blender workflow laboratory.

## Purpose

VirtualAuto exists to build a reproducible pipeline for automotive asset reconstruction, physically based materials, rendering research, and Blender workflow development.

The project is not focused only on producing attractive renders. It aims to preserve the reasoning behind automotive assets:

```
source asset
    -> provenance
    -> archaeology
    -> reconstruction
    -> physically based implementation
    -> validation
```

## Core principles

### Evidence over assumption

Research findings, reverse-engineering discoveries, and implementation choices should record:

- source
- confidence
- limitations
- validation method

### Unknown data is preserved

Unknown mesh attributes, material parameters, or resource fields are not discarded prematurely. They are documented as unknowns with hypotheses and experiments.

### Research is not implementation

A paper, forum post, or existing tool does not automatically become production workflow. Systems move through:

```
research
 -> implementation proposal
 -> prototype
 -> validation
 -> production status
```

### Blender baseline

Initial workflow target:

- Blender 5.0.1

## Initial domains

- Automotive materials
- Geometry rehabilitation
- Asset archaeology
- Blender node workflows
- Geometry Nodes systems
- Game asset recovery
- Validation and diagnostics

## Repository status

Early foundation stage. Structure will be expanded deliberately.
