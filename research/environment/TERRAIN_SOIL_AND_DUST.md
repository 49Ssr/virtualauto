# Terrain, soil, and dust

## 1. Terrain is process history

Terrain form is produced by geology, tectonics, weathering, water, ice, wind,
vegetation, gravity, land use, and construction across multiple time scales.
A convincing terrain system should therefore connect shape, material,
hydrology, erosion, deposition, and vegetation rather than treating each as an
independent noise layer.

`VA-RULE`: a terrain asset states whether it represents measured topography,
procedural geomorphology, art-directed form, or a hybrid.

## 2. Elevation data terminology

### DEM

Digital elevation model is a broad term for sampled elevation. Dataset meaning
must be checked rather than inferred from the acronym.

### DTM / bare-earth model

Attempts to represent terrain ground surface with vegetation and buildings
removed.

### DSM / surface model

May include vegetation, buildings, and other above-ground surfaces.

A road corridor built directly from a DSM can inherit tree canopies, roofs, and
bridges as false terrain. Conversely, a bare-earth DTM will not provide the
structures needed for reflection or silhouette.

## 3. Elevation-data record

Record:

- provider and product;
- horizontal and vertical datum;
- coordinate reference system;
- grid spacing versus true resolving power;
- vertical accuracy and void policy;
- bare-earth versus surface semantics;
- acquisition sensor and date;
- vegetation/building contamination;
- interpolation and reprojection history;
- licence;
- scene scale and origin transformation.

A nominal `30 m DEM` does not guarantee 30 m feature fidelity.

## 4. Terrain frequency bands

```text
continental/regional form
    mountains, valleys, coastlines

landform scale
    ridges, fans, terraces, dunes, escarpments

slope process scale
    gullies, channels, talus, cuts, embankments

surface scale
    rills, stones, crust, tyre ruts, footprints

micro-scale
    grains, pores, fine roughness
```

Each band requires a source and LOD strategy. Upscaling a coarse DEM with noise
does not recover real landforms.

## 5. Hydrology as an authoring constraint

Water follows gravitational potential, surface roughness, permeability, and
obstructions. Terrain and road environments should include:

- drainage divides;
- channels and flow accumulation;
- depressions and ponding;
- infiltration and runoff differences;
- erosion at concentrated flow;
- deposition where transport energy falls;
- culverts, drains, ditches, kerbs, and human redirection.

`VA-RULE`: wetness, vegetation density, erosion, and deposited material should
share a common topographic logic where visible.

## 6. Erosion and deposition

### Water-driven

Rain splash, sheet flow, rills, gullies, channels, bank erosion, and flood
deposition. Feature scale and direction follow slope and drainage.

### Wind-driven

Deflation, saltation, suspension, dune formation, scour around obstacles, and
lee-side deposition. Wind direction and grain-size availability matter.

### Gravity-driven

Creep, rockfall, landslide, talus, and collapse. Deposits accumulate below
source slopes and sort by transport process.

### Human/vehicle-driven

Cuts, fills, compacted tracks, graded shoulders, quarrying, construction spoil,
and repeated tyre paths.

Procedural erosion is a model, not proof of geological accuracy. Its parameter
units and failure cases should be retained.

## 7. Soil classification

`AUTHORITATIVE`: USDA soil texture class is based on proportions of sand, silt,
and clay. This is only one axis of soil behaviour.

Other relevant properties:

- mineralogy and organic matter;
- aggregate structure;
- bulk density and compaction;
- porosity and permeability;
- moisture state;
- crusting and cracking;
- colour by horizon and oxidation state;
- gravel, cobble, and rock fragment content;
- salts and carbonates;
- roots and biological activity.

`VA-RULE`: `dirt` is not a material class. State the assumed soil/aggregate and
surface process.

## 8. Grain-size bands and representation

A terrain surface may include clay-scale particles through boulders. Rendering
ownership should follow visible scale:

- unresolved fines: albedo/roughness/statistical micro-normal;
- sand and small gravel: displacement, instances, or texture depending distance;
- cobbles and rocks: geometry/instances with contact and occlusion;
- boulders/outcrops: terrain geometry and structural geology.

Avoid representing all sizes with one fractal noise function.

## 9. Soil moisture

Moisture changes:

- substrate colour and saturation;
- refractive-index contrast at pores;
- cohesion and clumping;
- dust emission;
- track/rut formation;
- specular response;
- vegetation and biological cues;
- drainage and puddling.

Useful state vocabulary:

```text
powder dry
-> dry compacted
-> slightly moist
-> cohesive damp
-> plastic mud
-> saturated
-> standing water
-> drying crust
```

A mud system must distinguish water-rich surface slurry from darkened damp
soil.

## 10. Vehicle interaction with soil

Relevant effects:

- tyre sinkage and contact-patch widening;
- compaction;
- rutting;
- displaced side berms;
- tread imprint;
- mud adhesion and sling;
- dry dust emission;
- stone ejection;
- underbody and wheel-well accumulation;
- track persistence and collapse.

A physically complete terramechanics simulation is outside initial scope.
Production approximations must still tie deformation/emission to contact,
material state, load proxy, and motion.

