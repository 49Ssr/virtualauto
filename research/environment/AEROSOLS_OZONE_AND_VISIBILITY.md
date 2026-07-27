# Aerosols, ozone, and visibility

## 1. Terms that must not be collapsed

### Aerosol

A suspension of solid or liquid particles in air. Relevant classes include
mineral dust, sea salt, sulfate, organic aerosol, soot/black carbon, smoke,
industrial particles, and mixed/hygroscopic particles.

### Haze

A visibility state commonly associated with dry particles and broad aerosol
loading. In CG it is often used loosely; VirtualAuto records the assumed cause.

### Fog

A near-surface cloud of suspended liquid droplets or ice crystals. Fog is not
just stronger haze: its particle population, humidity state, vertical
structure, and spatial variation differ.

### Smoke

Combustion aerosol and gases. Optical behaviour depends on fuel, combustion
state, age, humidity, and soot content.

### Suspended road dust

Mineral/organic material lifted from unpaved roads or resuspended from paved
surfaces by tyres, turbulence, wind, and vehicle wakes.

### Deposited dust

Particles resting on surfaces. It changes albedo, roughness, microgeometry,
water behaviour, and later becomes a source for resuspension. It is not a
participating medium until airborne.

## 2. Optical depth and visibility

`AUTHORITATIVE`: aerosol optical depth is a dimensionless measure of extinction
through a vertical atmospheric column. Extinction includes scattering and
absorption. It is not identical to horizontal meteorological visibility.

For a homogeneous medium, direct transmittance is often represented by the
Beer-Lambert relation:

```text
T(d) = exp(-sigma_t * d)
```

where `sigma_t` is extinction coefficient and `d` is path length.

Real atmospheres are vertically and horizontally heterogeneous. A single
Blender density value can only approximate a specified volume and scale.

`VA-RULE`: every local atmosphere volume records its dimensions. Density values
without a spatial extent are not comparable.

## 3. Scattering versus absorption

Two atmospheres with similar visibility can produce different automotive
appearance:

- strongly scattering aerosol can brighten the veil and reduce contrast;
- absorbing aerosol can darken the sky or warm the horizon;
- forward scattering can create bright aureoles and glare near the sun;
- coarse mineral dust can produce different angular and spectral response from
  fine smoke or sulfate.

Therefore a `dust colour` and `density` pair is not a general aerosol model.

## 4. Particle size and angular response

Particle size relative to wavelength strongly affects scattering.

- molecular-scale scattering is broadly described by Rayleigh theory;
- particles comparable to visible wavelength produce Mie-like angular
  behaviour, often strongly forward-peaked;
- much larger particles become increasingly geometric-optics-like and can fall
  rapidly under gravity.

A renderer phase-function parameter is an angular approximation. It does not
encode the full particle-size distribution.

## 5. Phase functions and anisotropy

The Henyey-Greenstein phase function is common in graphics because one parameter
`g` controls a smooth progression from backward through isotropic to forward
scattering.

Interpretation:

- `g = 0`: isotropic approximation;
- positive `g`: forward-biased scattering;
- negative `g`: backward-biased scattering.

`VA-RULE`: `g` is recorded as an artist, fitted, or measured proxy. It is never
silently labelled as particle size.

Blender's render engines may combine or approximate anisotropy differently.
Engine-specific behaviour must be tested rather than inferred from the node
label alone.

## 6. Ozone

Most atmospheric ozone resides in the stratosphere, with a broad vertical
profile rather than a uniform scene-level concentration. Ozone absorption is
spectral and contributes to sky colour, especially across long paths.

Blender Nishita's `Ozone` control is useful for appearance studies, but it does
not expose a total-column unit, vertical profile, temperature dependence, or
spectral cross-section to the user.

`VA-RULE`: treat the value as a Nishita implementation parameter until Blender
source and a controlled comparison establish a physical mapping.

## 7. Pollution and urban atmosphere

Urban pollution can combine:

- primary soot and dust;
- secondary sulfate/nitrate/organic aerosol;
- humidity growth;
- regional background haze;
- local exhaust plumes;
- construction dust;
- photochemical gases;
- cloud/fog interaction.

A convincing urban automotive scene often needs at least three spatial layers:

