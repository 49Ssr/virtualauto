# Real camera and atmosphere pipeline

This document connects the environment research to an executable Blender camera
pipeline. It does not claim that Blender's perspective camera and stock
compositor reproduce a multi-element photographic lens.

## Ownership

The active order is:

```text
far-field sky radiance and direct sun
-> bounded local participating medium
-> surfaces, reflections, refractions, and shadows
-> scene-linear Cycles result
-> Monte Carlo denoising
-> calibrated lens geometry and lateral chromatic aberration
-> measured point-spread function and veiling glare
-> sensor model
-> chromatic adaptation and display transform
```

Changing the order changes the model. In particular:

- Mist Pass is a depth-derived mask, not participating-media transport;
- compositor glare is not a substitute for in-scattering;
- lens bloom must not be baked into material emission or paint glints;
- denoising belongs before synthetic lens and sensor defects;
- display grading must not rewrite scene-lighting parameters.

## Sky and local atmosphere

Sky Texture supplies far-field sky radiance and, when its sun disc is enabled,
the direct solar source. A `Background` closure makes this World ownership
explicit.

Local haze or mist is a closed, bounded object containing a volume shader. It is
illuminated by the same sky and sun as the car. Consequently it can affect:

- light arriving at the vehicle;
- camera-to-surface transmittance;
- in-scattering toward the camera;
- reflections and refractions that traverse the medium;
- the apparent horizon and sky seen through the volume.

The bounded medium should use per-distance coefficients when available. Blender
5.x `Volume Coefficients` exposes absorption and scattering coefficients in a
form intended for real-world measurements. A visibility-controlled prior may use

```text
beta_ext = 3.912 / visibility_m
beta_sca = beta_ext * single_scatter_albedo
beta_abs = beta_ext * (1 - single_scatter_albedo)
```

This is an implementation relation with an implicit two-percent contrast
threshold. It does not infer aerosol composition, particle size, vertical
structure, or spectral behaviour from visibility alone.

For water-droplet mist, Blender's Mie phase-function mode is a better semantic
starting point than tinting a generic fog colour. Particle diameter, extinction,
single-scatter albedo, and height profile remain target-dependent inputs.

## Mist Pass

Mist Pass remains useful for:

- inspecting depth ranges;
- producing a clearly labelled art-direction matte;
- comparing the volume result against a cheap proxy;
- locating transparency and depth-discontinuity failures.

It is not accepted as the physical atmosphere because it does not participate in
lighting transport. The active beauty graph must not mix it over the render.

## Camera fidelity tiers

### Tier 0 — ideal rectilinear camera

Use verified sensor dimensions, focal length, pose, aperture, focus, shutter,
and render resolution. Keep distortion, transverse chromatic aberration,
vignetting, flare, and PSF neutral when no measured profile exists.

This is more honest than applying arbitrary imperfections.

### Tier 1 — calibrated image-space camera

Use a measured calibration such as Lensfun or Blender Movie Distortion. The
profile must identify:

- camera or crop factor;
- lens and focal length;
- aperture and focus distance where required;
- distortion model and coefficients;
- transverse chromatic-aberration model and coefficients;
- vignetting model and coefficients;
- source version and provenance.

Blender's stock Lens Distortion node has one radial distortion factor and one
dispersion factor. It cannot faithfully encode Lensfun's polynomial distortion,
channel-specific TCA, and aperture/distance-dependent vignetting models. A real
Lensfun profile therefore requires a tested polynomial warp, Lensfun-backed
post-process, or a calibrated Movie Distortion workflow.

### Tier 2 — measured PSF and flare

Use measured or simulated point-spread kernels indexed by aperture, focus,
field position, and preferably wavelength. Blender 5.2's compositor Glare node
can accept a convolution kernel, but a generic Fog Glow remains an artistic
approximation.

### Tier 3 — traced multi-element lens

A real lens contains multiple refractive elements, apertures, mechanical stops,
and coatings. PBRT's `RealisticCamera` demonstrates the reference class: rays
are traced through an explicit lens prescription. Blender's perspective camera
is not this model. Use an external optical render or validated surrogate when
multi-element aberrations are required.

## F40 Blender 5.2 baseline