## 11. Deposited dust on vehicles and hardscape

Dust deposition is driven by:

- gravitational settling;
- turbulent impaction;
- electrostatic attraction;
- rain splash and drying;
- capillary edge deposits;
- airflow separation and stagnation zones;
- human contact and cleaning;
- road spray carrying fines.

Expected vehicle patterns can include:

- horizontal-panel settling;
- rear wake accumulation;
- lower-body splash and road film;
- wheel-well loading;
- streaks below seams and drainage exits;
- cleaner wipe/contact zones;
- edge deposits after evaporation.

Generic cavity AO is not a dust model.

## 12. Suspended dust from roads

`AUTHORITATIVE`: paved-road dust often involves resuspension of loose material;
unpaved-road emissions involve tyre pulverization, lifting, and vehicle-wake
turbulence.

A dust system should separate:

- source reservoir on/in the road;
- emission rate proxy;
- coarse ballistic grains;
- suspended fine fraction;
- wake advection;
- wind advection;
- turbulent spread;
- settling and deposition;
- background aerosol.

Study-specific particle-size measurements may inform hypotheses but are not
universal presets.

## 13. Rocks and geological coherence

Rock assets should reflect:

- lithology and weathering style;
- bedding, foliation, jointing, or fracture orientation;
- source outcrop and downslope transport;
- angularity versus rounding;
- size sorting;
- lichen, dust, moisture, and burial.

Randomly scattering unrelated rocks over terrain quickly destroys geological
coherence and scale.

## 14. Vegetation as terrain evidence

Vegetation distribution is influenced by:

- climate and season;
- soil moisture and drainage;
- elevation and exposure;
- disturbance and maintenance;
- grazing/traffic;
- salt and pollution;
- shade and competition.

Vegetation should also influence:

- surface moisture and erosion;
- wind flow and dust;
- local shadow and reflection structure;
- litter and organic deposits;
- horizon density.

The initial environment domain does not attempt botanical simulation, but it
requires vegetation placement to share terrain and hydrology evidence.

## 15. Road cut, shoulder, and verge integration

Automotive scenes often fail at the transition between road and terrain.
Required cues include:

- constructed roadbed thickness;
- shoulder aggregate;
- ditch or kerb drainage;
- cut/fill slope geometry;
- erosion at outlets;
- compacted verge and tyre overrun;
- vegetation suppression near traffic;
- litter and sediment traps;
- guardrail/sign foundations.

A road ribbon floating over unrelated terrain is not acceptable for close or
moving shots.

## 16. Terrain shading and de-lighting

Photogrammetry and satellite imagery can contain:

- directional sun shadows;
- atmospheric haze;
- seasonal colour;
- sensor and compression artefacts;
- vegetation mixed with soil;
- parallax/orthorectification errors.

Do not use captured colour as diffuse albedo without assessing baked lighting.
Normals generated from colour are not measured surface orientation.

## 17. Procedural terrain rules

A process-aware procedural graph should expose:

- base landform source;
- erosion/deposition stage;
- hydrology fields;
- substrate classes;
- slope, curvature, elevation, and flow masks;
- disturbance/road construction;
- vegetation and debris response;
- moisture history;
- LOD and seed.

Every mask should have a causal interpretation or be labelled art direction.

## 18. LOD and floating origin

Large automotive environments require:

- stable world scale;
- camera/vehicle-relative precision strategy;
- displacement subdivision policy;
- near/mid/far terrain representation;
- consistent horizon silhouette;
- scatter density LOD;
- shadow and reflection LOD;
- motion-stable transitions.

A far terrain mesh can be visually coarse but must not pop in glossy vehicle
reflections.

## 19. Validation views

- orthographic elevation and slope maps;
- flow accumulation and basin overlays;
- metre-scale cross-sections;
- road/shoulder/terrain transition close-up;
- low grazing-light terrain render;
- wet/dry paired state;
- vehicle pass with dust/mud interaction;
- long-lens horizon and haze test;
- top-down distribution map for rocks/vegetation/deposition;
- fresh-file or deterministic regeneration.

## 20. Failure signatures

- drainage crosses ridges or ignores kerbs;
- wet patches appear at high points without a source;
- rocks have no source geology or downslope pattern;
- all slopes use equal vegetation density;
- erosion is isotropic noise;
- mud emits dust simultaneously from the same contact state;
- tyre tracks do not deform or disturb the material;
- terrain detail scale changes with object scaling;
- distant terrain contains near-field microdetail but poor silhouette;
- DSM artefacts are interpreted as ground;
- road and terrain occupy incompatible coordinate/datum systems.

## 21. Initial deliverable

VirtualAuto's first terrain deliverable should be a small metric road corridor,
not a continent:

```text
100–300 m road segment
+ crown/camber
+ shoulder and drainage
+ one soil class
+ dry/damp/wet states
+ controlled dust reservoir
+ near/mid/far terrain LOD
+ vehicle motion test
```

It should be built to diagnose the F40's paint, glass, tyre contact, lower-body
reflections, and motion—not to maximize procedural complexity.