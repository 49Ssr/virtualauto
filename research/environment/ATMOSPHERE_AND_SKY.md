# Atmosphere and sky

## 1. Scope

This document separates three related but non-equivalent systems:

1. **sky radiance** arriving from effectively infinite distance;
2. **direct solar radiance** arriving from the sun's angular extent;
3. **participating-media transport** between scene points and the camera.

A world sky can illuminate the car without producing correct aerial perspective
through the local scene. A bounded volume can produce local extinction without
providing a complete daylight sky. A Sun light can cast shadows without being a
radiometrically matched solar disc.

## 2. Physical basis

### 2.1 Molecular scattering

`PRIMARY`: Rayleigh scattering describes scattering by particles much smaller
than the wavelength. In the visible range its strong wavelength dependence is
commonly approximated as proportional to `1 / lambda^4`, which contributes to a
blue clear sky and stronger reddening along long atmospheric paths.

This approximation is useful conceptually but not a licence to hard-code one
blue colour. Accurate optical depth depends on refractive index, molecular
number density, depolarization, wavelength, altitude, and path length.

### 2.2 Aerosol scattering

Particles comparable to visible wavelengths produce strongly size- and
composition-dependent scattering and absorption. In rendering literature this
is often represented by a Mie-like term and an anisotropic phase function.
Real atmospheric aerosols include sea salt, mineral dust, smoke, sulfate,
organic material, soot, and mixed particles; one scalar cannot recover their
full spectral and angular behaviour.

### 2.3 Absorption

Ozone and other gases absorb selected wavelengths. Ozone affects ultraviolet
strongly and also contributes broad visible absorption. Water vapour, oxygen,
and other gases matter in spectral regions not represented by a simple RGB sky
control.

### 2.4 Multiple scattering

Light can scatter more than once before reaching the camera. This becomes
important near the horizon, under high aerosol load, at twilight, inside clouds,
and for bright participating media. A renderer or sky model that omits or
approximates multiple scattering can remain useful, but the limitation must be
recorded.

## 3. Analytic daylight model families in Blender

Blender `5.0` exposes three Sky Texture families.

### 3.1 Preetham

`PRIMARY`: the 1999 Preetham, Shirley, and Smits model provides a practical
analytic daylight approximation parameterized for interactive graphics.

Strengths:

- computationally compact;
- historically widespread;
- useful for broad daylight art direction.

Limitations:

- known inaccuracies near the sun, horizon, high turbidity, and twilight;
- not a spectral atmospheric transport solver;
- should not be selected merely because a legacy scene was tuned around it.

### 3.2 Hosek/Wilkie

`PRIMARY`: the 2012 Hosek and Wilkie model improves the Preetham family,
including high-turbidity and low-sun conditions, and introduces ground-albedo
influence in the fitted sky model.

Strengths:

- better fit across a broader clear-sky domain;
- useful when a compact analytic model is preferred.

Limitations:

- remains a fitted sky-radiance model rather than a full scene atmosphere;
- ground albedo is a model input, not a substitute for actual heterogeneous
  terrain and local bounce.

### 3.3 Nishita

`BLENDER-DOC`: Blender's Nishita option is based on an improved atmospheric
scattering model and exposes controls for sun position, altitude, molecular
content, dust, and ozone.

The exact Blender implementation and parameter scaling are authoritative only
through Blender source and versioned documentation. User-facing labels must not
be reverse-labelled as meteorological measurements without a calibration
study.

## 4. Blender 5.0 Sky Texture parameter interpretation

### Sun Direction / Elevation / Rotation

Owns solar direction in the generated sky. If a separate Sun light is used, it
must be aligned to the same direction and its energy ownership documented.

### Turbidity

Available for Preetham and Hosek/Wilkie. It controls atmospheric haziness in the
model family. It is not directly equal to aerosol optical depth, PM2.5, humidity,
or visibility distance.

### Ground Albedo

Influences the analytic sky fit. It is a broad lower-hemisphere reflectance
parameter, not a replacement for road, terrain, buildings, or local bounce.

### Sun Disc

`BLENDER-DOC`: in Nishita, the sun disc can be included. Blender documentation
notes engine-specific support; it must be tested in the chosen render engine.
A visible disc and a separate Sun light can double-represent solar energy unless
calibrated deliberately.

### Sun Size

Controls disc angular size/softness in the sky implementation. It must be kept
consistent with shadow-source angular size when the separate direct light is
expected to represent the same sun.

### Sun Intensity

An implementation multiplier, not a measured radiance unit by itself.

### Altitude

Changes the observer position within the model atmosphere. It should not be
used as a generic brightness control.

