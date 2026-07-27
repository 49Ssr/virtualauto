# Environment research practicality audit

## Verdict

The environment domain is scientifically careful and structurally useful, but the
first version overweights breadth, taxonomy, and defensive provenance relative to
what an automotive Blender artist can build this week.

It is not bad research. The failure mode is different: a strong reference library
can still become operationally inert when it gives atmospheric chemistry, snow
optics, cloud classification, road engineering, wet-surface transport, camera
science, and Blender implementation equal visual weight.

For VirtualAuto, environment knowledge is successful only when it helps answer one
of these questions:

1. What should be built in Blender?
2. Which object, node tree, texture, volume, or camera setting owns the effect?
3. What should be measured or recorded?
4. What can be ignored for the present shot?
5. How do we know the environment is not forcing the car material to lie?

The original domain answers questions 2, 3, and 5 well. It needs stronger answers
to 1 and 4.

## Audit criteria

Each topic is judged by:

- **automotive appearance leverage** — how strongly it affects paint, glass,
  silhouette, contact, scale, and motion;
- **direct Blender relevance** — whether it maps to current Blender objects,
  nodes, render settings, geometry, or compositor controls;
- **implementation readiness** — whether a competent user can build a controlled
  first version without inventing the missing half;
- **validation cost** — time and evidence needed before a result becomes useful;
- **current F40 relevance** — whether it helps the sourced DriveClub F40 now.

Scores are planning weights, not physical-importance rankings.

## Practical priority matrix

| Topic | Appearance leverage | Blender directness | Ready now | F40 now | Decision |
| --- | ---: | ---: | ---: | ---: | --- |
| finite reflection structures and broad bands | 5 | 5 | 5 | 5 | build first |
| camera, exposure, colour management | 5 | 5 | 4 | 5 | lock first |
| dry road, horizon, contact and lower hemisphere | 5 | 5 | 4 | 5 | build first |
| HDRI qualification and role separation | 5 | 5 | 4 | 4 | core workflow |
| sky/direct-sun ownership | 4 | 5 | 4 | 4 | core workflow |
| geometric/custom-normal diagnostics | 5 | 5 | 5 | 5 | immediate |
| bounded haze/fog | 3 | 4 | 3 | 2 | add only after dry baseline |
| built environment and vegetation mass | 4 | 4 | 3 | 3 | add as finite reflection structure |
| wet road state | 4 | 4 | 2 | 2 | second production milestone |
| terrain and road integration | 3 | 4 | 2 | 2 | shot-dependent |
| rain streaks and spray | 3 | 3 | 2 | 1 | later |
| windshield droplets and wipers | 4 | 3 | 1 | 1 | specialist system; do not mix with current glass fault |
| dust deposition/resuspension | 2 | 3 | 2 | 1 | situational |
| aerosol and ozone measurement theory | 2 | 2 | 1 | 1 | reference tier |
| cloud taxonomy and morphology | 2 | 2 | 1 | 1 | art-direction/reference tier |
| snow and ice optics | 1 | 2 | 1 | 0 | parked |

The most important correction is obvious: for glossy cars, **finite reflection
content, ground coherence, camera lock, and normal diagnosis produce more immediate
value than deeper atmospheric chemistry**.

## What the first version gets right

### Ownership is excellent

Separating World radiance, direct lights, finite reflectors, local volumes, ground,
weather, and camera/post is the strongest part of the domain. It prevents the
common failure where an HDRI, Sun light, compositor haze, wet-road shader, and
material tweaks all compensate for each other.

### The HDRI chapter is production-relevant

The distinction between lighting, reflection, background, and local reconstruction
is immediately useful. So are sun clipping, horizon, lower hemisphere, projection,
parallax, stitching, dynamic-range, and rights checks.

### The F40 diagnostic order is correct

The neutral asymmetric corridor is more valuable than adding a cinematic HDRI.
The current windshield triangles must be classified before transmission maps,
droplets, glare, or weather are allowed to hide them.

### The dry-to-wet state separation is conceptually correct

Keeping dry substrate, pore darkening, thin water, standing water, drainage, and
spray eligibility separate is a sound ownership model. It prevents the one-slider
wet-asphalt failure.

### The research refuses false precision