The active `F40_MCP.blend` implementation created on 2026-07-27 uses:

```text
World Sky Texture -> Background -> World Output Surface
VA_ENV_BoundedMist -> Material Output Volume (currently excluded from viewport/render)
Noisy Image + Denoising Albedo/Normal -> Denoise
-> optional calibrated 85 mm distortion/TCA/vignetting
-> neutral Lens Distortion fallback
-> qualified ideal f/8 diffraction kernel at 3840 x 2160
-> disabled unmeasured Fog Glow approximation
-> final output
```

The original `Camera2` remains an untouched ideal, uncalibrated full-frame
50 mm camera:

```text
sensor: 36 x 24 mm
focal length: 50 mm
distortion: neutral
TCA: neutral
vignetting: unset
PSF: unset
```

## F40 perspective and camera suite

`OBS-INSTRUMENT`, executed in Blender 5.2.0 LTS on 2026-07-27. The suite is
private scene evidence, not a claim that Blender reproduces the complete optical
behaviour of the named Canon lenses.

The live F40 scene now contains three non-destructive perspective candidates
derived from the original `Camera2` optical axis. Each aims at the same focus
target, `VA_F40_Focus_Hero`, while camera distance changes approximately in
proportion to focal length. This keeps subject scale broadly comparable and
makes perspective change, rather than a simple crop, the principal variable.

| Camera | Focal length | Target distance | Aperture | Blades | Intended role |
| --- | ---: | ---: | ---: | ---: | --- |
| `VA_CAM_5D4_35_CONTEXT` | 35 mm | 3.85 m | f/8 | 8 | assertive environmental/context view |
| `VA_CAM_5D4_50_HERO` | 50 mm | 5.50 m | f/8 | 7 | balanced front-quarter hero baseline |
| `VA_CAM_5D4_85_COMPRESSION` | 85 mm | 9.35 m | f/8 | 9 | compressed design/catalogue view |

All three use a 36 x 24 mm sensor gate, horizontal sensor fit, object-based
focus, and enabled thin-lens depth of field. Their metadata records a Canon EOS
5D Mark IV body and matching Canon EF prime-lens candidate. Canon's published
sensor size and lens aperture-blade counts support those fields. Lensfun commit
`698a39eea69be00f4f25b6da6c1ad34b1f162b50` supplies candidate distortion and
TCA profiles. The 35 and 50 mm profiles remain recorded but unapplied. The
matching 85 mm profile now has a separate polynomial compositor implementation;
it is active for the selected 85 mm camera and must be manually bypassed before
using either other camera.

The 960 x 540 / 32-sample comparison renders produced the following visual
observations:

- 35 mm enlarges the near nose and front wheel, strengthens depth, and gives the
  frame more advertising or action energy; it is least neutral for evaluating
  body proportions.
- 50 mm gives the most balanced hero framing; it was the initial suite baseline.
- 85 mm reduces near/far exaggeration and gives the cleanest design or catalogue
  reading; the user subsequently selected it as the active scene camera.

The suite does **not** pretend that one profile fits every camera. Only the 85 mm
candidate has an implemented distortion/TCA/vignetting stage. One ideal
circular-aperture diffraction component is active for f/8 at 3840 x 2160, but
no measured Canon lens PSF, sensor MTF, sensor noise, shutter response, white
balance, or camera response function is active. Blender depth of field remains
a thin-lens approximation. The
current 16:9 image is also a centred framing crop within the full-frame-width
camera model, not the native 3:2 still-image aspect ratio of the referenced
body.

The scene retains:

- `F40_MCP_pre_camera_suite.blend` as a checkpoint;
- `VA_CAMERA_SUITE_MANIFEST` as an embedded text record;
- the original `Camera2` without edits;
- private A/B renders under `VA_Evidence/CameraSuite_v1`.

## Qualified source-exact 85 mm Lensfun stage

`OBS-INSTRUMENT`, executed in Blender 5.2.0 LTS on 2026-07-27.

The optional stage targets only `VA_CAM_5D4_85_COMPRESSION` and the Lensfun
entry for Canon EF 85 mm f/1.4L IS USM at pinned commit
`698a39eea69be00f4f25b6da6c1ad34b1f162b50`. It reproduces the registered
Lensfun model classes rather than translating them into Blender's unrelated
single Distortion and Dispersion sliders:

