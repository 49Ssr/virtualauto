# Open questions and contradictions

This log prevents plausible interpretations from hardening into undocumented
facts. Entries remain open until a source, Blender source-code review, or
VirtualAuto experiment resolves them.

## ENV-CONTRA-001 — Nishita brightness and exposure

### Evidence

`BLENDER-DOC`: the Blender 5.0 Sky Texture manual notes that Nishita can appear
bright/overexposed with default settings and suggests reducing exposure.

### Tension

Exposure is a capture/display parameter. Lowering exposure can make an image
viewable but does not establish that sky radiance, sun radiance, ground bounce,
or camera calibration are physically matched.

### Current rule

Exposure adjustment is permitted and recorded. It must not be described as
atmospheric calibration or used to hide accidental energy double counting.

### Resolution test

Build a fixed diagnostic scene and compare Sky Texture families at recorded
scene-linear values, exposure brackets, and direct-sun ownership.

---

## ENV-CONTRA-002 — Meaning of Air, Dust, and Ozone controls

### Evidence

`BLENDER-DOC`: Nishita exposes Air, Dust, and Ozone with qualitative examples.

### Unknown

The user-facing documentation does not establish direct mappings to pressure,
molecular number density, aerosol optical depth, particle size/composition,
PM2.5, humidity, total-column ozone, or a vertical profile.

### Current rule

Store values under Blender/Nishita names. Do not publish converted physical
units until source code and controlled reference calculations support them.

---

## ENV-CONTRA-003 — Sun disc plus Sun light

### Evidence

Sky models and HDRIs can contain solar radiance. Blender Sun lights can provide
controllable direct illumination and shadows.

### Risk

Using both can double count direct solar energy, alter sky-to-sun ratio, and
mislead material tuning.

### Current rule

Every environment declares direct-sun ownership: `sky`, `HDRI`, `Sun light`, or
`deliberately split`. Combined use requires contribution passes.

---

## ENV-CONTRA-004 — World volume convenience versus atmospheric structure

### Evidence

`BLENDER-DOC`: a volume can fill the World, but official documentation explains
that an infinitely filled medium is not a good assumption for fog/atmospheric
scattering between Earth and an infinitely distant background; a bounded volume
is recommended for such effects.

### Current rule

World volume is allowed for constrained dark/stylized cases but is not the
default exterior atmosphere or a planetary model.

---

## ENV-CONTRA-005 — EEVEE visual match versus transport equivalence

### Evidence

`BLENDER-DOC`: EEVEE has volume, reflection, refraction, probe, and multiple-
scattering limitations that differ from Cycles.

### Risk

A camera-view match can conceal missing volumetric participation in paint,
glass, or probes.

### Current rule

EEVEE qualification includes explicit reflection/transmission tests. Matching a
beauty frame does not establish path-equivalent transport.

---

## ENV-CONTRA-006 — Analytic ground albedo versus actual ground

### Evidence

Hosek/Wilkie and Blender expose ground albedo as a sky-model input.

### Unknown

How Blender's fitted model response should be coordinated with heterogeneous
road, terrain, architecture, and renderer global illumination in a finite
scene.

### Current rule

Ground Albedo remains a sky-model parameter. It does not replace local geometry
or authorize double bounce. Compare sky-only and full-scene effects.

---

## ENV-CONTRA-007 — HDRI described as measured radiance

### Evidence

Image-based lighting research uses calibrated HDR scene radiance. Public HDRIs
vary widely in capture and processing quality.

### Risk

An EXR filename or high bit depth can be mistaken for radiometric fidelity.

### Current rule

Use `captured environment map` unless response recovery, clipping, processing,
and metadata justify stronger language. Acceptance is role-specific.

---

## ENV-CONTRA-008 — HDRI sun extraction

### Question

Can a clipped or blurred solar region be removed and replaced by a Sun light
without distorting the surrounding sky and total energy?

### Current rule

This is a production approximation. Preserve original map, processing script,
mask, residual analysis, and direct/world contribution renders.

---

## ENV-CONTRA-009 — Wet pavement roughness

### Common claim

Wet roads are smoother, so lower roughness.

### Contradiction

Water can fill microcavities and add a smoother interface, but rain also creates
ripples, drop impacts, flow, spray, uneven films, and rough standing water.
Substrate darkening and dielectric Fresnel change independently.

### Current rule

No single roughness scalar owns wetness. Separate substrate moisture, film
coverage, water-surface roughness, and standing-water geometry.

---

## ENV-CONTRA-010 — Darkening of wet porous materials

### Evidence

Optical literature attributes wet darkening to changes in pore-interface
contrast, internal reflection/transmission, and absorption path, not simply a
multiplied albedo.

### Unknown

What minimum RGB layered approximation is robust across asphalt, concrete,
soil, dust, and aggregate in Blender 5.0.1.

