# Environment workflow

This workflow turns reviewed environment research into controlled Blender scenes
without treating artistic success as physical validation.

Production baseline: Blender `5.0.1`.

## 1. Select the role

State what the environment is for:

- vehicle material qualification;
- Class-A/reflection-line diagnosis;
- glass/normal forensics;
- exterior hero render;
- weather interaction;
- EEVEE performance profile;
- camera/backplate integration.

One environment may support several roles, but acceptance is evaluated per role.

## 2. Create a profile

Copy the structure demonstrated by
[`lab/examples/environment_profile.json`](../../lab/examples/environment_profile.json)
and validate it against
[`environment-profile.schema.json`](../../lab/schemas/environment-profile.schema.json).

Do not fill unresolved values with plausible guesses. Each parameter records:

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
3. sky/HDRI;
4. direct sun or other emitters;
5. finite local reflectors and horizon;
6. road/terrain material scale bands;
7. bounded atmosphere;
8. weather and surface-state systems;
9. camera/post effects;
10. hero vehicle.

Do not begin with the final beauty stack.

## 5. Required diagnostic collections

Create or link clearly named collections for:

```text
ENV_DIAGNOSTICS
ENV_WORLD
ENV_DIRECT_LIGHTS
ENV_LOCAL_REFLECTORS
ENV_ATMOSPHERE
ENV_ROAD
ENV_TERRAIN
ENV_WEATHER
ENV_CAMERA_POST
```

This naming is a workflow suggestion, not a Blender API contract. A future
builder may use different generated names, but ownership must remain queryable.

## 6. Contribution captures

Retain at least:

- world only;
- direct lights only;
- local reflectors matte override;
- atmosphere only over a neutral target scene;
- no-atmosphere full scene;
- road dry substrate;
- road surface-state layer;
- no-post beauty;
- final display-referred reference.

## 7. F40 windshield diagnostic environment

For the currently observed symmetric triangular windshield patches, use a
restrained environment before adding complex weather:

1. duplicate the windshield non-destructively;
2. use a plain opaque grey material;
3. compare geometric, imported custom split, and recalculated normals;
4. use broad asymmetric finite reflectors on left/right;
5. retain an open sky and metric road;
6. orbit the camera and rotate the environment separately;
7. reintroduce specular, then transmission, then tint/normal/roughness inputs;
8. test Cycles and EEVEE only after the fault source is isolated;
9. record whether patches remain topology-locked, view-locked, light-locked, or
   attribute-locked.

Avoid procedural clouds, rain, droplets, glare, and dense HDRI reflections until
this isolation pass is complete. Complexity can mask whether the fault belongs
to geometry, loop normals, overlapping shells, vertex attributes, or material
inputs.

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
unrelated materials.

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

Wind and recent-weather history must be shared inputs where relevant.

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

## 13. Validation

Run the repository validator after adding profiles or schema-backed records:

```text
virtualauto validate
python -m unittest discover -s dev/tests -v
```

Then run Blender-specific diagnostics through the established Blender workflow
and MCP bridge. A green repository validator proves structural consistency, not
that Blender built or rendered the environment correctly.

## 14. Evidence package

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
```

Private or copyrighted source assets remain outside Git. Repository evidence
records may retain checksums and lawful small diagnostics according to policy.

## 15. Promotion states

```text
P0-idea
-> P1-specified
-> P2-buildable
-> P3-executed
-> P4-observed
-> P5-production-qualified
```

A profile cannot jump from written research to `P5`. The exact Blender version,
render engine, builder or scene source, and retained diagnostics are required.