```text
PTLens distortion at 85 mm:
  a = 0.00984
  b = -0.0325
  c = 0.0316

poly3 TCA at 85 mm:
  vr = 0.9999438
  vb = 0.9999330

PA vignetting interpolated at f/8 and 9.336846 m:
  k1 = -0.1757052864
  k2 = -0.0263920790
  k3 = 0.0396991339
```

Those are database parameters, not the final PTLens coefficients used by
Lensfun's modifier. Source audit of `modifier.cpp`, `mod-coord.cpp`,
`mod-subpix.cpp`, and `mod-color.cpp` at the pinned commit showed that Lensfun
first applies its coordinate normalization and focal-preserving coefficient
rescaling. For this profile, the rescaled PTLens coefficients are:

```text
a' =  3.6250027919958545
b' = -1.6751699595215340
c' =  0.22788978898810133
```

The first VirtualAuto map set incorrectly applied the database `a/b/c` values
directly. It passed visual calibration because the 85 mm effect is subtle, but
it was not source-exact. That V1 map set remains packed and marked superseded.
V2 then regenerated every map from a small `bpy`-free Python model of the
pinned equations, but its Blender adapter encoded pixel positions as
`x/(width-1)` and `y/(height-1)`. A dedicated Map UV identity test showed that
Blender 5.2 instead requires `(x+0.5)/width` and `(y+0.5)/height`: the former
convention produced 17.21 dB PSNR on the permanent 64 x 32 stress pattern,
while the pixel-centre convention reproduced the source exactly. V3 combines
the source-pinned Lensfun equations with that verified Blender convention and
freezes all four float32 pixel hashes in the camera contract. Both earlier
implementations remain packed and marked superseded.

Three packed 960 x 540 floating-point coordinate maps preserve channel-specific
reverse distortion/TCA. A fourth packed map stores scene-linear vignetting
transmission. Explicit Scale nodes expand those smooth fields to the compositor
Render Size operation domain before Map UV or multiplication. This avoids
storing several hundred megabytes of full-resolution maps while preserving the
final output domain.

Blender's Cycles UV pass convention stores U and V in red and green and a
constant value of one in blue. Map UV treated the first generated maps, whose
blue channel was zero, as invalid and returned black. Correcting blue to one
restored the remap. This failure is useful node-behaviour evidence: an RGB image
that visually contains valid U/V values is not automatically a valid Map UV
field.

Historical V1 evidence remains under `VA_Evidence/CameraPipeline_v2`, and V2
under `CameraPipeline_v4`. The qualified V3 evidence is under
`VA_Evidence/CameraPipeline_v5` and
contains:

- the same denoised scene-linear 3840 x 2160 EXR used by the V1 gate;
- V3 profile outputs with ideal diffraction bypassed and active;
- neutral and V3 straight-grid renders;
- a V3 flat-field render;
- centred and off-axis V3 hard-edge renders;
- numerical beauty and calibration reports.

Observed result: distortion and f/8 falloff are subtle but visible; the
calibrated TCA remains subpixel and was not amplified for effect. Relative to
V2, the corrected V3 beauty has a 34.59 dB PSNR, retains 86.80 percent of V2's
strong-edge gradient metric, and has a mean-luminance ratio of 0.99901. This is
not a new optical blur: it exposes the several-pixel edge-domain resampling
error that V2 introduced after its 960 x 540 map was expanded to 4K. On a 0.5
scene-linear flat field, V3 measured 0.50001 at centre and 0.41920 one pixel
inside each corner, a corner/centre ratio of 0.83839 consistent with the packed
map's 0.83787 extreme-corner sample plus interpolation. These are compositor
validation values, not optical MTF or physical transmission measurements.

The earlier full-resolution domain failure remains relevant: Map UV inherited
the 960 x 540 coordinate-map domain and produced an inset result in a black
canvas until explicit Render Size scaling was added. V3 retains that proven
domain adaptation.

