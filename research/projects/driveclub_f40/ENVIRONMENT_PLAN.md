# DriveClub F40 environment qualification plan

## Status

`P2-buildable corridor specified; no private F40 environment profile executed`

This plan connects the general
[environment domain](../../environment/README.md) to the currently sourced
third-party F40 export and the incomplete original-resource archaeology. It does
not claim that the original DriveClub environment renderer, materials, or
weather systems have been recovered.

The first environment research pass was deliberately reviewed for practicality.
The governing documents are now:

- [environment practicality audit](../../environment/PRACTICALITY_AUDIT.md);
- [production ladder](../../environment/PRODUCTION_LADDER.md);
- [experiment priority](../../environment/EXPERIMENT_PRIORITY.md);
- [F40 glass quickstart](../../../workflows/environment/F40_GLASS_QUICKSTART.md).

A non-destructive Blender builder now exists at
[`build_f40_glass_corridor.py`](../../../workflows/environment/build_f40_glass_corridor.py).
It remains `P2-buildable`, not executed evidence.

## Immediate reason

The current F40 render shows a strong paint response but a windshield with
symmetrical triangular patches that remain visibly different under smoothing
and cleanup attempts. Complex HDRI/weather detail can conceal whether the fault
belongs to:

- topology or non-planar triangulation;
- imported custom loop normals;
- tangent reconstruction;
- overlapping inner/outer/rain shells;
- vertex colours or unknown attributes;
- UV stream selection;
- material roughness/tint/normal inputs;
- engine-specific transmission/reflection behaviour.

The first environment must therefore maximize diagnostic separation, not visual
spectacle.

## Phase 1 — Neutral glass-forensics corridor

This is a Level 0 environment. Atmosphere, HDRI, detailed asphalt, terrain,
weather, and post effects are explicitly out of scope.

### Far field

- constant neutral World for the starter build;
- no analytic sky until the neutral rig is understood;
- no clouds;
- no rain, droplets, glare, or compositor haze;
- no Sun light in the starter profile.

### Near field

- metric dry neutral road slab;
- one large bright finite band on one side;
- one smaller differently placed bright band on the other;
- one dark absorber region;
- no repeating small lights or dense architecture;
- chrome, grey, black-gloss, and glass proxy objects.

This asymmetric layout should produce broad reflection bands that reveal
whether triangular patches remain locked to faces/loops as camera and environment
move.

### Windshield sequence

1. retain immutable duplicate of imported windshield;
2. plain opaque grey, no textures or attributes;
3. flat versus smooth shading;
4. imported custom normals versus cleared/recalculated normals on duplicates;
5. specular opaque dielectric;
6. minimal glass with no tint/normal/roughness maps;
7. finite thickness/shell isolation;
8. one UV/attribute input at a time;
9. full material only after the fault owner is identified.

### Required captures

- geometric-normal and split-normal visualizations;
- face/material/UV/colour-attribute IDs;
- left band, right band, absorber, World, and direct-light contribution toggles;
- camera orbit;
- environment movement with fixed camera/car;
- Cycles baseline before EEVEE comparison;
- screenshot and scene-linear evidence at fixed exposure;
- diagnostic-sphere confirmation that the rig itself is not generating the same
  artefact on known-good geometry.

### Classification outcome

Record the artefact as one or more:

- `topology-locked`;
- `loop-normal-locked`;
- `tangent-locked`;
- `UV/attribute-locked`;
- `overlap/depth-locked`;
- `view/reflection-locked`;
- `engine-specific`;
- `unresolved`.

## Phase 2 — Paint robustness matrix

After the windshield fault is isolated, qualify the existing paint under:

1. neutral studio-like reflection environment;
2. clear dry midday;
3. low-sun dry atmosphere;
4. bright structured overcast.

Post-rain lighting is deferred until the dry road and static wet-state milestones
exist.

No per-environment material retuning without a recorded variant. Inspect:

- bonnet/fender reflection roll-off;
- clearcoat highlight core and shoulder;
- metallic/effect-pigment response;
- panel-to-panel continuity;
- red-channel clipping and tone-map saturation;
- lower-body road reflection;
- consistency with black trim, carbon, lamps, tyres, and glass.

## Phase 3 — Road and grounding

Build one metric dry road corridor with:

- profile/camber only where visible or needed for contact;
- texture scale ownership chosen by camera distance and tyre contact;
- shoulder and drainage logic reserved for the wet milestone;
- tyre-contact and shadow diagnostics;
- lower-body reflection consistency.

The road should expose vehicle scale and stance before detailed terrain or track
dressing is added. The starter Level 0 slab is intentionally not production
asphalt.

## Phase 4 — Static wet-surface progression

Before active rain:

1. damp substrate darkening;
2. connected wet film;
3. low-point ponding and runoff;
4. tyre-contact disturbance eligibility;
5. post-rain drying state.

The same accepted dry substrate and topography must remain underneath every state.

## Phase 5 — Active weather progression

Only after dry and static wet qualification:

1. isolated rain streaks and shutter test;
2. ground impact/splash;
3. tyre spray from eligible water regions;
4. windshield droplets/flow;
5. wiper interaction;
6. camera/lens contamination as a separate post layer.

The model must not imitate DriveClub's rain system by visual guess and then label
it recovered. Original game behaviour may be used as `SRC-COMMUNITY` or captured
reference only after provenance and version are recorded.

## Phase 6 — Terrain and context

Add near/mid/far layers only when the shot demands them:

- road cut/shoulder/drainage;
- one declared soil/aggregate class;
- terrain silhouette and haze;
- vegetation mass tied to terrain/water logic;
- finite reflection structures;
- motion-stable LOD.

The target is a coherent camera and reflection field, not a complete DriveClub
track.

## Environment profile IDs proposed

- `ENV-F40-DIAG-GLASS-DRY-001`
- `ENV-F40-PAINT-CLEAR-MIDDAY-001`
- `ENV-F40-PAINT-OVERCAST-001`
- `ENV-F40-ROAD-WET-001`
- `ENV-F40-RAIN-ACTIVE-001`
- `ENV-F40-POSTRAIN-LOWSUN-001`

These IDs reserve intent only. No corresponding profile becomes executed or
validated until a schema-backed record and evidence package exist.

## Stop conditions

Stop material work when:

- environment energy ownership is unclear;
- camera exposure changes between comparison variants;
- the windshield material masks a geometry/normal fault;
- an HDRI is introduced before the Level 0 classification;
- HDRI sun clipping is compensated by paint roughness;
- wet road state ignores topography;
- rain/spray is added before dry road and glass baselines;
- EEVEE limitations are treated as source-asset defects;
- a visual similarity to DriveClub is represented as recovered original logic.

## Next smallest action

1. Register the third-party F40 export as a private immutable source asset.
2. Run the existing non-destructive Blender `5.0.1` inventory.
3. Execute `build_f40_glass_corridor.py` in a copy of the workfile.
4. Run only the opaque/specular/minimal-glass sequence from the quickstart.
5. Retain one supported classification before any HDRI, atmosphere, road-detail,
   or weather work.

The general environment research supplies future reference and ownership. It does
not replace this small diagnostic execution.