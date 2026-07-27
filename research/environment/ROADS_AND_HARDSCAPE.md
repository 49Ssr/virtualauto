# Roads and hardscape

## 1. Road appearance is an assembly

A road surface is not one material. It is a constructed, worn, contaminated,
weathered, and drained assembly whose visible response depends on scale,
aggregate, binder, finishing, traffic, moisture, and maintenance.

Common classes include:

- dense-graded asphalt concrete;
- stone-matrix asphalt;
- open-graded or porous asphalt;
- chip seal/surface dressing;
- rolled asphalt and mastic-rich surfaces;
- broom-finished, tined, polished, patched, or exposed-aggregate concrete;
- cobble, block, brick, and modular paving;
- compacted gravel and unsealed roads;
- kerbs, shoulders, drains, barriers, paint, thermoplastic markings, reflectors,
  metal covers, sealants, and repair compounds.

`VA-RULE`: a road asset declares construction class and state. `Asphalt` alone
is not enough.

## 2. Texture scale bands

`AUTHORITATIVE`: FHWA pavement guidance separates surface texture into bands:

- **microtexture:** approximately `1 micrometre` to `0.5 mm`;
- **macrotexture:** approximately `0.5 mm` to `50 mm`;
- **megatexture:** approximately `50 mm` to `500 mm`.

Longer-wavelength unevenness belongs to roughness/profile rather than surface
texture in this classification.

### 2.1 Microtexture

Aggregate-scale asperity and polish. It influences tyre friction and very small
highlight breakup. In Blender it is usually below explicit geometric
resolution and belongs in measured/derived normal, roughness, or statistical
microfacet treatment.

### 2.2 Macrotexture

Aggregate arrangement, voids, grooves, and local drainage texture. It is often
visible in close automotive shots and should not be represented only by shader
roughness.

### 2.3 Megatexture

Pothole edges, coarse distress, patch steps, rut transitions, and broad surface
irregularity. It affects wheel contact, shadow, silhouette, and camera motion.
It belongs in geometry/displacement where shot distance permits.

### 2.4 Profile and terrain form

Road crown, crossfall, banking, vertical curvature, settlement, and long-wave
waviness. These control drainage, puddles, vehicle stance, and horizon movement.

## 3. Asphalt components

A practical asphalt model separates:

- aggregate mineral response;
- binder/mastic response;
- air voids and cavities;
- exposed versus coated aggregate;
- compaction and segregation;
- oxidation and ageing;
- traffic polish;
- fines, dust, rubber, oil, salts, and biological contamination;
- cracks, seals, patches, and utility cuts.

Fresh asphalt can appear dark and binder-rich. Ageing, abrasion, oxidation,
aggregate exposure, dust, and repairs produce spatially varied response. There
is no universal asphalt base colour.

## 4. Concrete components

Concrete appearance depends on:

- cement paste colour and curing;
- aggregate type and exposure;
- finishing direction;
- joints and sealant;
- tining/grooving;
- laitance, polish, scaling, spalling, and repairs;
- tyre rubber and oil;
- water absorption and efflorescence;
- freeze-thaw and de-icing history.

Broom or tine direction is anisotropic evidence. Random isotropic noise is not a
sufficient substitute for directional finishing.

## 5. Road geometry and vehicle grounding

Road geometry must support:

- physically plausible tyre contact;
- suspension compression and ride height;
- wheel-shadow contact;
- kerb dimensions;
- drainage direction;
- puddle formation;
- debris migration;
- camera vibration and motion.

A perfectly flat plane produces a showroom-like stance even when textured
heavily. Conversely, arbitrary high-amplitude displacement can make tyres float
or penetrate.

`VA-RULE`: road height fields are filtered by wheel-contact scale. Geometry that
would move a real tyre/contact patch must be represented coherently in the
vehicle-ground relationship.

## 6. Layered road representation

Recommended ownership:

```text
base geometry
    -> crown, banking, long-wave profile

mid-scale displacement/geometry
    -> ruts, patches, potholes, joints, kerbs

fine displacement or normal
    -> aggregate macrotexture, grooves, cracks

roughness and micro-normal
    -> aggregate microtexture, binder polish, fines

surface-state layer
    -> dust, dampness, water film, oil, rubber, salt

instances/decals
    -> debris, leaves, markings, repairs, drains
```

Each band uses world-space units and an LOD transition policy.

## 7. Wet pavement is not a roughness slider

Wet appearance can involve:

1. water entering pores and reducing air-solid refractive contrast;
2. darkening/saturation of the substrate;
3. a surface water film adding dielectric reflection;
4. microcavities filling and effective roughness changing;
5. standing water becoming locally smooth and reflective;
6. water thickness varying by slope, texture, traffic, and drainage;
7. spray, ripples, wakes, tyre tracks, and evaporation;
8. polarization and angle-dependent glare.

A production wet-road model should separate substrate state from surface water.

## 8. Moisture state machine

Suggested state vocabulary:

```text
dry
-> dusty dry
-> spotted
-> damp
-> wet film
-> flowing
-> ponded
-> drying edge
-> residual contaminated film
```

Transitions depend on:

- rain rate and drop momentum;
- surface porosity and initial moisture;
- slope/camber;
- drainage and blockage;
- wind;
- temperature and evaporation;
- tyre disturbance;
- texture depth.

One scalar may drive a shot-specific approximation, but the downstream masks
must preserve the qualitative distinctions above.

