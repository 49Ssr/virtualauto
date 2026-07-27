# Camera, colour, and compositing boundaries

## 1. Environment appearance is camera-dependent

The rendered environment is not complete until radiance passes through camera,
exposure, colour management, and display. These stages can make a physically
reasonable scene appear dull, clipped, hazy, saturated, or colour-shifted—and
can make an incoherent scene appear temporarily convincing.

`VA-RULE`: environment and material records preserve scene parameters separately
from camera/display parameters.

## 2. Exposure

Exposure controls how scene-linear radiance is mapped into the captured image.
It does not change:

- atmospheric density;
- sun/sky energy ratio;
- surface reflectance;
- HDRI clipping already present in the source;
- water-film thickness;
- physical visibility.

Exposure does change:

- apparent brightness and colour after tone mapping;
- visible highlight clipping/roll-off;
- noise and volumetric readability;
- balance between sky, car, road, and artificial lights;
- motion-blur and depth-of-field choices when tied to a camera model.

Environment experiments fix exposure unless exposure is the tested variable.

## 3. White balance and chromatic adaptation

White balance is a camera/display interpretation of illuminant colour. It should
not be used to force manufacturer paint to a preferred RGB under every sky.

Record:

- scene illuminant/environment;
- white-balance or chromatic-adaptation setting;
- reference neutral target where used;
- whether HDRI/background was already white-balanced;
- intended photographic or perceptual goal.

Mixed daylight, fluorescent, LED, sodium, signs, and vehicle lamps may not admit
one globally neutral balance.

## 4. Colour management

The display transform shapes:

- highlight roll-off;
- saturation under high exposure;
- contrast of haze/fog;
- apparent paint hue and value;
- lamp and sun clipping;
- wet-road glare;
- shadow visibility.

A material/environment comparison must use the same colour-management state or
explicitly study the transform.

Retain scene-linear EXR evidence for diagnostic measurements where practical.
A display-referred screenshot is not a substitute for source-linear data.

## 5. Tone mapping and bright sources

Automotive scenes contain intense sources and reflections:

- sun disc;
- chrome glints;
- clearcoat peaks;
- headlamps;
- wet-road highlights;
- signs and street lights.

Tone mapping can compress these into similar display values even when their
scene-linear intensities differ greatly. Therefore:

- inspect exposure brackets;
- inspect scene-linear peak/percentile data;
- avoid judging HDRI sun fidelity from one tone-mapped frame;
- distinguish source clipping from display compression;
- test colour shifts in saturated highlights.

## 6. Camera lens and field of view

Lens choice alters environmental relationships:

- wide lenses exaggerate near-field parallax and road scale;
- long lenses compress horizon and terrain;
- camera height changes road dominance and horizon line;
- close vehicle perspectives magnify windshield and bonnet reflections;
- distortion can bend architecture and road markings.

Environment profiles should store camera height and pose, not only focal length.

## 7. Depth of field

Depth of field affects perception of:

- rain and dust particle size;
- foreground road texture;
- distant haze and terrain;
- highlight shape/bokeh;
- artificial lights;
- vegetation cards and LOD.

A blurred environment can hide geometric or procedural defects. Qualification
includes a deep-focus diagnostic even when the final shot is shallow.

## 8. Motion blur and shutter

Motion blur determines visible rain streaks, wheel motion, road texture flow,
vegetation motion, and camera shake.

Record:

- shutter interval/angle;
- frame rate;
- camera motion;
- object motion;
- deformation/particle motion support;
- rolling/global shutter assumption if relevant.

A still streak texture cannot be evaluated independently of shutter.

## 9. Lens flare and glare

Flare/glare can arise from:

- optical reflections between lens elements;
- sensor blooming/charge spread;
- diffraction;
- scattering by contamination or moisture;
- post-processing.

Blender compositor glare is an image-space effect. It may reproduce a desired
look, but it does not replace a finite emitter, atmospheric scattering, or
correct scene exposure.

