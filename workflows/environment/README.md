# Environment workflow

This workflow turns reviewed environment research into controlled Blender scenes
without treating artistic success as physical validation.

Production baseline: Blender `5.0.1`.

## Immediate path

Before using the full workflow, choose a production level from the
[environment production ladder](../../research/environment/PRODUCTION_LADDER.md).
Do not build weather, terrain, or atmospheric complexity merely because those
research chapters exist.

For the current F40 windshield problem:

1. follow the [F40 glass quickstart](F40_GLASS_QUICKSTART.md);
2. build the non-destructive starter corridor with
   [`build_f40_glass_corridor.py`](build_f40_glass_corridor.py);
3. classify the artefact before introducing an HDRI, transmission textures,
   droplets, rain, glare, depth of field, or compositor haze.

The builder is `P2-buildable`, not `VA-VALIDATED`, until it has been executed in
Blender `5.0.1` and retained evidence has been reviewed.

## 1. Select the role and level

State what the environment is for:

- vehicle material qualification;
- Class-A/reflection-line diagnosis;
- glass/normal forensics;
- exterior hero render;
- weather interaction;
- EEVEE performance profile;
- camera/backplate integration.

Then state the complexity level:

- Level 0 — diagnostic core;
- Level 1 — dry automotive look development;
- Level 2 — shot-specific exterior context;
- Level 3 — static wet surface state;
- Level 4 — active weather;
- Level 5 — specialised reconstruction.

One environment may support several roles, but acceptance is evaluated per role.
A later level must not block an earlier one.

## 2. Create a profile

For unresolved research structure, copy
[`lab/examples/environment_profile.json`](../../lab/examples/environment_profile.json).
For a compact buildable diagnostic starting point, copy
[`environment_profile_f40_glass_starter.json`](../../lab/examples/environment_profile_f40_glass_starter.json).
Validate either against
[`environment-profile.schema.json`](../../lab/schemas/environment-profile.schema.json).

Do not fill unresolved physical values with plausible guesses. Practical starter
values are allowed only when explicitly labelled `implementation-default` or
`artist-default`.

Each parameter records:

- value;
- unit or implementation namespace;
- status;
- source IDs;
- notes/limitations.

## 3. Establish energy ownership

Before building the scene, decide:

- what owns far-field radiance;
- what owns direct sunlight;
- what owns local atmospheric participation;
- what owns near-field reflection structure;
- what owns visible background;
- what belongs only to camera/compositor.

Produce a written ownership list and reject overlaps that cannot be diagnosed.

## 4. Build in layers

Recommended sequence:

1. camera and metric ground;
2. neutral world and diagnostic objects;
3. broad finite reflection structures;
4. sky/HDRI;
5. direct sun or other emitters;
6. horizon and camera-visible background;
7. road/terrain material scale bands;
8. bounded atmosphere;
9. weather and surface-state systems;
10. camera/post effects;
11. hero vehicle integration and motion.

Do not begin with the final beauty stack. For Level 0, stop after step 3 and the
vehicle diagnostic integration.

## 5. Required diagnostic collections

Create or link clearly named collections for:

```text
VA_ENV_DIAGNOSTICS
VA_ENV_WORLD
VA_ENV_DIRECT
VA_ENV_REFLECTORS
VA_ENV_GROUND
VA_ENV_TERRAIN
VA_ENV_ATMOSPHERE
VA_ENV_WEATHER
VA_ENV_CAMERA_POST
```

The F40 starter builder creates one owned collection named
`VA_ENV_F40_GLASS_DIAGNOSTIC` so it can be removed or rebuilt without touching the
vehicle.

These names are workflow defaults, not permanent Blender API contracts. Ownership
must remain queryable even if a future builder uses different generated names.

## 6. Contribution captures

Retain at least:

- world only;
- direct lights only;
- finite reflectors individually toggled;
- local reflectors matte override;
- atmosphere only over a neutral target scene;
- no-atmosphere full scene;
- road dry substrate;
- road surface-state layer;
- no-post beauty;
- final display-referred reference.

Level 0 does not need atmosphere, wetness, or post-effect captures because those
systems should be absent.

## 7. F40 windshield diagnostic environment

