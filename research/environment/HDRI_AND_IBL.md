# HDRI and image-based lighting

## 1. Scope

High-dynamic-range environment maps can provide measured or captured directional
radiance for image-based lighting. They are powerful because automotive
materials need broad, structured radiance over the full sphere. They are also
easy to misuse because a file labelled `HDRI` may still be clipped, stitched,
blurred, graded, incorrectly transformed, or spatially incompatible with the
scene.

`PRIMARY`: image-based lighting as established by Debevec uses captured HDR
scene radiance to illuminate synthetic objects in a corresponding environment.
The method does not imply that every internet panorama is a calibrated
radiometric measurement.

## 2. Required asset record

Every environment map considered for production should record:

- source and rights status;
- file format and checksum;
- pixel dimensions and projection;
- bit depth and channel encoding;
- declared colour space or transfer function;
- dynamic range or bracket information where available;
- whether the solar disc is clipped;
- capture time, location, weather, and camera orientation where available;
- white-balance and exposure processing;
- stitching, ghosting, tripod removal, denoising, or retouching;
- visible horizon height and roll;
- intended use: lighting, reflections, visible background, or reference only.

A filename is not provenance.

## 3. Dynamic range

Outdoor daylight can contain an extreme ratio between the sun and shaded
surfaces. If the solar region is clipped, the map can still provide useful broad
reflections but may not generate correct direct shadows or glints.

Indicators of inadequate range:

- sun pixels plateau at one value across a large area;
- sun intensity changes little when exposure is lowered;
- chrome reflections show a broad white patch rather than a compact high-energy
  source;
- hard shadows are missing despite a visibly clear sun;
- metallic flakes and narrow clearcoat glints require artificial gain.

`VA-RULE`: do not compensate for a clipped sun by raising the entire HDRI
strength. This raises sky and ground energy as well.

## 4. Projection and sampling

Blender's Environment Texture node is intended for environment maps and handles
spherical projection in the World context. A generic Image Texture is not an
interchangeable substitute.

Common projections include:

- latitude-longitude/equirectangular;
- mirror ball/light probe;
- cube map;
- angular map.

Files must be interpreted according to their actual projection. Reprojection
can blur the sun, lose energy, or create seams.

## 5. Lighting versus visible background

One map does not have to own every role.

### Lighting map

Prioritizes radiance fidelity and sampling. It can remain unclipped and visually
unattractive at display exposure.

### Reflection map

Prioritizes high-resolution structures seen in glossy paint and glass. It may
require local geometry to correct parallax.

### Background plate

Prioritizes camera-specific perspective, composition, and image quality. It may
be tone-mapped and should not automatically illuminate the scene.

### Local reconstruction

Finite geometry for road, walls, trees, buildings, gantries, lamps, and other
near-field structures.

A robust automotive setup may use all four, with ownership recorded.

## 6. Parallax and spatial validity

An HDRI encodes radiance by direction from one capture point. It does not encode
full scene depth.

Consequences:

- translation away from the capture point produces no parallax in the world map;
- nearby objects appear infinitely distant in reflections;
- windows and body panels can show spatially impossible alignments;
- contact shadows and occlusion are absent;
- a long vehicle can sample directions that correspond to different real-world
  positions, but the map cannot adjust.

`VA-RULE`: reconstruct finite geometry for any feature whose parallax is visible
or whose shadow/occlusion matters to the shot.

## 7. Horizon and orientation

The environment map must be oriented using evidence, not only by placing a
pleasing highlight.

Record:

- world rotation;
- horizon pitch and roll;
- solar azimuth/elevation where identifiable;
- camera-forward direction;
- whether the ground hemisphere matches the reconstructed road;
- mirrored or flipped state.

A deliberately rotated HDRI is valid art direction, but it is no longer a
camera-registered reconstruction unless the scene is rotated with it.

## 8. White balance and colour management

Captured radiance may be processed through camera white balance, matrixing,
lens corrections, stitching software, and grading.

Potential failures:

- a warm map is counteracted by a cool camera white balance, making material
  colour look neutral for the wrong reason;
- display-referred JPEG pixels are treated as linear radiance;
- an EXR has already been chromatically adapted or graded but is described as
  raw;
- visible background and lighting map use different colour transforms.