### Air

Controls molecular density/scattering in the model. It is not a direct pressure
or molecular number-density measurement unless validated against source code
and a defined atmosphere.

### Dust

Controls aerosol-like scattering in the model. It does not specify particle
size distribution, composition, absorption, vertical profile, or relative
humidity growth.

### Ozone

Controls ozone absorption in the model. It is not a direct total-column ozone
measurement or vertical ozone profile.

## 5. Sky radiance versus local atmosphere

Official Blender documentation warns that applying volume shading to the World
is not a physically correct planetary-atmosphere model. For local fog and
atmospheric scattering, a bounded volume is generally a better-controlled
scene representation.

Recommended ownership:

```text
World Surface
    -> far-field sky/background radiance

Sun Light or calibrated sky disc
    -> direct solar shadows and highlights

Bounded Volume
    -> local extinction, in-scattering, fog, haze, smoke

Terrain and local geometry
    -> horizon, occlusion, reflected structure, parallax
```

This is an implementation decomposition, not a claim that these independent
pieces automatically conserve energy.

## 6. Direct-sun ownership patterns

### Pattern A: analytic sky plus separate Sun

Use when direct-light sampling, controllable shadows, and predictable highlights
are required.

Requirements:

- align directions exactly;
- document whether the analytic sun disc remains visible;
- control double counting;
- match angular size and shadow softness intentionally;
- retain a chrome-sphere and diffuse-grey diagnostic.

### Pattern B: HDRI owns the sun

Use only when the HDRI sun is unclipped and has sufficient angular/spatial
resolution and dynamic range for the intended result.

Risks:

- shadow softness and sampling noise;
- clipped sun radiance;
- sun enlarged by stitching or bloom;
- insufficient resolution for hard automotive glints.

### Pattern C: HDRI sky plus extracted/rebuilt Sun

A production approximation in which the environment map provides broad sky and
reflection structure while a separate Sun supplies direct illumination.

Requirements:

- identify and, where possible, neutralize the HDRI's original direct-sun energy;
- document the residual sun in the map;
- do not describe the result as a measured environment without qualification.

## 7. Horizon construction

The horizon is one of the highest-leverage automotive cues.

A believable horizon requires:

- correct camera height;
- terrain or built-environment silhouette;
- atmospheric extinction with distance;
- vertical sky luminance gradient;
- local occlusion and reflection structure;
- consistent visible-background and reflection geometry.

A flat plane meeting an infinite world can be acceptable for a diagnostic rig,
but it should not be mistaken for a natural exterior environment.

## 8. Twilight and night

Low-sun and post-sunset rendering requires more than rotating a midday sky:

- optical path length increases;
- multiple scattering and aerosol absorption become more visible;
- direct solar illumination can disappear while upper atmosphere remains lit;
- artificial lights introduce different spectra and finite-distance emitters;
- exposure changes alter apparent sky colour and lamp balance;
- city glow is volumetric and spatially distributed, not simply a brighter
  horizon colour.

Stars, moonlight, and airglow are outside the initial physical scope unless a
source and validation target are introduced.

## 9. Cloud interaction boundary

Sky Texture does not generate a meteorologically structured cloud field.
Clouds alter:

- direct-sun visibility;
- diffuse-sky distribution;
- local shadowing;
- aerial perspective;
- ground wetness history;
- reflection structure over the vehicle.

A clear-sky model beneath generic procedural clouds is only coherent if cloud
optical depth, shadowing, and sky illumination are treated together.

## 10. Automotive diagnostics

A sky/atmosphere setup should be rejected for material validation if:

- the car only reads from one camera angle;
- broad body panels see no stable reflection gradients;
- windows reflect a background inconsistent with what is visible;
- sun direction differs between shadows, sky disc, and highlights;
- exposure is changed to hide clipped or missing solar radiance;
- haze is painted into the compositor while reflections remain perfectly clear;
- the horizon height changes incorrectly with camera movement;
- Cycles and EEVEE divergences are unrecorded.

## 11. Initial VirtualAuto rules

1. Record the Sky Texture family and every exposed value.
2. Record direct-sun ownership separately.
3. Do not map Blender controls to physical atmospheric units without a test.
4. Use bounded local volumes for controllable fog/haze studies.
5. Keep a no-volume reference render.
6. Keep a world-only, direct-only, and combined-light diagnostic.
7. Check clearcoat, metal, glass, black trim, tyre rubber, and road response.
8. Validate sky/reflection behaviour in motion, not only one still.
9. Treat exposure as capture, not atmospheric density.
10. Preserve implementation differences by Blender version and render engine.