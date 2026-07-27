# Blender 5.0.1 environment implementation cards

These cards are implementation contracts, not claims of live execution. They
use Blender `5.0.1` terminology from official documentation and must be checked
against the live API before a builder script is promoted.

Each card states ownership, node intent, diagnostics, and rejection conditions.
Values are deliberately not supplied as universal presets.

---

## ENV-WORLD-NISHITA-B50

### Purpose

Analytic clear-sky world radiance using Blender Sky Texture in Nishita mode.

### Ownership

- far-field sky radiance;
- optional visible solar disc;
- broad clear-sky molecular/aerosol/ozone appearance.

Does not own:

- local fog or aerial perspective through finite scene depth;
- clouds;
- terrain horizon;
- vehicle spray or dust;
- a separate Sun light unless explicitly calibrated.

### Node contract

```text
Texture Coordinate / Mapping policy
    -> Sky Texture [Nishita]
    -> Background
    -> World Output Surface
```

Record Sky Texture properties:

- Sun Disc support/state;
- Sun Size;
- Sun Intensity;
- Sun Elevation;
- Sun Rotation;
- Altitude;
- Air;
- Dust;
- Ozone.

Record Background Strength separately.

### Required diagnostics

- world-only diffuse grey;
- world-only chrome;
- zenith/horizon exposure bracket;
- visible sun-disc check;
- car orbit/turntable;
- recorded render engine.

### Reject when

- a separate Sun points elsewhere;
- exposure is used to hide a clipped/overbright setup without a capture rationale;
- Air/Dust/Ozone are labelled as measured physical units;
- local distance haze is attributed to the World surface alone.

---

## ENV-WORLD-HOSEK-B50

### Purpose

Compact analytic daylight using Hosek/Wilkie sky model.

### Node contract

```text
Sky Texture [Hosek/Wilkie]
    -> Background
    -> World Output Surface
```

Record:

- Sun Direction;
- Turbidity;
- Ground Albedo;
- Background Strength;
- world rotation policy.

### Diagnostic emphasis

- high versus low sun;
- low versus high turbidity;
- dark versus bright ground albedo;
- comparison against Nishita at matched sun direction and exposure.

### Reject when

- Ground Albedo is used in place of actual road/terrain geometry;
- Turbidity is reported as aerosol optical depth;
- the model family is changed after material tuning without rerunning material
  qualification.

---

## ENV-WORLD-HDRI-B50

### Purpose

World-space image-based lighting and/or visible environment.

### Node contract

```text
Texture Coordinate [Generated policy not assumed]
    -> Mapping / Vector Rotate
    -> Environment Texture
    -> Background
    -> World Output Surface
```

The Environment Texture node owns projection-aware environment sampling. The
file's encoding and projection must be known.

### Required metadata

- asset ID and checksum;
- rights state;
- projection;
- colour-space/encoding interpretation;
- world rotation;
- strength;
- sun clipped/unclipped/unknown;
- role: lighting, reflection, camera, or reference;
- lower-hemisphere treatment.

### Required diagnostics

- chrome and rough spheres;
- direct-shadow test;
- exposure bracket around sun;
- horizon-level overlay;
- moving glossy vehicle;
- local-parallax failure check;
- HDRI-only versus added-Sun split.

### Reject when

- Image Texture is used as an unexplained substitute;
- a display-referred map is treated as scene-linear radiance;
- the HDRI sun and Sun light are added without ownership analysis;
- material roughness is tuned before map bandwidth/clipping is checked.

---

## ENV-DIRECT-SUN-B50

### Purpose

Controllable directional direct illumination and shadows.

### Ownership

- direct solar-like illumination;
- shadow direction and angular softness.

### Object contract

```text
Light object: Sun
rotation -> shared astronomical direction
angle -> angular-source proxy
energy -> calibrated or artist-default direct component
```

### Required diagnostics

- shadow direction compared with sky disc/HDRI sun;
- shadow penumbra ruler;
- direct-only diffuse and chrome;
- world-only/direct-only/combined render;
- no-light environment map comparison.

### Reject when

- direction does not match the intended sun;
- the environment already owns an unmodified high-energy sun and no calibration
  record exists;
- arbitrary energy changes are compensated by material albedo/roughness.

---

## ENV-LOCAL-ATMOSPHERE-B50

### Purpose

Bounded haze, fog, smoke, or neutral extinction through a finite region.

### Node contract

Preferred initial test forms:

```text
Volume Scatter + Volume Absorption
    -> Add Shader
    -> Material Output Volume
```

or, after version/socket verification:

```text
Principled Volume
    -> Material Output Volume
```

Record:

- volume dimensions and transform;
- density field units/proxy;
- scattering colour;
- absorption colour;
- anisotropy;
- engine volume steps/resolution/bounces;
- clipping/start/end settings where applicable.

### Required diagnostics

- no-volume reference;
- known-distance black/white targets;
- scattering-only, absorption-only, and combined;
- headlight beam;
- windshield and paint reflection comparison;
- Cycles/EEVEE divergence.

### Reject when

- a world volume is claimed as a complete planetary atmosphere;
- density is recorded without volume scale;
- compositor mist substitutes for the volume in a physical validation claim;
- EEVEE camera-volume appearance is assumed to exist identically in glossy
  reflections or refractions.

---

## ENV-ROAD-DRY-B50

### Purpose

Metric dry asphalt/concrete baseline with separated scale bands.

### Ownership

- substrate colour and material class;
- binder/paste and aggregate response;
- microtexture, macrotexture, megatexture, and profile;
- cracks, joints, markings, and contamination.

### Shader/geometry contract

