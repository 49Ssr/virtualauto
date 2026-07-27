# Weather and hydrometeors

## 1. Weather is a coupled state

Weather changes illumination, visibility, surface state, vehicle contamination,
aerodynamics, and camera response simultaneously. Adding particles labelled
`rain` to an otherwise dry clear-sky scene is not a weather system.

A weather profile should couple:

- cloud and sky radiance;
- precipitation type and intensity;
- wind and gusts;
- atmospheric extinction;
- ground accumulation and drainage;
- vehicle interaction;
- lens/windshield interaction;
- temporal history and transition.

## 2. Cloud classification and appearance

`AUTHORITATIVE`: the WMO International Cloud Atlas classifies clouds by genera,
species, varieties, supplementary features, and accessory clouds. This is a
more useful authoring vocabulary than `fluffy`, `stormy`, or `noise cloud`.

Cloud appearance depends on:

- altitude and vertical extent;
- liquid/ice phase;
- particle-size distribution;
- optical depth;
- internal structure and turbulence;
- solar/view angle;
- surrounding sky radiance;
- precipitation and virga;
- terrain and boundary-layer interaction.

A procedural density field alone does not guarantee meteorological or optical
coherence.

## 3. Cloud lighting

Clouds can:

- block or soften direct sunlight;
- create high-contrast silver lining;
- redistribute sky illumination;
- cast large moving shadows;
- brighten the horizon through multiple scattering;
- reduce or increase local contrast depending on view direction;
- become major reflection sources on automotive clearcoat and glass.

Production approximation levels:

1. distant background card only;
2. cloud-shadow texture plus sky modification;
3. volumetric cloud layer;
4. multi-layer volumetric weather field.

Each level must declare which effects it omits.

## 4. Overcast conditions

An overcast sky is not a grey background. It has:

- directional luminance gradients;
- cloud-base texture and depth;
- horizon brightening/darkening depending state;
- weak but nonzero shadow direction;
- local breaks and colour variation;
- ground/urban bounce;
- reflection structure at several angular scales.

A uniform world colour removes body-form cues and encourages artificial
reflection cards. A controlled overcast environment should still produce broad,
readable gradients over a car.

## 5. Fog

`AUTHORITATIVE`: fog is a near-surface cloud of suspended water droplets or ice
crystals that reduces visibility.

Relevant types include:

- radiation fog;
- advection fog;
- upslope fog;
- valley fog;
- steam/evaporation fog;
- precipitation fog;
- freezing fog.

The type informs vertical structure, terrain relation, motion, and surface
wetness. A uniform box volume is only one approximation.

## 6. Rain

Rain rendering spans distinct phenomena:

- falling drops visible by motion blur and highlights;
- atmospheric extinction from dense rain shafts;
- splash crowns and secondary droplets;
- road-film growth and runoff;
- puddle impacts and ripples;
- tyre spray and wake mist;
- body-panel impacts and rivulets;
- windshield droplets and wiper clearing;
- lens droplets and flare;
- sound and exposure changes outside rendering scope but relevant to cinematic
  coherence.

### 6.1 Drop-size distribution

`PRIMARY`: Marshall-Palmer is a canonical statistical rain-drop distribution,
but real distributions vary with rainfall type and intensity. VirtualAuto does
not use one fixed drop diameter for all rain.

### 6.2 Falling-drop representation

Small, fast drops are often perceived as streaks because of shutter integration.
Inputs:

- world-space velocity from gravity and wind;
- drop-size proxy;
- shutter time;
- lens focus and aperture;
- illumination and phase response;
- depth distribution;
- collision/occlusion.

A camera-facing streak texture that ignores world motion is an image-space
approximation and must be labelled.

### 6.3 Rain shafts

Distant rain can appear as volumetric curtains with spatially varying density.
It should affect terrain visibility and sky illumination, not only add streaks.

## 7. Wind

Wind is a vector field, not one particle direction.

Required distinctions:

- mean wind;
- gusts;
- turbulence;
- terrain/building shelter;
- vehicle-relative airflow;
- boundary-layer variation with height;
- wakes behind moving vehicles.

Wind should coherently influence:

- rain streaks;
- snow drift;
- dust and spray;
- vegetation;
- cloud advection;
- surface drying;
- loose debris.

## 8. Windshield water

The windshield is a moving, inclined, curved surface exposed to gravity,
vehicle acceleration, aerodynamic shear, surface tension, adhesion, coalescence,
and wipers.

A production approximation can track droplets in windshield-local coordinates
with forces projected into the surface tangent plane:

```text
surface acceleration proxy
    = gravity
    - vehicle acceleration
    + aerodynamic shear
```

Then apply:

- adhesion threshold;
- velocity damping;
- coalescence;
- breakup at high shear;
- thickness/optical response;
- wiper displacement and residual film;
- boundary drainage.

This is still a model. It should be validated in motion and not inferred from
one DriveClub visual impression.

## 9. Body-panel water

Different vehicle regions experience different water behaviour:

- upward-facing panels collect drops and shallow film;
- steep panels shed water;
- seams, badges, vents, and panel gaps create drainage paths;
- mirrors and spoilers create wakes and drip sources;
- lower body receives road spray and contaminated film;
- engine heat and airflow can accelerate drying;
- hydrophobic coatings change bead/contact behaviour.

A uniform droplet texture over the entire car is not acceptable for close work.