For the observed symmetric triangular windshield patches, use the restrained
corridor before adding complex weather:

1. duplicate the windshield non-destructively;
2. use a plain opaque grey material;
3. compare geometric, imported custom split, and recalculated normals;
4. use broad asymmetric finite reflectors on left/right;
5. retain an open neutral World and metric road;
6. orbit the camera and move the environment separately;
7. reintroduce specular, then transmission, then tint/normal/roughness inputs;
8. test Cycles first and EEVEE only after the fault source is isolated;
9. record whether patches remain topology-, loop-normal-, tangent-, attribute-,
   overlap-, view-, light-, or engine-linked.

Avoid procedural clouds, rain, droplets, glare, and dense HDRI reflections until
this isolation pass is complete. Complexity can mask whether the fault belongs to
geometry, loop normals, overlapping shells, vertex attributes, or material inputs.

## 8. HDRI intake

Store HDRIs outside Git unless an approved asset policy says otherwise. Record:

- source and licence;
- checksum;
- projection and dimensions;
- encoding/colour interpretation;
- sun clipping status;
- rotation/horizon;
- lower hemisphere;
- processing history;
- accepted roles;
- visible defects.

Never derive the local filename from an untrusted remote path without
sanitization.

An HDRI enters Level 1 only after the Level 0 corridor has established that the car
itself is not producing the artefact being investigated.

## 9. Road intake/build

Record:

- construction class;
- metric texture bands;
- scene transform/scale;
- profile/camber;
- drainage field;
- wear/traffic paths;
- surface-state history;
- scan/procedural provenance;
- LOD ownership.

Wet variants derive from the same base road and topography rather than becoming
unrelated materials. The Level 0 road is deliberately plain; detailed asphalt is
not required for glass diagnosis.

## 10. Atmosphere build

Use a bounded volume for controllable local fog/haze studies. Record:

- exact bounds;
- scattering/absorption inputs;
- density field;
- anisotropy;
- engine volume settings;
- visibility targets;
- no-volume reference.

World volume or compositor mist can be used only with explicit role labels.
Atmosphere belongs at Level 2 or later unless it is the direct experiment target.

## 11. Weather build

Weather is introduced after dry geometry/material qualification.

Required order:

1. cloud/illumination state;
2. atmospheric visibility;
3. precipitation field;
4. ground accumulation and drainage;
5. vehicle collision/spray;
6. windshield/body water;
7. camera/lens contamination;
8. post effects.

Wind and recent-weather history must be shared inputs where relevant. Each system
requires an off state and diagnostic output.

## 12. Camera lock

For comparative renders, lock:

- camera pose and lens;
- exposure;
- white balance;
- colour management;
- shutter;
- depth of field;
- post stack.

Any unlocked field becomes an experiment variable and is recorded.

## 13. Performance and complexity record

For each promoted environment, capture:

- render engine and device;
- viewport responsiveness;
- render time and samples;
- peak memory where available;
- HDRI dimensions;
- volume bounds and settings;
- displaced/instanced geometry counts;
- weather-particle counts;
- known denoiser or temporal artefacts.

A physically motivated system that prevents iteration is not automatically the
right production representation.

## 14. Validation

Run the repository validator after adding profiles or schema-backed records:

```text
virtualauto validate
python -m unittest discover -s dev/tests -v
```

Then run Blender-specific diagnostics through the established Blender workflow
and MCP bridge. A green repository validator proves structural consistency, not
that Blender built or rendered the environment correctly.

## 15. Evidence package

An executed profile should eventually produce:

```text
environment profile JSON
Blender runtime manifest
source-asset checksums
builder/import logs
contribution renders
scene-linear diagnostic output
display-referred reference
observations
claims/decisions
known limitations
performance record
```

Private or copyrighted source assets remain outside Git. Repository evidence
records may retain checksums and lawful small diagnostics according to policy.

## 16. Promotion states

```text
P0-idea
-> P1-specified
-> P2-buildable
-> P3-executed
-> P4-observed
-> P5-production-qualified
```

A profile cannot jump from written research to `P5`. The exact Blender version,
render engine, builder or scene source, retained diagnostics, and named role are
required.