```text
world-space coordinates
    -> construction/process masks
        -> substrate albedo
        -> micro roughness
        -> micro normal
        -> fine displacement

geometry/displacement
    -> aggregate macrotexture
    -> joints, patches, ruts, profile

Principled BSDF
    -> Material Output Surface
```

### Required controls

- declared metric aggregate scale;
- binder/aggregate coverage;
- traffic polish;
- construction direction;
- contamination masks;
- displacement ownership by scale;
- LOD policy.

### Diagnostics

- top orthographic metric grid;
- grazing light;
- tyre contact;
- black-gloss lower-body reflection;
- moving camera for tiling/pop;
- normal/displacement/roughness isolation.

### Reject when

- one noise node owns every scale;
- object scaling changes apparent aggregate size;
- normal detail creates features that should affect contact/silhouette;
- visible road and reflected ground disagree.

---

## ENV-ROAD-WET-LAYER-B50

### Purpose

Add moisture and surface-water state without replacing the dry substrate model.

### Ownership split

```text
substrate moisture
    -> darker/saturated pore response

thin water film
    -> dielectric reflection/transmission proxy

standing water geometry
    -> local smooth/disturbed surface

flow/accumulation field
    -> coverage and thickness proxy
```

### Required inputs

- base dry material;
- topographic low points;
- slope/flow field;
- rain/recent-weather state;
- porosity/permeability proxy;
- traffic disturbance;
- water-surface roughness/disturbance.

### Diagnostics

- dry/damp/wet/ponded sequence at fixed exposure;
- Fresnel/grazing response;
- low-point mask;
- water-only pass;
- road-substrate-only pass;
- tyre-spray source mask;
- lower-body reflection.

### Reject when

- wetness is only lower roughness;
- water is metallic;
- puddles appear on crowns without a barrier/source;
- the substrate disappears under an opaque paint-like layer;
- wet masks are camera-projected rather than scene-space without disclosure.

---

## ENV-DUST-DEPOSITION-B50

### Purpose

Scene-space deposited dust/road film on vehicles and environment.

### Inputs

- upward orientation;
- cavity/exposure fields;
- airflow/wake region proxy;
- wheel/splash proximity;
- cleaning/wipe masks;
- water flow and evaporation edges;
- deposition history;
- world-space dust scale.

### Outputs

- albedo change;
- roughness change;
- micro-normal or thickness proxy;
- coverage mask;
- optional loose-particle instances at visible scale.

### Diagnostics

- coverage-only view;
- cavity field versus final deposition;
- clean baseline;
- rain/wipe response;
- moving vehicle/rear wake plausibility.

### Reject when

- ambient occlusion is used directly as final dust coverage;
- every cavity accumulates equally despite water/airflow;
- dust ignores cleaning, touch, or tyre spray;
- settled dust is also rendered as suspended volume without an emission event.

---

## ENV-RAIN-STREAKS-B50

### Purpose

Near/mid-field falling rain visible through shutter integration.

### Geometry/particle contract

- world-space drop positions;
- gravity and wind velocity;
- camera shutter/motion blur;
- depth and occlusion;
- size distribution proxy;
- lighting response;
- culling/LOD.

### Diagnostics

- zero-shutter reference;
- velocity-vector view;
- camera-static versus camera-moving;
- crosswind variation;
- depth-of-field variation;
- ground collision and splash isolation.

### Reject when

- streaks are fixed to camera while represented as scene rain;
- all drops share one length independent of depth/velocity;
- rain remains visible through solid occluders;
- road and vehicle state stay dry indefinitely.

---

## ENV-WINDSHIELD-WATER-B50

### Purpose

Curved-glass water coverage, droplet motion, coalescence, and wiper response.

### Data ownership

- windshield-local UV or surface coordinates;
- world gravity transformed to surface tangent;
- vehicle acceleration and orientation;
- aerodynamic shear proxy;
- adhesion/contact-angle proxy;
- wiper swept field;
- drainage boundaries;
- optical thickness/normal field.

### Diagnostics

- stationary level vehicle;
- acceleration, braking, and cornering cases;
- crosswind;
- wiper single sweep and intermittent cycle;
- exterior/interior camera;
- reflection/refraction and alpha isolation;
- no-droplet glass baseline.

### Reject when

- droplets move in screen space;
- symmetrical motion persists under asymmetric acceleration/wind;
- wipers only erase alpha without displaced water/residual film when visible;
- water normals hide source windshield normal defects.

---

## ENV-DEBUG-PASSES-B50

### Purpose

Make environment contributions independently inspectable.

Minimum debug outputs or material overrides:

- world radiance only;
- direct lights only;
- local volume only;
- cloud shadow/coverage;
- surface moisture;
- standing-water mask/depth proxy;
- terrain slope/curvature/flow;
- road scale bands;
- dust deposition;
- precipitation velocity;
- object/material IDs;
- geometric normals and imported/custom normals;
- depth and Mist Pass, clearly labelled;
- exposure/colour-management record.

### Rule

A viewport switch accelerates iteration but does not replace retained evidence
renders or machine-readable parameters.

---

## ENV-PROFILE-COMPILER-B50

### Purpose

Future deterministic builder from a machine-readable environment profile.

### Required behaviour

- version guard Blender `5.0.1` production target;
- fail on missing/renamed node types or sockets;
- write only owned objects/materials/collections;
- preserve user scene content unless explicitly targeted;
- record every generated datablock;
- attach source/provenance IDs;
- expose seed and world-space scale;
- generate debug views;
- support clean rebuild and diff;
- never invent unresolved physical values.

### Status

`HYP / NOT IMPLEMENTED`. A schema and builder belong in a separate reviewed
change after the environment research structure is accepted.