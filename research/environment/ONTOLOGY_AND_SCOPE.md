# Environment ontology and ownership

## 1. Why environment requires its own domain

Automotive appearance is strongly conditional. A surface does not carry a
complete visual identity by itself; it transforms incident radiance according
to geometry, material structure, viewing direction, wavelength, and camera
response. Environment therefore owns much of what is often misdiagnosed as a
paint, glass, or topology problem.

Examples:

- a clipped or low-dynamic-range sun produces weak metallic glints and false
  clearcoat tuning;
- an over-uniform world makes Class-A curvature look flat even when geometry is
  sound;
- an incoherent horizon can make glass appear too dark or too reflective;
- excessive volumetric extinction can erase reflection contrast and encourage
  physically implausible material compensation;
- a road with only high-frequency bump lacks the macrostructure that anchors
  wheel scale and suspension height;
- a wet road without drainage logic reads as polished plastic.

`VA-RULE`: material qualification must state the environment profile used.

## 2. Ownership graph

```text
astronomical state
    -> solar/lunar direction and angular extent
    -> atmospheric state
        -> sky radiance
        -> direct-beam attenuation
        -> aerial perspective
        -> visibility
    -> weather state
        -> cloud field
        -> precipitation
        -> wind
        -> accumulation / evaporation / melt
    -> terrain and built environment
        -> horizon and occlusion
        -> road and soil response
        -> local reflection structure
    -> vehicle and camera
        -> reflected/transmitted radiance
        -> exposure, lens, sensor, display
```

No node group or scene collection should own this entire graph. VirtualAuto
splits it into contracts with explicit inputs and outputs.

## 3. Spatial scale bands

Environment authoring must survive several scale bands simultaneously.

| Scale | Typical ownership | Automotive consequence |
| --- | --- | --- |
| sub-millimetre | road microtexture, dust grains, water menisci | grazing sparkle, friction cues, highlight breakup |
| millimetres to centimetres | aggregate, cracks, chips, droplets, tyre marks | local roughness, contact realism, spray initiation |
| decimetres to metres | potholes, kerbs, puddles, drainage, vegetation | wheel grounding, suspension scale, near reflections |
| tens to hundreds of metres | road camber, embankments, buildings, tree masses | horizon motion, parallax, occlusion, lighting structure |
| kilometres | terrain profile, haze depth, cloud layers | aerial perspective and scene scale |
| planetary | sun position, atmospheric optical path | sky colour, irradiance, shadow direction |

`VA-RULE`: texture scale is recorded in scene units. A noise scale chosen by eye
without world-space interpretation is an artist default, not a physical value.

## 4. State dimensions

A reusable environment profile should eventually expose, at minimum:

### 4.1 Astronomical

- location or abstract latitude;
- date/time or explicit sun elevation and azimuth;
- solar angular size policy;
- moon and stars when relevant.

### 4.2 Atmospheric

- sky-model family;
- molecular-scattering control;
- aerosol loading and type hypothesis;
- ozone control;
- local extinction and anisotropy;
- vertical and horizontal visibility targets.

### 4.3 Meteorological

- cloud class and coverage;
- precipitation type and intensity;
- wind vector and gust model;
- temperature only when it affects phase/state;
- recent weather history, not only the current frame.

### 4.4 Ground

- substrate class;
- texture scale bands;
- slope/camber and drainage;
- contamination and wear;
- moisture and ponding state;
- road-marking construction and age.

### 4.5 Capture

- render engine and version;
- exposure and white balance;
- colour-management transform;
- shutter and motion-blur policy;
- visible background source;
- lighting source;
- reflection and volumetric diagnostics.

## 5. Environment profiles versus scenes

An environment profile is a controlled state description. A scene is one
implementation of that profile.

```text
ENV-PROFILE-DRY-CLEAR-01
    -> sky and sun contract
    -> atmosphere contract
    -> road state contract
    -> local reflector layout
    -> camera qualification settings
```

Several scenes may implement the same profile at different performance levels.
A profile must not contain Blender object names as its only semantics.

## 6. Physical layers versus art-direction layers

VirtualAuto permits art direction, but it must be separable from physical
ownership.

| Layer | Examples | Rule |
| --- | --- | --- |
| physical approximation | sky radiance, bounded fog, water film, terrain slope | parameter provenance and limitations required |
| production approximation | low-order cloud shadow, tiled road, impostor trees | visual and performance acceptance criteria required |
| art direction | highlight card, selective haze, background grade | must be labelled and disable-able |
| camera/display | exposure, tone mapping, bloom, vignette | cannot be used to rewrite scene energy silently |

A reflection card can be valid in automotive imagery. It becomes misleading
only when represented as naturally occurring environmental radiance or when it
hides a material failure.

## 7. Far field, near field, and parallax

A world shader is effectively infinitely distant. It supplies direction-dependent
radiance but no local parallax, contact shadow, or finite-distance occlusion.
Therefore:

- the visible world can light broad body curvature;
- it cannot replace nearby walls, trees, road furniture, gantries, or a studio
  cyclorama when those features should move through reflections;
- a backplate can match one camera but fail in windows and paint from another;
- local geometry must carry the spatial structures that reveal vehicle form.

`VA-RULE`: every HDRI-based scene declares which visible structures are
represented by finite geometry and which remain infinitely distant.

## 8. Time and history

Weathered state depends on history:

```text
recent rain + current sun
    != dry scene with raindrops added
```

Relevant memory includes:

- duration and intensity of prior rain;
- drainage and evaporation time;
- traffic disturbance;
- dust deposition since cleaning;
- snow compaction and melt/refreeze history;
- wind direction during deposition.

A single `wetness` scalar is acceptable only as a documented control proxy for
an explicitly limited shot.

## 9. Engine ownership

### Cycles

Use when reflected/refracted participation, multiple scattering, or coherent
hero-vehicle transport is important. A result is still only as physical as the
scene model and inputs.

### EEVEE

Use for iteration and production where its known limitations are acceptable.
Environment qualification must specifically test reflection, refraction,
volume, probe, transparency, and shadow divergences from Cycles.

### Compositor

Owns image-space effects and grading. Depth mist, glare, atmospheric tint, and
rain-on-lens effects implemented here are not promoted to scene-space physics.

## 10. Minimum environment acceptance gate

Before a scene becomes a material-validation environment it must provide:

1. recorded world and direct-light ownership;
2. no accidental sun double counting;
3. known horizon and scale;
4. road/ground scale references;
5. a declared atmosphere/visibility state;
6. camera, exposure, and colour-management record;
7. chrome, diffuse-grey, rough dielectric, black-gloss, and glass diagnostics;
8. still and motion checks;
9. Cycles/EEVEE divergence notes where both are supported;
10. a fresh-file reconstruction or deterministic builder path.

Passing this gate does not prove atmospheric or meteorological accuracy. It
proves that the environment is controlled enough to diagnose an automotive
asset.