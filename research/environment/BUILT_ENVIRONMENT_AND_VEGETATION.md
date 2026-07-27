# Built environment and vegetation

## 1. Why local surroundings matter to cars

Automotive surfaces reveal nearby geometry through reflection before that
geometry becomes visually prominent in the camera view. Buildings, walls,
trees, signs, gantries, kerbs, lamps, barriers, and road furniture create the
large and medium angular structures that describe body curvature.

A distant world map cannot provide correct parallax, contact shadow, or
finite-distance occlusion for these objects.

## 2. Reflection-structure hierarchy

Useful environment structures can be classified by their reflection footprint:

- **large bands:** sky/ground boundary, building façades, tree lines, studio
  cyclorama;
- **medium bands:** windows, walls, signs, barriers, trucks, hedges;
- **small peaks:** lamps, sun, retroreflectors, wet highlights, illuminated
  windows;
- **high-frequency clutter:** leaves, fence wire, gravel, façade details.

A car scene needs a deliberate distribution across this hierarchy. Too little
structure makes form unreadable; too much produces visual noise and aliasing.

## 3. Built-environment categories

- urban street canyon;
- suburban/residential road;
- industrial/service area;
- motorway/highway;
- mountain pass;
- circuit/paddock;
- bridge/tunnel;
- car park/garage;
- studio or architectural plaza;
- rural road.

Each category implies different road construction, lighting, drainage, scale,
traffic residue, signage, vegetation, and reflection structure.

## 4. Metric and regulatory context

Road furniture and markings are jurisdiction- and era-specific. Relevant
assets include:

- lane width and marking patterns;
- kerb profiles;
- barriers and guardrails;
- bollards and delineators;
- road studs and reflectors;
- signs and supports;
- drains and utility covers;
- lamps and mounting heights;
- bridge joints and expansion systems;
- tunnel linings and emergency equipment.

`VA-RULE`: if a scene claims a real location/period, dimensions and placement
must be sourced. Generic cinematic scenes may use a declared fictional standard.

## 5. Façade construction and ageing

Building materials should reflect construction:

- masonry modules, mortar joints, bonds, and repair;
- cast/precast concrete panels, joints, formwork, staining, and spalling;
- metal cladding seams, fasteners, coatings, and oxidation;
- glass curtain walls, mullions, coatings, blinds, and interior depth;
- painted render, cracks, moisture, and cleaning patterns;
- timber orientation, joints, finish, and weathering.

Random grunge cannot replace process, drainage, access, and maintenance history.

## 6. Window systems

Architectural glass can become a major secondary light/reflection source.
Consider:

- finite thickness and IOR;
- coatings and tint;
- interior/exterior luminance;
- blinds and curtains;
- pane segmentation;
- frame shadow and depth;
- dirt/cleaning patterns;
- reflections of sky and street;
- night emission.

A flat emissive rectangle is acceptable only at an appropriate distance/LOD.

## 7. Artificial lighting

Night environments require finite-distance, spatially distributed emitters:

- street lamps;
- vehicle lamps;
- signs and billboards;
- windows;
- shopfronts;
- tunnel fixtures;
- traffic signals;
- work lights;
- reflected city glow.

Record:

- source geometry and size;
- spectrum or colour-temperature proxy;
- luminous intensity/energy status;
- beam/IES profile where available;
- mounting position and orientation;
- flicker/time state;
- weather interaction;
- exposure and bloom ownership.

A visible emissive surface and a separate light can double count unless their
roles are coordinated.

## 8. IES and measured distributions

IES photometric files can represent directional luminous intensity from real
fixtures. They require:

- fixture identity and file provenance;
- unit/orientation verification;
- correct source scale and placement;
- visible luminaire geometry;
- colour/spectrum treatment;
- comparison with manufacturer documentation where possible.

An IES profile is not a material or spectrum.

## 9. Tunnels and enclosed roads

Tunnels alter:

- environment radiance from open sky to repeated local fixtures;
- exposure adaptation;
- reflections and acoustic/cinematic rhythm;
- road moisture and contamination;
- wall/ceiling soot and cleaning;
- ventilation haze;
- portal glare;
- headlight contribution.