`VA-RULE`: environment maps enter the renderer as scene-linear data only when
their encoding supports that interpretation. Display transforms remain at the
camera/output stage.

## 9. Sun separation and double counting

### Unmodified HDRI plus Sun light

This is the easiest way to double count direct solar energy. The HDRI still
contains the sun while a second source casts shadows.

### Sun removed from HDRI plus Sun light

Potentially controllable, but removing the sun must preserve surrounding sky
and avoid a dark or blurred hole. The processing becomes part of provenance.

### HDRI sun only

Potentially faithful when the source is unclipped and well sampled. It can be
noisy and may not provide desired angular control.

### Analytic sky plus local captured structures

Useful when atmospheric state must be controllable but local reflection
structure comes from reference photography or geometry.

No pattern is universally correct. Each requires diagnostic renders.

## 10. Ground hemisphere

Many HDRIs contain an actual ground, a patched tripod region, a blurred nadir,
or an artificial lower hemisphere. This directly affects:

- rocker-panel and lower-door reflections;
- wheel and tyre readability;
- glass lower-hemisphere reflection;
- apparent ground bounce;
- underside illumination.

A real road plane combined with a mismatched HDRI ground can create duplicate
horizons and impossible lower-body reflections.

Possible ownership patterns:

- retain HDRI ground for lighting but hide it from camera;
- replace lower hemisphere with calibrated ground radiance;
- use light-path separation cautiously and document the non-physical result;
- build local geometry and use the HDRI mainly for upper-hemisphere radiance.

## 11. Resolution and highlight bandwidth

Automotive clearcoat and polished metal respond to small, high-contrast sources.
Map resolution therefore affects:

- highlight edge definition;
- lamp and window reflection detail;
- sun angular size;
- sparkle activation;
- aliasing in motion.

A blurred environment can make a physically plausible material appear too
rough. Material roughness must not be reduced to compensate until the source
radiance bandwidth is checked.

## 12. Capture defects

Inspect for:

- moving-cloud or foliage ghosts between brackets;
- stitching discontinuities crossing the horizon or sun;
- duplicated vehicles or people;
- chromatic seams;
- clipped channels;
- denoising or sharpening halos;
- tripod/nadir paint-out;
- exposure inconsistencies between sectors;
- lens flare baked into the panorama;
- weather changes during capture.

These defects can become large moving reflections over car bodywork.

## 13. Sampling and renderer controls

The environment map is part of the Monte Carlo sampling problem.

Diagnostics should record:

- world strength;
- multiple importance sampling or equivalent behaviour;
- sample count;
- caustic and glossy settings;
- clamp values;
- denoiser;
- sun extraction strategy;
- firefly suppression;
- engine and version.

Clamping can suppress the very peaks that make an HDRI useful for automotive
highlights.

## 14. Rights and storage

VirtualAuto may reference CC0 or appropriately licensed HDRIs, but the repo does
not automatically vendor large environment files.

Preferred record:

```text
asset ID
source URL
licence
source checksum
local checksum
capture metadata
processing history
approved roles
known defects
```

Poly Haven is one possible CC0 source, not an automatic guarantee that every map
fits a scene or preserves an unclipped sun.

## 15. Qualification rig

For each HDRI candidate render:

- chrome sphere;
- 18% diffuse-grey sphere/card;
- rough dielectric sphere at several roughness values;
- black glossy curved panel;
- clear glass slab and curved windshield proxy;
- metallic-flake and solid-paint panels;
- road plane with neutral diffuse response;
- vehicle turntable or camera orbit.

Capture at least:

- default orientation;
- sun-aligned orientation;
- one 90-degree rotation;
- source-only;
- extracted/direct-light-only;
- combined lighting;
- camera-visible and lighting-only variants.

## 16. Acceptance questions

1. Is the sun clipped?
2. Are luminance ratios plausible enough for the intended use?
3. Is the horizon level and spatially compatible?
4. Are lower-hemisphere reflections usable?
5. Are stitching defects visible on a car in motion?
6. Does the map create sufficient reflection structure without material cheating?
7. Is local parallax required?
8. Can the environment be reconstructed from a fresh file?
9. Are rights and processing history known?
10. Does the setup maintain consistent exposure and white balance across
    validation environments?

A map can be accepted for reflections while rejected for direct illumination or
visible background. Acceptance is role-specific.