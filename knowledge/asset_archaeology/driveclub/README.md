# DriveClub asset archaeology

This module studies how DriveClub vehicle assets are packaged, referenced,
converted, and ultimately reconstructed in Blender without discarding unknown
semantics.

## Current state

- No PS4 package or root installation has been processed by VirtualAuto.
- No DriveClub mesh, material, shader, hierarchy, or vehicle definition has been
  decoded by VirtualAuto.
- No extracted game asset is stored in this repository.
- The user reports owning an already-exported F40 model with apparently damaged
  or incomplete UV behaviour. That is an `OBS-USER` research lead, not retained
  evidence and not proof of the original format semantics.
- DriveClubFS and 010GameTemplates have been inspected at pinned commits. Their
  documented and code-visible boundaries are recorded below.

## Evidence labels

| Label | Meaning |
| --- | --- |
| `SRC-UPSTREAM-DOC` | Stated by an upstream project's own documentation |
| `SRC-CODE` | Directly visible in pinned source code |
| `SRC-COMMUNITY` | Reported in a reverse-engineering forum or user tool; requires reproduction |
| `OBS-USER` | Direct report from the VirtualAuto operator without retained repository evidence |
| `HYP` | Plausible interpretation awaiting a controlled test |
| `UNRESOLVED` | Known question without sufficient evidence |
| `VA-VALIDATED` | Reproduced by VirtualAuto with linked evidence |

No claim in this directory is `VA-VALIDATED` yet.

## Documents

- [Pipeline boundary](PIPELINE.md)
- [Resource and semantic model](RESOURCE_MODEL.md)
- [Failure modes and parser rules](FAILURE_MODES.md)
- [F40 first-target plan](F40_TARGET.md)
- [Open questions and experiments](OPEN_QUESTIONS.md)
- [Source register](SOURCE_REGISTER.md)

## Governing principle

The target is not a convenient FBX export. The target is a reproducible semantic
intermediate that preserves:

- raw resource identity and dependency links;
- every vertex and index stream;
- original byte ranges, offsets, counts, and strides;
- all UV, colour, normal, tangent, skinning, and unknown channels;
- submesh, material, hierarchy, LOD, damage, and state relationships where
  available;
- the exact tool revisions and transformations applied.

Blender is a consumer of that intermediate. It must not become the first place
where source meaning is guessed or silently destroyed.