`VA-RULE`: flare, bloom, glare, and starburst contributions are independently
toggleable and recorded.

## 10. Lens and sensor contamination

Rain, dust, fingerprints, and spray on the camera/lens differ from environmental
particles:

- they are near/imaged at the lens plane;
- often strongly defocused;
- move with lens/camera, gravity, wiping, or airflow;
- alter flare and contrast;
- do not cast normal scene shadows or occupy world depth.

A lens-droplet layer must not be reused as windshield or world rain.

## 11. Aerial perspective and compositor depth

A compositor can use depth or Mist Pass to create a distance fade. Advantages:

- cheap;
- controllable;
- useful for art direction and diagnostics.

Limitations:

- does not affect scene lighting transport;
- cannot naturally appear in glossy reflection/refraction;
- may mishandle transparency, depth discontinuities, and layered media;
- can ignore local lights and shadows;
- often uses one colour independent of view angle/spectrum.

Use it as a labelled post layer, not as evidence of physical atmosphere.

## 12. Backplates

A backplate is a camera-specific image. Requirements:

- known or estimated camera/lens/perspective;
- horizon and camera-height match;
- exposure and white-balance match;
- shadow and weather match;
- local geometry for receiving/casting interaction;
- separation from lighting map;
- rights/provenance.

A backplate can be perfect for one camera and invalid for an orbit.

## 13. Shadow catcher and differential compositing

Image-based insertion may use approximate local geometry to catch shadows and
reflected light. The method should preserve:

- clean plate;
- synthetic-only contribution;
- shadow/reflection differential;
- local ground reflectance estimate;
- camera and environment registration;
- compositing operation.

This is a reconstruction workflow, not proof that the background's physical
geometry/material was recovered exactly.

## 14. Atmospheric grading

Post grading can support depth and mood, but broad colour changes must not be
mislabelled as ozone, aerosol, or weather.

Separate controls for:

- global grade;
- distance-dependent grade;
- sky grade;
- local fog/haze pass;
- artificial-light bloom;
- lens contamination;
- vignette;
- film grain.

## 15. Manufacturer paint and camera response

A manufacturer paint name or reference chip does not correspond to one display
RGB value. Environment, angle, exposure, sensor spectral response, white
balance, tone mapping, and display transform affect appearance.

For paint validation:

- retain a controlled neutral environment;
- render multiple illumination/view angles;
- keep camera pipeline fixed;
- record any creative grade separately;
- do not tune physical material parameters against one graded beauty frame.

## 16. Environment-camera diagnostic matrix

| Test | Scene fixed | Camera variable | Purpose |
| --- | --- | --- | --- |
| exposure bracket | yes | exposure | reveal clipping and roll-off |
| white-balance bracket | yes | adaptation | separate illuminant from material colour |
| focal-length match | geometry registration | lens/pose | check parallax and horizon |
| deep/shallow focus | yes | focus/aperture | expose hidden environment defects |
| shutter sweep | motion fixed | shutter | rain/road/particle motion |
| grade bypass | yes | display transform | preserve scene-linear diagnosis |
| flare bypass | yes | compositor/lens effects | separate emitter/volume from post |

## 17. Failure signatures

- different environment variants use different exposure without record;
- HDRI is brightened globally to recover a clipped sun;
- white balance is altered per paint colour;
- tone mapping hides sky or lamp clipping;
- depth mist is visible in camera but absent in reflections while claimed physical;
- backplate horizon and road plane disagree;
- rain streaks are tuned without a shutter record;
- lens droplets cast world-space shadows;
- final grade is baked into albedo/HDRI and then graded again;
- denoising removes fine volumetric or rain signals without a reference pass.

## 18. Initial evidence package

Every accepted environment profile should retain:

- one scene-linear multilayer EXR or equivalent diagnostic output;
- display-referred reference render;
- exposure/white-balance/transform record;
- camera/lens/pose record;
- no-post render;
- no-volume render;
- world/direct contribution renders;
- post stack manifest;
- source assets and checksums;
- known clipping/noise/denoising limitations.