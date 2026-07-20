# Pagani Huayra cinematic recreation status

## State

`discontinued; evidence retained`

The original project is discontinued. Its unresolved observations are retained
because they directly motivate reusable geometry, material, AO, lighting, and
import-forensics work; retaining them does not imply that work will resume.

## Current baseline

- Blender production baseline for future work: `5.0.1`
- Source model: untextured FBX reported by the user; not registered in the
  repository
- Source caveat: some geometric features may be placeholders for alpha-, UV-,
  normal-, or shader-driven details rather than literal final geometry
- Current scene and material revisions: not registered
- Retained evidence: none in this repository

## Direct user observations

`OBS-USER`, no repository evidence yet:

- several carbon regions show unstable or incorrect shading normals;
- a Weighted Normal modifier improves some regions but should not remain an
  unexplained dependency;
- some materials required manually baked AO;
- AO darkening albedo damages textures and does not provide the desired
  material-specific occlusion of diffuse and reflections;
- light behaviour should eventually expose shared maximum, minimum, frequency,
  `maxk`, and `mink` controls, but their exact ownership and meaning are not yet
  specified;
- the grille needs darker apparent albedo and a thinner, noisier coat response;
- current EEVEE results can remain convincing with conventional cast shadows
  disabled in some shots because diffuse/specular lighting was heavily tuned.

The final point is a scene-specific observation, not evidence that shadows are
physically unnecessary.

## Unresolved interpretation space

### Carbon normals

Potential causes include:

- source custom normals lost or decoded incorrectly;
- inconsistent topology, mirrored transforms, or tangent handedness;
- inappropriate smoothing boundaries;
- non-uniform scale or unapplied transforms;
- insufficient geometric curvature or triangulation mismatch;
- normal maps authored for a different tangent basis;
- separate source meshes flattened into one composite export.

Weighted Normal is a diagnostic comparison, not automatic repair.

### Material-specific AO

The desired behaviour is not "multiply base colour by AO." A future experiment
must separate:

- geometric occlusion evidence;
- indirect diffuse attenuation;
- reflection visibility or local environment occlusion;
- cavity dirt or baked pigment variation;
- engine-specific AO approximations.

Any solution must avoid double-counting physically traced occlusion in Cycles
and must state its EEVEE limitations.

### Grille

The apparent darkness may be controlled by geometry depth, transmission/open
area, substrate, roughness distribution, coating, cavity environment, or
texture—not albedo alone. Diagnose under a controlled reflection rig before
committing a material constant.

## Animation/camera note

Source video frames may include fade-in, fade-out, or standalone-badge frames.
Those can be represented as timing delays without inventing vehicle animation.
The camera can hold the current shot angle or move outside the rig temporarily
until the next shot.

## Next smallest actions when resumed

1. Register the exact FBX and a fresh immutable Blender import.
2. Audit transforms, topology, split normals, tangents, UVs, and material slots
   before modifiers.
3. Isolate one failing carbon panel and compare source normals, geometric
   normals, controlled triangulation, and a clean tangent-space diagnostic.
4. Specify an AO experiment that controls diffuse and reflection branches
   without modifying albedo.
5. Build a shared light-controller contract only after the intended variables
   have units, ownership, and shot-level acceptance criteria.

## Changelog

### 2026-07-20

- Migrated known project observations into VirtualAuto without claiming retained
  evidence or completed Blender 5.0.1 validation.
- Marked the project paused while DriveClub F40 archaeology becomes the first
  active source-recovery target.