1. regional background extinction;
2. boundary-layer or street-canyon haze;
3. local transient plumes from traffic, tyres, brakes, or construction.

A uniform world tint cannot represent all three.

## 8. Humidity and aerosol growth

Many aerosol particles take up water as relative humidity rises. This can
increase particle size, scattering, and haze even without adding new dry mass.
Fog onset is not simply a continuous extension of one dry-aerosol parameter,
but humidity history explains why visibility and sky brightness can change
rapidly.

VirtualAuto does not yet implement a hygroscopic growth model. Any humidity
control is therefore an explicit production proxy.

## 9. Vertical structure

Outdoor atmosphere commonly includes:

- relatively clean free troposphere above;
- a mixed boundary layer near the ground;
- elevated dust or smoke layers;
- valley inversions;
- fog banks and drainage flows;
- local road-level plumes.

For automotive cameras near the ground, a shallow dense layer can influence
visibility and headlight backscatter more than the same integrated mass spread
uniformly through a tall volume.

`VA-RULE`: do not default to one infinite homogeneous fog cube for every
exterior scene.

## 10. Headlights and backscatter

At night, fog, snow, rain, and dust can scatter vehicle lighting back toward the
camera. Important variables include:

- beam shape and source size;
- particle phase function;
- camera proximity to the emitter;
- medium density and depth;
- exposure and flare;
- wet road reflection.

A bright volumetric cone is not automatically correct. It can double count
sensor bloom or omit occlusion and multiple scattering.

## 11. Dust plumes behind vehicles

Road-dust emission involves source material, tyre contact, vehicle wake, wind,
and gravitational settling.

A production plume should distinguish:

- **emission zone** near contact patches and underbody wake;
- **coherent wake** with vehicle-relative advection;
- **turbulent dispersion** and breakup;
- **size-dependent settling**;
- **ground interaction and redeposition**;
- **background aerosol** already present.

`VA-RULE`: particles must use world/vehicle velocity coherently. A plume that
sticks to the car or ignores crosswind fails motion qualification.

## 12. Pollution colour pitfalls

Do not author atmosphere by choosing a brown, grey, or blue volume colour first.
Colour emerges from:

- light spectrum;
- scattering and absorption spectra;
- phase angle;
- path length;
- ground and cloud illumination;
- exposure and white balance.

An RGB absorption/scattering pair can be a useful approximation, but its source
and intended lighting range must be recorded.

## 13. Visibility targets

For a controlled environment, define observable targets such as:

- contrast of a black/white target at 50 m, 200 m, and 1 km;
- disappearance of terrain silhouettes by distance;
- sun aureole width;
- horizon luminance relative to zenith;
- direct-light attenuation through a known volume;
- headlight backscatter at a recorded exposure.

These targets are more useful than a free-floating `fog density` number.

## 14. Blender implementation boundary

### World Sky Texture

Useful for broad clear-sky molecular/aerosol/ozone appearance. Not sufficient
for local spatial haze, road dust, fog banks, or vehicle plumes.

### Principled Volume / Volume Scatter / Volume Absorption

Useful for bounded participating media. Their RGB coefficients and anisotropy
are renderer inputs, not an automatic atmospheric measurement system.

### EEVEE

Official documentation records important limitations: volume rendering is
camera-focused, multiple scattering is absent, and volume behaviour in
reflections/refractions/probes is restricted. Automotive qualification must
check glass and paint separately.

### Cycles

Supports more complete path-traced participation, but default bounce settings,
sampling, clamping, and denoising can still erase or bias weak volumetric
signals.

### Mist Pass

A depth-derived compositor mask. It can assist art direction or diagnostics but
must not be promoted as physical extinction.

## 15. Initial experiments

1. Match three target transmittances through a bounded neutral volume and verify
   the exponential distance relationship.
2. Hold extinction constant while varying scattering/absorption ratio; compare
   black-gloss, chrome, and diffuse-grey response.
3. Hold extinction constant while varying anisotropy; inspect sun aureole and
   headlight backscatter.
4. Compare a shallow ground layer with a tall homogeneous volume at equal
   vertical optical depth.
5. Render the same medium in Cycles and EEVEE, including paint reflections,
   windshield transmission, and headlight beams.
6. Separate deposited dust material response from suspended dust visibility.

No default production aerosol values are accepted until these experiments are
run and retained.