Blender Sky Texture controls are not represented as meteorological measurements,
and a government road or soil definition is not silently converted into a shader
preset. That restraint must remain.

## Where the first version fails in practice

### 1. It reads like a complete discipline rather than a production decision tree

A user can read hundreds of lines and still not know what to create first in an
empty Blender file. Research breadth is not the same as build order.

**Correction:** provide a minimum viable rig, exact collection ownership, a scene
construction order, starter implementation values, and explicit stop points.

### 2. Too many topics appear equally urgent

Ozone, snow grain size, aerosol absorption, cloud genera, drainage, road texture,
HDRI calibration, and glass diagnostics all live beside one another. This is
accurate as a library but poor as an active workflow.

**Correction:** every domain item is assigned to one of four tiers:

- `T0-diagnostic-core` — build immediately;
- `T1-production-core` — required for ordinary dry hero work;
- `T2-shot-dependent` — add only when the shot demands it;
- `T3-research-reference` — retain for future modelling and source interpretation.

### 3. The implementation cards are contracts, not recipes

They say what a system owns and how it can fail, but often stop before exact Blender
object/node construction, starter values, naming, execution order, and a minimal
render test.

**Correction:** preserve the contracts, then pair them with executable or
step-by-step build recipes. A contract prevents semantic drift; a recipe gets work
done. They are not substitutes.

### 4. The environment profile is intentionally complete but heavy for diagnosis

The schema requires World, direct lighting, atmosphere, ground, weather, camera,
diagnostics, and limitations even when a glass test deliberately uses no weather
or atmosphere. This makes missing ownership visible, but it also encourages large
forms full of `unresolved` values.

**Correction:** keep the full schema for provenance, but publish a compact starter
profile using explicit `none` states and clearly labelled `implementation-default`
values. A profile should take minutes to copy for a diagnostic scene, not become a
research project before the scene exists.

### 5. The original example is too cautious to operate

The fictional F40 example leaves most useful values null. It proves that the schema
can hold uncertainty but does not prove that the workflow can build a useful rig.

**Correction:** add a second fictional `P2-buildable` starter profile. Its values
are not claimed physical; they are deterministic diagnostic defaults.

### 6. There is no performance or complexity budget

Volumes, dense road displacement, vegetation, rain, droplets, reflection geometry,
and high-resolution HDRIs can each become the dominant scene cost. The original
research records renderer limitations but does not provide a practical budget or
LOD escalation rule.

**Correction:** require three complexity states:

- `diagnostic` — static, no weather, no volumetric complexity, minimal local
  structures;
- `lookdev` — dry hero environment with stable road, horizon, reflection structures,
  and optional light haze;
- `beauty` — shot-specific terrain, weather, motion, and post effects.

Nothing enters `beauty` before its lower tier is stable.

### 7. Physical vocabulary can become cargo cult

Terms such as Rayleigh, Mie, aerosol optical depth, phase function, microtexture,
macrotexture, megatexture, hydrometeor, and DEM/DTM/DSM are useful only when they
change a decision. Otherwise they create the appearance of rigour while the scene
still uses arbitrary noise and exposure.

**Correction:** every technical term in an implementation document must answer:

- what observable does it change?
- what Blender control or asset does it inform?
- what mistake does it prevent?
- is it needed for this shot?

If no answer exists, the term stays in reference research and leaves the build
workflow.

### 8. Some engineering scale bands are informative but not shader laws

Pavement texture terminology is valuable for separating contact-scale geometry
from shading detail. It does not mean Blender must use four literal texture nodes
with hard boundaries copied from road engineering.

**Correction:** use the bands as a diagnostic ownership framework. Let camera
distance, pixel footprint, tyre contact, displacement cost, and shot scale decide
implementation.

### 9. Weather systems are too ambitious for the first production milestone

Rain streaks, road accumulation, tyre spray, windshield droplets, wipers, camera
contamination, drying, and wind coupling form several interacting simulations.
Trying to build them as one environment feature would recreate the exact opaque
proprietary-system problem VirtualAuto is trying to escape.

**Correction:** weather is split into independently testable systems. The first
weather milestone is only dry-to-damp-to-wet road state under fixed illumination.
Windshield water remains separate until the underlying glass is clean.

## Reweighted production model