The branch is now active through `LF85_09_CAMERA_SPECIFIC_MIX` at Factor 1 for
the current `VA_CAM_5D4_85_COMPRESSION`. Factor 0 is the required bypass before
using another camera. An attempted automatic factor driver was rejected after
Blender reported it invalid; no false automatic safety remains in the file.
This is an implemented and calibration-checked image-space stage, not a camera
response or full optical simulation.

## Qualified ideal f/8 diffraction stage

`OBS-INSTRUMENT`, executed in Blender 5.2.0 LTS on 2026-07-28.

The active 85 mm camera uses f/8 and an effective 3840 x 2160 output. For an
ideal circular aperture at the 550 nm reference wavelength, the first-zero Airy
diameter is:

```text
2.44 * wavelength * f-number = 10.736 micrometres
```

At a 36 mm-wide 3840-pixel output, one output pixel spans 9.375 micrometres on
the modeled sensor gate, so that diameter is approximately 1.145 output pixels.
A pixel-integrated 9 x 9 intensity kernel was generated and packed as
`VA_IDEAL_AIRY_F8_550NM_4K_9X9`. The finite kernel contains approximately
98.095 percent of the infinite ideal Airy energy before Blender's Convolve node
normalizes it to one. It is inserted after the qualified Lensfun geometry/TCA/
vignetting stage and before output.

This is **not** a measured Canon EF 85 mm f/1.4L IS USM PSF. It models only the
ideal circular-aperture diffraction component. The real lens has nine aperture
blades, but no official f/8 pupil shape, field-dependent PSF, optical
prescription, or measured f/8 MTF was found. Canon's published MTF explanation
states that its current lens MTF charts are measured wide open, so those charts
cannot be repurposed as an f/8 convolution kernel. The EOS 5D Mark IV is
documented as having an optical low-pass filter, but its transfer function,
CFA/demosaic response, and capture sharpening are unknown and therefore remain
unset.

Two gates were passed:

1. A 64 x 64 synthetic impulse recovered all 81 kernel coefficients and total
   normalized energy of 1.0 from Blender's Convolve node.
2. The same denoised scene-linear 3840 x 2160 F40 EXR was processed through
   the source-exact Lensfun/Map UV V3 stage with the
   kernel bypassed and active. The active result retained 95.63 percent of the
   strong-edge gradient metric, had a mean-luminance ratio of 1.00030, and a
   55.24 dB PSNR relative to the bypass. Visual inspection found the expected
   mild diffraction softening without glow halos, colour fringes, or framing
   changes.

The old generic Fog Glow node remains muted as a rejected PSF approximation.
No arbitrary bloom, flare, veiling glare, chromatic diffraction, sensor noise,
white balance, or sharpening was added. The contract is valid only for the
named camera at f/8 and 3840 x 2160. A read-only audit now checks the active
camera, lens state, output, colour management, compositor nodes, profile mix,
neutral fallback, and diffraction qualification before an expensive render:

```text
research/projects/driveclub_f40/camera_pipeline.json
workflows/blender/scripts/audit_camera_pipeline.py
```

The current live audit passes all 50 checks, including final sampling,
denoising, compositor-device state, active map names, packed status, dimensions,
and all four float32 map hashes. An intentional unsaved f/5.6
mismatch then failed only `camera.aperture_f_number` with exit status 2, after
which f/8 was restored and the scene resaved. A passed audit proves state
identity, not optical accuracy; the impulse and same-source 4K gates remain the
visual and numerical evidence.

The active atmosphere prior is:

```text
bounded volume: 120 x 120 x 42 m
ground visibility prior: 1500 m
extinction coefficient: 0.002608 1/m
single-scatter albedo: 0.95
particle diameter prior: 12 um
top density factor: 0.12
phase function: Mie
```

At full ground density this implies approximately 97.43 percent direct
transmittance over 10 m and 87.77 percent over 50 m. These are derived values,
not validation against a measured weather record.

Sky Texture `Air`, `Aerosol`, and `Ozone` remain uncalibrated artist priors in
this scene. The sun angular diameter is set to 0.533 degrees, and the Sky Texture
is the only direct-sun owner.

The following render passes are enabled:

- Z;
- Mist, diagnostic only;
- Environment;
- Normal;
- Cycles denoising data.

## Audited real-lens candidate