Portal transition should be tested in motion. A static exposure that works
inside and outside may be impossible without an explicit camera strategy.

## 10. Vegetation categories

Vegetation influences automotive environments through:

- silhouette and horizon density;
- broad green/seasonal reflection bands;
- high-frequency leaf highlights;
- shadow breakup;
- wind evidence;
- moisture and dust interception;
- litter and organic deposits;
- local cooling/fog/shelter cues;
- scale.

Separate:

- canopy/tree mass;
- trunk/branch structure;
- shrub/hedge mass;
- grasses and verge;
- ground litter;
- dead/dry vegetation;
- managed versus wild growth.

## 11. Botanical and ecological coherence

Full botanical simulation is outside initial scope, but placement should respect:

- climate and season;
- moisture and drainage;
- sun/shade;
- elevation and exposure;
- soil/substrate;
- maintenance and disturbance;
- road salt and pollution;
- competition and succession.

A random global scatter with equal density on road, rock, ditch, and shaded
forest fails basic ecological coherence.

## 12. Vegetation shading

Leaves are thin, oriented, often glossy/translucent structures. Important cues:

- front/back response;
- transmission and subsurface proxy;
- cuticle gloss;
- leaf-angle distribution;
- variation by age, hydration, and species;
- canopy self-shadowing;
- wind motion;
- LOD stability.

Billboards/cards are valid at distance but can collapse in car reflections,
shadow, and motion. Test them from reflective viewpoints, not only camera view.

## 13. Wind and motion coherence

Vegetation motion provides a strong cue for wind that must agree with:

- rain streaks;
- dust/spray drift;
- cloud motion;
- loose litter;
- surface drying;
- vehicle wake.

Different vegetation scales respond at different frequencies. One synchronized
sine wave across every tree is not acceptable.

## 14. Scatter and LOD

A practical scatter system should separate:

- hero finite geometry near vehicle/camera;
- mid-ground instanced assets;
- far canopy/silhouette representation;
- reflection and shadow LOD;
- wind animation LOD;
- density/size distributions;
- deterministic seeds and exclusion masks.

LOD transitions must be checked in glossy paint, where pop can be more obvious
than in the visible background.

## 15. Background density and scale

An environment should not be uniformly detailed. Detail density should fall
with distance and be organized by scene function:

- near zone: contact, parallax, readable construction;
- middle zone: reflection structure, occlusion, motion cues;
- far zone: horizon and broad colour/luminance mass;
- sky: far-field radiance and weather.

The far background must preserve silhouette and atmospheric integration rather
than carrying unnecessary microdetail.

## 16. Dirt and maintenance patterns

Built environments collect contamination through:

- rain runoff and drip edges;
- rising damp;
- splash zones;
- road spray;
- tyre/foot traffic;
- exhaust and soot;
- cleaning access;
- graffiti/removal;
- vegetation contact;
- leaks and drainage failure.

The pattern should identify source, transport, and deposition. AO-only dirt is
not sufficient.

## 17. Automotive reflection diagnostics

Render the vehicle with:

- sky only;
- built geometry matte grey;
- built geometry actual materials;
- vegetation disabled/enabled;
- artificial lights isolated;
- camera orbit and drive-through;
- mirror/chrome proxy at vehicle positions.

Look for:

- reflection bands that describe body form;
- impossible infinite-distance near objects;
- card/LOD pop;
- mismatch between visible and reflected architecture;
- excessive high-frequency clutter;
- artificial lights lacking visible sources;
- vegetation motion inconsistent with weather.

## 18. Initial F40 environment recommendation

For first F40 material and glass qualification, use a restrained corridor:

- one road surface with metric scale;
- a low wall or façade on one side;
- tree/hedge mass on the other;
- open sky above;
- a controlled horizon;
- optional lamp/sign structures;
- no dense city clutter.

This provides broad asymmetric reflection structure that can expose windshield
normal discontinuities and paint curvature without burying the diagnosis in a
complex environment.