### T0 — diagnostic core

Build and retain first:

- metric units and known car placement;
- locked camera and colour-management record;
- neutral World or one known sky;
- no local atmosphere;
- broad asymmetric finite reflectors;
- dry neutral ground and simple horizon;
- chrome, grey, black-gloss, and glass diagnostic objects;
- contribution toggles;
- normal, UV, attribute, face, and material diagnostics.

This is the current F40 priority.

### T1 — production core

Add after T0 is understood:

- qualified analytic sky or HDRI;
- explicit direct-sun owner;
- production dry road with metric scale and lower-hemisphere coherence;
- finite buildings/walls/trees that materially affect reflections;
- stable horizon and camera-visible background;
- material robustness turntable or camera move;
- render-time and memory record.

### T2 — shot-dependent systems

Add only when demanded by the shot:

- bounded haze/fog;
- detailed terrain;
- vegetation LOD;
- night fixtures;
- damp/wet/ponded road states;
- dust deposition;
- active precipitation;
- spray;
- lens contamination.

### T3 — research reference

Retain, but do not block ordinary production on:

- atmospheric chemistry or real-column inversion;
- full aerosol classification;
- cloud taxonomy beyond useful shape reference;
- snow spectral modelling;
- physically detailed droplet coalescence;
- complete hydrology or erosion simulation;
- real meteorological reconstruction without measured inputs.

## Blender relevance corrections

### Sky Texture

The Sky Texture is directly relevant for controllable far-field radiance. It does
not generate nearby reflection architecture, road geometry, local aerial
perspective, or a complete weather system. The default Vector input can be left
unconnected for a straightforward World setup; vector manipulation should be added
only when its coordinate purpose is explicit.

### HDRI

The Environment Texture is high-value, but an HDRI must be qualified by role.
Automotive use cares unusually strongly about high-frequency bright structures,
lower-hemisphere content, and local parallax. A beautiful panorama can be a poor
paint-lighting asset.

### Sun light

The Sun object is practical for stable direction, shadow softness, and animation.
It becomes dangerous only when the World or HDRI already owns a solar peak and the
split is not diagnosed.

### Volumes

Bounded volumes are useful for local haze and fog. They are expensive, noisy, and
engine-sensitive. They should not appear in the diagnostic rig, and they should
not be used merely because atmospheric research exists.

### Road

The road is not set dressing. It owns tyre contact, scale, lower-body reflection,
shadow reception, spray eligibility, and a large part of the image's lower
hemisphere. A modest coherent road is more valuable than a complex distant terrain
system.

### Camera and colour

Environment and camera cannot be tuned independently in practice, but their
ownership must remain distinct. Exposure and display transform are observation
controls; they are not replacements for missing radiance or broken material
parameters.

## Practical acceptance gates

An environment is useful for F40 material and glass work when:

1. the car scale and ground contact are credible;
2. broad reflections move continuously over known-good diagnostic objects;
3. the windshield artefact can be classified under opaque, specular, and glass
   stages;
4. World, direct, and local-reflector contributions can be isolated;
5. exposure and colour management remain fixed between variants;
6. no volume, weather, or post effect is needed to make the car readable;
7. the scene can be rebuilt or linked without manual archaeology;
8. performance is acceptable for repeated orbit and environment-rotation tests.

It is not necessary for this first environment to contain real atmospheric ozone,
cloud simulation, terrain erosion, rain, or production vegetation.

## Immediate decisions

- Keep the broad environment research as the long-term reference layer.
- Stop treating all environment categories as one active milestone.
- Make the F40 glass corridor the first executed environment asset.
- Add deterministic starter values as implementation defaults, not physical facts.
- Add a non-destructive Blender builder for the corridor.
- Execute the builder in Blender `5.0.1` before promoting it beyond `P2-buildable`.
- Defer wet-road physics until the dry F40 glass and paint baselines are stable.
- Defer windshield water until the windshield itself has passed normal/topology and
  material isolation.

## Final assessment

The research is worth keeping. The practical mistake would be using its breadth as
an excuse to build everything.

For automotive CG, the environment's first job is not to reproduce the atmosphere
of Earth. Its first job is to provide coherent, finite, scale-correct radiance that
reveals the vehicle honestly. Everything else is conditional.