# VirtualAuto projects

This directory keeps concise, append-oriented status records for actual Blender
and archaeology projects. Domain knowledge belongs under `knowledge/`; reusable
implementation belongs under `blender/`; retained tests belong under
`experiments/`. Project records link those systems to a specific asset and state.

## Current projects

- [DriveClub Ferrari F40 archaeology](driveclub_f40/STATUS.md) — active research
  target; original resources not yet acquired by VirtualAuto.
- [Pagani Huayra cinematic recreation](pagani_huayra/STATUS.md) — paused; retains
  unresolved geometry, material, and lighting observations.

## Update rule

Each status record should preserve:

- current state and last meaningful change;
- immutable source and derived-asset IDs when registered;
- Blender version and scene revision;
- confirmed observations versus suspected causes;
- blockers and next smallest actions;
- links to experiments and evidence;
- a short append-only changelog.

Do not use a project note to promote one asset-specific observation into general
technical doctrine.
