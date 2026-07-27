# Automotive environment production ladder

This document turns the environment research library into a build order. It is not
a substitute for the source-backed domain documents; it decides when they become
relevant.

Production baseline: Blender `5.0.1`.

## Level 0 — geometry and material diagnosis

Use for:

- imported-normal and topology faults;
- UV/attribute isolation;
- glass debugging;
- Class-A reflection continuity;
- basic paint robustness.

Build only:

1. metric scene units;
2. a dry neutral ground plane;
3. a neutral World background;
4. one broad bright reflector on one side;
5. a different-sized bright reflector and a dark absorber on the other;
6. chrome, grey, black-gloss, and glass proxy objects;
7. one locked camera plus orbit/environment-rotation variants;
8. contribution and normal/attribute diagnostics.

Do not add:

- HDRI;
- Sun light unless it is the tested variable;
- atmosphere or compositor haze;
- terrain detail;
- clouds;
- wetness;
- rain;
- lens effects.

Exit Level 0 when artefacts can be classified as geometry-, normal-, tangent-,
attribute-, material-, overlap-, view-, or engine-linked.

## Level 1 — dry automotive look development

Use for:

- paint, glass, trim, tyre, lamp, carbon, and metal qualification;
- stable hero-car turntables;
- reflection-line and panel-continuity checks.

Add:

- one qualified analytic sky or HDRI;
- an explicit direct-sun policy;
- finite local structures that create useful reflection bands;
- a road with coherent metric texture and lower-hemisphere response;
- simple horizon and background;
- fixed camera/colour pipeline;
- moving camera or vehicle test;
- render-time and memory capture.

Minimum acceptance:

- no accidental solar double counting;
- no material retuning required merely because the environment rotates;
- road scale remains stable under object transforms;
- reflections move continuously over known-good geometry;
- visible background and reflected environment do not contradict one another at
  the shot scale;
- the setup survives a fresh-file link/build test.

## Level 2 — shot-specific exterior environment

Add only what the shot can see or reflect:

- road camber, shoulder, kerb, drainage, markings, patches, and local contamination;
- terrain cut/fill and horizon silhouettes;
- buildings, barriers, trees, gantries, signs, and lamps;
- bounded haze or fog;
- vegetation and background LOD;
- camera plate or compositor integration;
- shot-specific artificial lighting.

A Level 2 scene does not need a complete world. It needs a coherent camera frustum,
reflection field, shadow field, and motion path.

## Level 3 — wet surface state

Start from the accepted dry scene. Add in this order:

1. damp substrate darkening;
2. connected thin-film wetness;
3. low-point accumulation;
4. explicit standing-water geometry where visible;
5. runoff/flow masks;
6. tyre-contact disturbance and spray eligibility;
7. drying history.

Do not add rain yet. The wet-surface state must work as a static environment before
precipitation and spray obscure it.

Exit Level 3 when:

- the dry substrate is still identifiable;
- water is dielectric, not metallic;
- puddles respond to topography;
- lower-body reflections and road appearance agree;
- the same scene can render dry/damp/wet/ponded variants at fixed exposure.

## Level 4 — active weather

Add independently testable systems:

1. cloud/illumination state;
2. visibility volume;
3. falling precipitation;
4. ground impact and splash;
5. tyre spray;
6. body and windshield water;
7. wipers;
8. lens contamination;
9. post-rain drying.

Each system must have an off state and diagnostic output. Shared wind, vehicle
motion, and weather history are explicit inputs rather than hidden assumptions.

## Level 5 — specialised environmental reconstruction

Reserve for shots or research that justify the cost:

- real-location sun/sky reconstruction;
- measured HDR capture and calibration;
- detailed aerosol/visibility fitting;
- physically informed cloud or snow models;
- full terrain-data ingestion;
- long-duration hydrology, deposition, or erosion;
- DriveClub weather-system archaeology.

Level 5 knowledge must not block Levels 0–2.

## Minimum collection ownership

Suggested Blender collections:

```text
VA_ENV_DIAGNOSTICS
VA_ENV_WORLD
VA_ENV_DIRECT
VA_ENV_REFLECTORS
VA_ENV_GROUND
VA_ENV_TERRAIN
VA_ENV_ATMOSPHERE
VA_ENV_WEATHER
VA_ENV_CAMERA_POST
```

These names are human workflow defaults, not permanent API promises. The practical
requirement is that every contribution can be isolated without editing the car
material.

## Practical environment presets

A preset is accepted only when its status is explicit:

- `diagnostic-default` — deterministic values selected to expose faults;
- `artist-default` — useful starting point with no physical calibration claim;
- `calibrated` — fitted to retained reference or measurement;
- `measured` — supported by retained measurement/provenance;
- `source-recovered` — reconstructed from source assets with evidence;
- `production-qualified` — accepted for named roles after Blender tests.

Do not call a preset `physical` merely because it uses a Sky Texture, Principled
BSDF, a volume node, or metric units.

## Cost escalation rule

Before adding any system, answer:

1. Is it visible to the camera?
2. Is it visible in paint, glass, chrome, lamps, or wet-road reflections?
3. Does it cast a required shadow or affect contact?
4. Does it change motion, accumulation, or visibility?
5. Can a cheaper representation preserve the observable?

If every answer is no, omit it.

## Current F40 path

The F40 should proceed:

```text
Level 0 glass corridor
-> Level 0 paint/normal orbit
-> Level 1 dry road and reflection environment
-> Level 1 qualified sky/HDRI comparisons
-> Level 3 static wet-road state
-> Level 4 rain only after glass and road are stable
```

The current windshield artefact is a Level 0 problem. Ozone, rain, droplets, and
terrain are not valid dependencies for solving it.