### Resolution test

Paired dry/wet reference capture under controlled geometry and polarized/non-
polarized lighting where available; compare substrate-only and film layers.

---

## ENV-CONTRA-011 — Mist Pass as atmosphere

### Evidence

`BLENDER-DOC`: Mist Pass is a depth-based mask for compositing.

### Risk

A depth fade can visually resemble haze while failing angle, reflection,
refraction, shadow, and local-light interactions.

### Current rule

Use Mist Pass for diagnostics or labelled art direction only. It cannot support
a physical atmosphere claim.

---

## ENV-CONTRA-012 — One aerosol anisotropy parameter

### Evidence

Graphics commonly uses a one-parameter phase-function approximation.

### Unknown

A real aerosol distribution can combine multiple particle populations and
spectral/angular behaviour not captured by one `g`.

### Current rule

Anisotropy is a fitted or artistic proxy unless linked to a defined optical
model. It is not particle size.

---

## ENV-CONTRA-013 — Ozone as a sky-blue control

### Evidence

Blender documentation describes Ozone as useful for making the sky appear
bluer.

### Risk

Treating ozone as a purely blue colour control erases its absorption role and
vertical/spectral context.

### Current rule

Retain implementation terminology, avoid universal visual directions, and test
across sun elevation and exposure.

---

## ENV-CONTRA-014 — Cloud density noise versus cloud classification

### Evidence

WMO classification is morphological/observational; renderer clouds are density
and optical fields.

### Unknown

How to map official cloud class descriptors to procedural generator constraints
without falsely claiming meteorological simulation.

### Current rule

Use WMO names as reference targets only when visible morphology supports them.
`Inspired by` is preferred over a formal classification for unvalidated
procedural clouds.

---

## ENV-CONTRA-015 — Rain drop distribution

### Evidence

Marshall-Palmer is a canonical exponential drop-size distribution.

### Unknown

Its validity varies by precipitation regime. Renderer-visible streaks also
depend on shutter, lighting, and depth.

### Current rule

Do not turn one distribution into a universal particle preset. Record the rain
regime or call the size field a production proxy.

---

## ENV-CONTRA-016 — Snow as high-albedo diffuse material

### Evidence

Snow spectral albedo and BRDF depend on effective grain size, impurities,
illumination, angle, and state.

### Current rule

A white diffuse shader can be a distant LOD only. Hero snow requires structure,
state, exposure/clipping checks, and contamination.

---

## ENV-CONTRA-017 — DEM resolution versus terrain detail

### Evidence

Elevation products report grid spacing and accuracy, but sensor, vegetation,
buildings, interpolation, and processing affect actual terrain fidelity.

### Current rule

Do not call grid spacing `detail resolution` without product evidence. Added
procedural detail is synthetic and remains separately owned.

---

## ENV-CONTRA-018 — Dust on surfaces versus suspended dust

### Risk

The same procedural mask is sometimes used as albedo deposit and volume density.
This creates mass without an emission/transport event.

### Current rule

Deposited reservoir, emission, airborne transport, and redeposition are separate
states. A shot-specific shortcut must state which transitions are omitted.

---

## ENV-CONTRA-019 — World-space road scale under object scaling

### Question

Which coordinate/transform convention best preserves metric aggregate and crack
scale while allowing reusable road assets and procedural deformation?

### Current rule

Apply/record transforms or use explicit scene-unit coordinates. Qualification
includes scaled-object variants and checks for texture swimming.

---

## ENV-CONTRA-020 — Environment versus material compensation

### Risk

A weak environment causes material edits that later fail elsewhere: lower paint
roughness, brighter flakes, darker glass, exaggerated coat, or fake AO.

### Current rule

Before editing a vehicle material, inspect environment bandwidth, direct/world
ratio, horizon, exposure, reflection structure, and local geometry. Record which
side owns the correction.

---

## Priority unresolved questions

1. What exact equations and scaling does Blender 5.0.1 use for Nishita Air,
   Dust, Ozone, Sun Intensity, and Altitude?
2. What is the smallest calibrated environment rig that remains useful in both
   Cycles and EEVEE?
3. How should an environment profile express radiometric values versus artist
   defaults without false precision?
4. Can a deterministic road-water state model remain practical for cinematic
   shots without fluid simulation?
5. Which atmosphere contributions must be visible in automotive reflections for
   perceptual coherence?
6. What HDRI diagnostics can be automated without claiming full radiometric
   calibration?
7. How should local road dust couple to vehicle wake, deposition, and weather?
8. What subset of weather history is necessary to produce credible surface
   state?
9. Which environment variables most strongly expose the F40 windshield's
   triangular shading fault without confounding it with material transmission?
10. Which DriveClub environment systems can be recovered as source evidence,
    and which should only inspire independent Blender implementations?