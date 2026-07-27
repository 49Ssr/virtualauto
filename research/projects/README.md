# VirtualAuto projects

This directory keeps concise, append-oriented status records for actual Blender
and archaeology projects. Domain knowledge belongs under `research/`; reusable
operator implementation belongs under `workflows/`; retained tests belong under
`lab/experiments/`. Project records link those systems to a specific asset and state.

## Current projects

- [DriveClub Ferrari F40 archaeology](driveclub_f40/STATUS.md) — active research;
  a sparse 1.28 overlay exposed a partial F40 resource catalogue, while the
  matching base contribution and complete source semantics remain missing.
  The [environment qualification plan](driveclub_f40/ENVIRONMENT_PLAN.md)
  isolates the sourced export's windshield and paint before weather complexity.
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