## 9. Drainage and puddles

Puddles form from topography and flow, not from arbitrary noise masks.

Minimum production logic:

- obtain or construct a low-frequency height field;
- identify local basins and flow paths;
- respect road crown, kerbs, drains, shoulders, and wheel ruts;
- modulate by permeability and recent rainfall;
- add edge meniscus/transition only at visible scale;
- allow tyre tracks to remove, redistribute, or disturb water;
- preserve a dry or damp high point where drainage demands it.

`VA-RULE`: screen-space puddle masks are art-direction layers unless generated
from scene-space topography and state.

## 10. Water-film shading

A thin water film can be represented as:

- an explicit surface/shell;
- a layered material approximation;
- a BSDF blend driven by film coverage;
- geometry for standing water and shader treatment for dampness.

Checks:

- correct dielectric Fresnel response;
- no metallic water;
- substrate remains visible through thin clean film;
- roughness derives from water-surface disturbance, not substrate alone;
- film reflection aligns to actual surface normal and gravity;
- depth and contamination influence absorption/tint only when justified;
- no duplicated clearcoat-like lobe with uncontrolled energy.

## 11. Road spray and tyre interaction

Spray has several components:

- tread pickup and ejection;
- side spray/fan;
- sheet breakup from standing water;
- fine mist in the wake;
- displaced water wake;
- wheel-well and underbody interaction.

Inputs should include:

- tyre angular and linear velocity;
- local water depth;
- tread/contact state proxy;
- vehicle speed and wake;
- wheel steering angle;
- wind;
- gravity and droplet-size proxy.

The system must remain stable in motion and should not emit from dry regions.

## 12. Dirt, dust, rubber, and oils on pavement

### Dust and fines

Accumulate in low-energy areas, shoulders, joints, edges, and surface cavities.
Traffic can clean wheel paths while resuspending material.

### Rubber

Braking/acceleration zones, racing lines, junctions, and tyre-contact areas can
darken and smooth the surface. Distribution follows vehicle trajectories, not
uniform grunge.

### Oil and fuel

Localized around parking positions, service areas, traffic queues, and vehicle
failure zones. Wetness can spread or iridesce films, but thin-film colour should
not be added without scale and illumination tests.

### Salt and de-icing residue

Can create pale deposits, splash patterns, corrosion cues, and changed moisture
behaviour.

## 13. Markings and road furniture

Road markings may be paint, thermoplastic, tape, raised markers, or embedded
reflectors. Their properties include:

- thickness and edge profile;
- bead retroreflection;
- wear and tyre polish;
- cracking and delamination;
- wet-night performance;
- dirt accumulation;
- repair overlap and jurisdiction-specific geometry.

Do not use one perfectly flat white decal for every road marking.

Kerbs, barriers, drains, manholes, cats-eyes, studs, signs, and gantries provide
high-value scale and reflection structure for vehicles. Their dimensions and
placement should follow a declared road context.

## 14. Procedural authoring rules

Procedural roads should be parameterized by construction and process:

- aggregate size distribution;
- binder coverage;
- compaction direction;
- paving lane and seam layout;
- crack/joint cause;
- traffic paths;
- drainage topology;
- repair chronology;
- contamination sources;
- surface-state history.

A stack of unrelated noise nodes is not process evidence.

## 15. Scanning and photogrammetry

Scans can capture valuable macrotexture and distress but require:

- metric scale;
- de-lighting or known illumination;
- separation of albedo, normals, displacement, and baked shadows;
- tiling strategy without repeated unique defects;
- removal or retention of loose debris by intent;
- licence/provenance;
- LOD and contact validation.

Photogrammetric colour is not automatically diffuse albedo.

## 16. Automotive qualification views

For a road material/environment capture:

- low grazing camera along the surface;
- orthographic top view with metric ruler;
- tyre contact close-up;
- long focal-length view for repeating patterns;
- wet/dry paired exposure;
- headlight night view;
- chrome and black-gloss reflection test near ground;
- moving camera at vehicle speed;
- rain/spray interaction where applicable.

## 17. Failure signatures

Reject or revise when:

- aggregate appears the size of footballs;
- only normal maps move while silhouette/contact remain flat;
- road roughness is spatially uniform;
- wetness ignores gravity and drainage;
- puddles occur on crowns and slopes without barriers;
- markings have no thickness or wear;
- tyre tracks do not align with actual trajectories;
- cracks cross patches and joints without chronology;
- every metre carries equal detail density;
- world-space scale changes when an object is scaled;
- lower-body car reflections show a different ground from the visible road.

## 18. Initial road material matrix

| State | Substrate diffuse | Film reflection | Macrotexture | Local geometry |
| --- | --- | --- | --- | --- |
| dry fresh asphalt | dark binder-rich | low/moderate | construction-dependent | seams/aggregate |
| dry aged asphalt | aggregate/fines visible | variable polish | worn/cracked | patches/ruts |
| damp | darker substrate | discontinuous | still visible | little standing water |
| wet film | darker substrate | continuous but disturbed | partially optically filled | flow paths |
| ponded | viewed through water | strong smooth/disturbed | submerged | basin boundary/ripples |
| dusty | pale/low-contrast deposit | suppressed until disturbed | cavities filled | loose deposits |
| rubbered | dark traffic-path deposit | often smoother | localized | trajectory-driven |

This matrix is qualitative. It does not supply unverified production constants.