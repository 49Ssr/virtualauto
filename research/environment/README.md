# Automotive environment research

Environment is an appearance-forming system, not a backdrop. Vehicle paint,
glass, carbon, lamps, tyres, roads, dust, and wetness only read correctly when
the surrounding radiance field, participating media, ground response, weather,
and camera pipeline are internally coherent.

This domain uses Blender `5.0.1` as the production baseline. Blender `5.2 LTS`
may be used as a forward compatibility target, but no feature or result is
promoted to production status until the exact version and execution path are
recorded.

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

No environment result in this directory is `VA-VALIDATED` at creation time.

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

- [Environment ontology and ownership](ONTOLOGY_AND_SCOPE.md)
- [Atmosphere and sky](ATMOSPHERE_AND_SKY.md)
- [Aerosols, ozone, and visibility](AEROSOLS_OZONE_AND_VISIBILITY.md)
- [HDRI and image-based lighting](HDRI_AND_IBL.md)
- [Roads and hardscape](ROADS_AND_HARDSCAPE.md)
- [Terrain, soil, and dust](TERRAIN_SOIL_AND_DUST.md)
- [Weather and hydrometeors](WEATHER_AND_HYDROMETEORS.md)
- [Built environment and vegetation](BUILT_ENVIRONMENT_AND_VEGETATION.md)
- [Camera, colour, and compositing boundaries](CAMERA_COLOR_AND_COMPOSITING.md)
- [Blender 5.0.1 implementation cards](BLENDER_IMPLEMENTATION_CARDS.md)
- [Validation and experiment backlog](VALIDATION_AND_EXPERIMENTS.md)
- [Claim-to-source map](CLAIM_SOURCE_MAP.md)
- [Open questions and contradictions](OPEN_QUESTIONS_AND_CONTRADICTIONS.md)
- [Source register](SOURCE_REGISTER.md)

Machine-readable environment ownership is specified by
[`environment-profile.schema.json`](../../lab/schemas/environment-profile.schema.json).
The corresponding
[fictional example profile](../../lab/examples/environment_profile.json) is
executable documentation, not retained F40 evidence.

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

## Production objective

The immediate target is a reusable automotive environment framework that can
support the DriveClub Ferrari F40 without forcing material tuning to compensate
for an incoherent scene. A car material must remain interpretable across a
small, controlled set of dry, wet, hazy, overcast, and night environments
before it is considered robust.