## 10. Wipers and cleared regions

Wiper systems should distinguish:

- blade geometry and swept area;
- contact pressure proxy;
- cleared film versus displaced edge ridge;
- residual streaks and chatter;
- missed corners;
- parked position;
- intermittent timing;
- washer fluid and contamination where relevant.

The swept mask should derive from linkage/blade motion, not a hand-painted arc
unless labelled as a shot-specific approximation.

## 11. Snow

Snow appearance depends on:

- grain size and metamorphism;
- density and compaction;
- liquid-water content;
- impurities;
- illumination directness;
- viewing angle;
- surface structure;
- age and melt/refreeze history.

`PRIMARY`: spectral snow-albedo models show that effective grain size and
illumination geometry matter strongly. A white diffuse material is insufficient.

### 11.1 Falling snow

Requires size/shape proxies, tumbling, low terminal velocity, wind, depth of
field, and local lighting.

### 11.2 Accumulation

Follows surface orientation, shelter, temperature, wind redistribution, and
contact disturbance. Warm vehicle surfaces and tyres can melt or compact snow.

### 11.3 Road snow states

```text
fresh powder
-> tracked/compacted
-> polished snow
-> slush
-> wet melt
-> refrozen ice
-> dirty residual banks
```

Each state has distinct geometry, water content, contamination, and reflection.

## 12. Ice and frost

### Clear/glaze ice

Can preserve dark substrate while adding smooth or rough dielectric reflection.
Thickness, bubbles, cracks, and trapped water matter.

### Frost

Fine ice crystals scatter strongly, brighten the surface, and build according
to temperature/humidity and exposure. Windshield frost is not a generic white
roughness mask.

### Black ice

A thin transparent ice layer on dark pavement can be visually subtle but highly
specular at grazing angles. It requires strict lighting and angle tests.

## 13. Hail

Hail introduces larger ballistic particles, impacts, splash, bounce, and
potential vehicle damage. It is outside initial production scope but should not
be represented by enlarging rain streaks alone.

## 14. Road-surface transitions during weather

Weather profiles must drive the road state machine:

```text
rain onset
    isolated dark spots
    cavity filling
    connected wet film
    runoff and ponding
    spray onset

rain cessation
    flow reduction
    high-point drying
    edge/cavity retention
    evaporation streaks
    contamination deposits
```

Transition timing can be art-directed, but spatial order must respect slope,
porosity, and traffic.

## 15. Headlights in precipitation

Rain, fog, snow, and spray affect:

- beam visibility;
- forward/back scatter;
- glare and halo;
- wet-road reflection;
- drop highlights;
- camera flare;
- contrast of signs and markings.

Scene-space scattering and camera-space flare are separate. Both may be needed,
but their contributions must be independently disable-able.

## 16. Lightning and storm illumination

Lightning is a short-duration spatial emitter with cloud and atmospheric
interaction. A production shot should consider:

- source location and branching scale;
- cloud illumination before/after visible channel;
- exposure and rolling/global shutter assumptions;
- wet-surface reflection;
- temporal sequence and thunder delay outside image rendering.

A full-screen white flash is a compositor approximation, not a lightning-light
model.

## 17. Weather state schema proposal

A future machine-readable environment profile should include:

```text
weather_type
cloud_class
cloud_coverage
precipitation_type
precipitation_rate_proxy
wind_mean
wind_gust
visibility_targets
surface_initial_state
recent_weather_history
accumulation_policy
evaporation_policy
vehicle_interaction_policy
camera_precipitation_policy
```

Physical units are preferred where the implementation supports them. Proxies
must be named as proxies.

## 18. Engine and performance strategy

Hero-quality weather can be decomposed by contribution:

- analytic or captured sky;
- low-frequency cloud illumination/shadows;
- volumetric cloud/fog where necessary;
- near-camera precipitation geometry/particles;
- distant precipitation volume;
- local collision splashes;
- shader/geometry water accumulation;
- compositor-only lens contamination.

This permits LOD without pretending one technique handles every scale.

## 19. Validation suite

For each weather profile:

- fixed camera still;
- vehicle and camera motion;
- world-only/direct-only/volume-only passes;
- dry baseline;
- surface-state progression;
- glass and paint reflection checks;
- headlight test when relevant;
- wind-direction diagnostic;
- particle velocity visualisation;
- accumulation mask visualisation;
- Cycles/EEVEE comparison where supported;
- fresh-file or deterministic-builder run.

## 20. Failure signatures

- rain passes through roof/ground without occlusion;
- streak direction ignores camera shutter and world velocity;
- all surfaces become equally wet at once;
- puddles form before cavities and low points;
- spray emits on dry road;
- windshield droplets ignore acceleration and wipers;
- fog affects camera view but not the intended reflection/transmission path;
- snow accumulates under tyres or on hot/vertical surfaces without a declared
  approximation;
- cloud shadows move independently of clouds/wind;
- compositor haze changes the background but leaves distant reflections crystal
  clear;
- wind influences particles but not vegetation or drying;
- weather has no prior-state history.

## 21. Initial weather profiles

VirtualAuto should first qualify five controlled profiles:

1. clear dry midday;
2. hazy dry late afternoon;
3. bright overcast damp road;
4. active rain with wet film and limited ponding;
5. post-rain low sun with drying road and residual spray.

Snow, heavy fog, dust storm, and night rain follow after the ownership and
validation framework is proven.