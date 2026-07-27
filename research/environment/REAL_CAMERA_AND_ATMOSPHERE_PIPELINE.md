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
VA_ENV_BoundedMist -> Material Output Volume
Noisy Image + Denoising Albedo/Normal -> Denoise
-> neutral Lens Distortion
-> disabled unmeasured PSF approximation
-> final output
```

The current camera is recorded as an ideal, uncalibrated full-frame 50 mm
camera:

```text
sensor: 36 x 24 mm
focal length: 50 mm
distortion: neutral
TCA: neutral
vignetting: unset
PSF: unset
```

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

## Sources

- [Blender Volume Coefficients](https://docs.blender.org/manual/en/5.0/render/shader_nodes/shader/volume_coefficients.html)
- [Blender Volumes](https://docs.blender.org/manual/en/5.0/render/materials/components/volume.html)
- [Blender Render Passes](https://docs.blender.org/manual/en/5.0/render/layers/passes.html)
- [Blender Denoise Node](https://docs.blender.org/manual/en/5.0/compositing/types/filter/denoise.html)
- [Lensfun manual](https://lensfun.github.io/manual/latest/)
- [Lensfun calibration format](https://lensfun.github.io/manual/v0.3.1/elem_calibration.html)
- [PBRT Realistic Cameras](https://www.pbr-book.org/3ed-2018/Camera_Models/Realistic_Cameras)