Lensfun commit `698a39eea69be00f4f25b6da6c1ad34b1f162b50` contains a
full-frame Canon EF 50 mm f/1.8 STM entry in `data/db/slr-canon.xml`:

```text
distortion, PTLens at 50 mm:
  a = 0.0061844
  b = -0.0313122
  c = 0.0314815

TCA, poly3 at 50 mm:
  vr = 1.0000409
  vb = 0.9999893

vignetting, PA at 50 mm / f2.5 / 10 m:
  k1 = -0.0364
  k2 = -1.3199
  k3 = 0.7328

vignetting, PA at 50 mm / f3.5 / 10 m:
  k1 = -0.4165
  k2 = 0.4098
  k3 = -0.4114
```

This is a candidate because it matches the scene's format and focal length, not
because it has been chosen as the intended photographic lens. Its calibration
rows were captured on several Canon full-frame bodies. It is stored in the
Blender text datablock `VA_REAL_LENS_CANDIDATE` but remains disabled.

## Acceptance tests

1. Atmosphere-off and atmosphere-on renders use the same camera, exposure,
   colour management, sky, and material state.
2. The atmosphere-on image changes direct visibility and in-scattering, not only
   the background colour.
3. Mist Pass does not feed the beauty output.
4. A zeroed lens stage is visually neutral.
5. A measured lens profile is tested against straight-line, flat-field, and
   high-contrast-edge calibration images before acceptance.
6. PSF and glare are tested on scene-linear high-dynamic-range emitters and
   reflections, not on already tone-mapped pixels.
7. Denoising is compared on/off so weak volume and sparkle signals are not
   silently erased.
8. Final evidence retains atmosphere-off, no-post, diagnostic passes, and the
   active manifest.
9. Camera-specific stages must pass the machine-readable camera contract before
   a final render; mismatch is a failure, not an invitation to retune the image.

## Sources

- [Blender Volume Coefficients](https://docs.blender.org/manual/en/5.0/render/shader_nodes/shader/volume_coefficients.html)
- [Blender Volumes](https://docs.blender.org/manual/en/5.0/render/materials/components/volume.html)
- [Blender Render Passes](https://docs.blender.org/manual/en/5.0/render/layers/passes.html)
- [Blender Map UV Node](https://docs.blender.org/manual/en/5.0/compositing/types/transform/map_uv.html)
- [Blender Compositor System](https://docs.blender.org/manual/en/5.0/compositing/compositor_system.html)
- [Blender Denoise Node](https://docs.blender.org/manual/en/5.0/compositing/types/filter/denoise.html)
- [Lensfun manual](https://lensfun.github.io/manual/latest/)
- [Lensfun calibration format](https://lensfun.github.io/manual/v0.3.1/elem_calibration.html)
- [PBRT Realistic Cameras](https://www.pbr-book.org/3ed-2018/Camera_Models/Realistic_Cameras)
- [Canon EOS 5D Mark IV](https://www.usa.canon.com/shop/p/eos-5d-mark-iv)
- [Canon EF 35mm f/2 IS USM](https://www.cla.canon.com/en/p/ef-35mm-f-2-is-usm)
- [Canon EF 50mm f/1.8 STM](https://www.usa.canon.com/shop/p/ef-50mm-f-1-8-stm)
- [Canon EF 85mm f/1.4L IS USM](https://www.cla.canon.com/en/p/ef-85mm-f-1-4l-is-usm)
- [Canon â€” Reading and Understanding Lens MTF Charts](https://www.usa.canon.com/learning/training-articles/training-articles-list/reading-and-understanding-lens-mtf-charts)
- [Edmund Optics â€” The Airy Disk](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/limitations-on-resolution-and-contrast-the-airy-disk/)
- [Blender 5.2 Python API â€” Compositor Convolve Node](https://docs.blender.org/api/5.2/bpy.types.CompositorNodeConvolve.html)
- [Lensfun Canon SLR calibration data](https://github.com/lensfun/lensfun/blob/698a39eea69be00f4f25b6da6c1ad34b1f162b50/data/db/slr-canon.xml)
- [Lensfun source at the audited commit](https://github.com/lensfun/lensfun/tree/698a39eea69be00f4f25b6da6c1ad34b1f162b50)
