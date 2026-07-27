# Automotive environment research

Environment is an appearance-forming system, not a backdrop. Vehicle paint,
glass, carbon, lamps, tyres, roads, dust, and wetness only read correctly when
the surrounding radiance field, participating media, ground response, weather,
and camera pipeline are internally coherent.

This domain uses Blender `5.0.1` as the production baseline. Blender `5.2 LTS`
may be used as a forward compatibility target, but no feature or result is
promoted to production status until the exact version and execution path are
recorded.

## Start here

The domain is intentionally broad, but the build order is not.

1. Read the [practicality audit](PRACTICALITY_AUDIT.md).
2. Use the [production ladder](PRODUCTION_LADDER.md) to decide what belongs in the
   current scene.
3. Use the [experiment priority](EXPERIMENT_PRIORITY.md) rather than treating the
   complete backlog as an active queue.
4. For the sourced F40 windshield issue, follow the
   [glass diagnostic quickstart](../../workflows/environment/F40_GLASS_QUICKSTART.md)
   before adding an HDRI, atmosphere, weather, droplets, or post effects.
5. Use the source-backed chapters only when the active production level reaches
   them.

The current priority order is:

```text
finite reflection structure
-> camera and colour lock
-> dry ground and lower hemisphere
-> normal/UV/material diagnostics
-> qualified sky or HDRI
-> direct-sun ownership
-> shot-specific terrain/atmosphere
-> static wet state
-> active weather
-> specialist atmospheric or hydrological research
```

## Practical tiers

- `T0-diagnostic-core` — metric ground, neutral World, finite reflection bands,
  camera lock, diagnostic objects, normal/attribute isolation.
- `T1-production-core` — qualified sky/HDRI, explicit direct light, coherent dry
  road, finite reflected context, horizon, motion and performance checks.
- `T2-shot-dependent` — terrain, vegetation, bounded haze, wet road, night lights,
  dust, precipitation, spray, and post effects.
- `T3-research-reference` — atmospheric chemistry, full aerosol fitting, detailed
  cloud/snow optics, hydrology, erosion, and other specialist reconstructions.

Research in a later tier must not block an earlier production task.

## Evidence labels

| Label | Meaning |
| --- | --- |
| `BLENDER-DOC` | Official Blender documentation for the stated version |
| `PRIMARY` | Primary research paper, standards body, or original technical report |
| `AUTHORITATIVE` | Governmental, intergovernmental, or standards-based reference |
| `SECONDARY` | Useful explanatory or community source; not sufficient alone for a strong claim |
| `OBS-USER` | Direct user report without retained repository evidence |
| `HYP` | Falsifiable interpretation awaiting a controlled test |
| `VA-RULE` | VirtualAuto implementation or evidence rule |
| `VA-VALIDATED` | Reproduced by VirtualAuto with linked evidence |

No environment result in this directory is `VA-VALIDATED` merely because it is
well sourced or structurally validated.

## System decomposition

A production environment is divided by physical and implementation ownership:

1. **Far-field radiance** — sky model or environment map.
2. **Direct emitters** — sun, moon, lamps, signs, and local fixtures.
3. **Participating media** — haze, fog, smoke, suspended dust, clouds, and rain
   shafts.
4. **Ground and hardscape** — road, kerb, concrete, gravel, soil, markings,
   drainage, and local reflectors.
5. **Terrain and horizon** — macro-scale form, elevation, silhouettes, and
   occlusion.
6. **Weather state** — precipitation, wind, accumulation, evaporation, melt,
   spray, and deposition.
7. **Surface state** — dry, dusty, damp, wet, ponded, icy, snowy, contaminated,
   or recently cleaned.
8. **Built context** — architecture, road furniture, vegetation, artificial
   lights, and finite reflection structure.
9. **Camera and display** — exposure, white balance, lens, motion, flare,
   colour management, and output transform.

These layers may share data, but they must not silently own the same energy or
phenomenon twice.

## Documents

### Practical control

- [Practicality audit](PRACTICALITY_AUDIT.md)
- [Production ladder](PRODUCTION_LADDER.md)
- [Experiment priority](EXPERIMENT_PRIORITY.md)
- [Blender 5.0.1 implementation cards](BLENDER_IMPLEMENTATION_CARDS.md)
- [Validation and complete experiment backlog](VALIDATION_AND_EXPERIMENTS.md)

### Source-backed reference

- [Environment ontology and ownership](ONTOLOGY_AND_SCOPE.md)
- [Atmosphere and sky](ATMOSPHERE_AND_SKY.md)
- [Aerosols, ozone, and visibility](AEROSOLS_OZONE_AND_VISIBILITY.md)
- [HDRI and image-based lighting](HDRI_AND_IBL.md)
- [Roads and hardscape](ROADS_AND_HARDSCAPE.md)
- [Terrain, soil, and dust](TERRAIN_SOIL_AND_DUST.md)
- [Weather and hydrometeors](WEATHER_AND_HYDROMETEORS.md)
- [Built environment and vegetation](BUILT_ENVIRONMENT_AND_VEGETATION.md)
- [Camera, colour, and compositing boundaries](CAMERA_COLOR_AND_COMPOSITING.md)
- [Real camera and atmosphere pipeline](REAL_CAMERA_AND_ATMOSPHERE_PIPELINE.md)
- [Claim-to-source map](CLAIM_SOURCE_MAP.md)
- [Open questions and contradictions](OPEN_QUESTIONS_AND_CONTRADICTIONS.md)
- [Source register](SOURCE_REGISTER.md)

Machine-readable environment ownership is specified by
[`environment-profile.schema.json`](../../lab/schemas/environment-profile.schema.json).
The deliberately unresolved
[research example](../../lab/examples/environment_profile.json) demonstrates
uncertainty handling. The
[starter profile](../../lab/examples/environment_profile_f40_glass_starter.json)
demonstrates deterministic implementation defaults for a buildable diagnostic rig.
Neither is retained evidence from the private F40.

## Non-negotiable boundaries

- A pleasing sky is not evidence of a physically coherent atmosphere.
- An HDRI is not automatically calibrated, unclipped, correctly oriented, or
  suitable for both lighting and visible background use.
- A wet road is not a dry road with one roughness value reduced.
- Mist Pass is a depth mask for compositing, not participating-media transport.
- World volume is not treated as a complete planetary-atmosphere model.
- EEVEE and Cycles are not assumed to agree where their volume and reflection
  models differ.
- Blender Sky Texture `Air`, `Dust`, and `Ozone` controls are model parameters;
  they are not silently re-labelled as measured aerosol optical depth, PM2.5,
  humidity, or Dobson units.
- No weather, terrain, or surface-state system may invent conservation,
  drainage, or accumulation behaviour without declaring the approximation.
- No external HDRI, terrain dataset, scan, or proprietary game environment is
  committed without a rights and provenance review.
- Scientific terminology that does not change a Blender decision stays in the
  reference tier rather than inflating the active workflow.

## Production objective

The immediate target is not a universal Earth simulator. It is a reusable,
scale-correct automotive environment framework that reveals the DriveClub Ferrari
F40 honestly without forcing the car material to compensate for an incoherent
scene.

The first executed asset should be the Level 0 glass diagnostic corridor. Dry hero,
wet-road, weather, and specialist atmosphere systems follow only after the glass,
paint, road contact, and camera pipeline are stable.
