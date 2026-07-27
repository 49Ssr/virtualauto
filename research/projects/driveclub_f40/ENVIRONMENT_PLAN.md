# DriveClub F40 environment qualification plan

## Status

`P1-specified; no F40 environment profile executed`

This plan connects the general
[environment domain](../../environment/README.md) to the currently sourced
third-party F40 export and the incomplete original-resource archaeology. It does
not claim that the original DriveClub environment renderer, materials, or
weather systems have been recovered.

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

### Far field

- clear analytic sky or neutral controlled world;
- no clouds;
- no rain, droplets, glare, or compositor haze;
- direct-sun ownership isolated and disable-able.

### Near field

- metric dry road;
- one broad light façade/wall on one side;
- one darker vegetation/absorber mass on the other;
- open upper sky;
- simple horizon;
- no repeating small lights or dense architecture.

This asymmetric layout should produce broad reflection bands that reveal
whether triangular patches remain locked to faces/loops as camera and light move.

### Windshield sequence

1. retain immutable duplicate of imported windshield;
2. plain opaque grey, no textures or attributes;
3. flat versus smooth shading;
4. imported custom normals versus cleared/recalculated normals;
5. specular opaque dielectric;
6. transmission with no tint/normal/roughness maps;
7. finite thickness/shell isolation;
8. one UV/attribute input at a time;
9. full material only after the fault owner is identified.

### Required captures

- geometric-normal and split-normal visualizations;
- face/material/UV/colour-attribute IDs;
- world-only, direct-only, and combined light;
- camera orbit;
- environment rotation with fixed camera/car;
- Cycles baseline before EEVEE comparison;
- screenshot and scene-linear evidence at fixed exposure.

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

1. clear dry midday;
2. low-sun dry atmosphere;
3. bright structured overcast;
4. neutral studio-like reflection environment;
5. post-rain low sun.

No per-environment material retuning without a recorded variant. Inspect:

- bonnet/fender reflection roll-off;
- clearcoat highlight core and shoulder;
- metallic/effect-pigment response;
- panel-to-panel continuity;
- red-channel clipping and tone-map saturation;
- lower-body road reflection;
- consistency with black trim, carbon, lamps, tyres, and glass.

## Phase 3 — Road and grounding

Build one metric road corridor with:

- profile/camber;
- separated micro/macro/megatexture;
- shoulder and drainage;
- dry/damp/wet-film/ponded state variants;
- tyre-contact and shadow diagnostics;
- lower-body reflection consistency.

The road should expose vehicle scale and stance before detailed terrain or
track dressing is added.

## Phase 4 — Weather progression

Only after dry qualification:

1. isolated rain streaks and shutter test;
2. road spotting and damp progression;
3. connected wet film;
4. low-point ponding and runoff;
5. tyre spray from eligible water regions;
6. windshield droplets/flow;
7. wiper interaction;
8. post-rain drying state;
9. camera/lens contamination as a separate post layer.

The model must not imitate DriveClub's rain system by visual guess and then label
it recovered. Original game behaviour may be used as `SRC-COMMUNITY` or captured
reference only after provenance and version are recorded.

## Phase 5 — Terrain and context

Add near/mid/far layers:

- road cut/shoulder/drainage;
- one declared soil/aggregate class;
- terrain silhouette and haze;
- vegetation mass tied to terrain/water logic;
- finite reflection structures;
- motion-stable LOD.

The initial target is a controlled corridor, not a complete DriveClub track.

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
- HDRI sun clipping is compensated by paint roughness;
- wet road state ignores topography;
- rain/spray is added before dry road and glass baselines;
- EEVEE limitations are treated as source-asset defects;
- a visual similarity to DriveClub is represented as recovered original logic.

## Next smallest action

Register the third-party F40 export as a private immutable source asset, run the
existing non-destructive Blender `5.0.1` inventory, and execute only the Phase 1
neutral corridor. The general environment research supplies the diagnostic
ownership; it does not replace the export inventory.