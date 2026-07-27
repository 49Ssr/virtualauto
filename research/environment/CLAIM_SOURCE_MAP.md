# Environment claim-to-source map

This map connects the domain's load-bearing claims to registered sources. It is
not a substitute for reading the source conditions, equations, units, or
limitations. Claims marked `VA-RULE` are repository policy derived from the
evidence and workflow goals rather than quotations from a source.

| Claim ID | Claim | Evidence class | Source IDs | Scope / limitation |
| --- | --- | --- | --- | --- |
| `CLM-ENV-001` | Blender 5.0 Sky Texture exposes Preetham, Hosek/Wilkie, and Nishita families. | `BLENDER-DOC` | `SRC-ENV-BLENDER-SKY-5.0` | Exact Blender 5.0 user-facing models; not a claim of equation identity beyond documentation/source review. |
| `CLM-ENV-002` | Nishita exposes sun, altitude, Air, Dust, and Ozone controls. | `BLENDER-DOC` | `SRC-ENV-BLENDER-SKY-5.0` | Control labels do not establish physical-unit mappings. |
| `CLM-ENV-003` | Blender documentation warns that an infinitely filled World volume is a poor assumption for terrestrial fog/atmospheric scattering and recommends a bounded volume. | `BLENDER-DOC` | `SRC-ENV-BLENDER-VOLUME-5.0` | Blender implementation guidance, not a complete atmosphere solution. |
| `CLM-ENV-004` | Cycles volume bounces and EEVEE multiple-scattering support differ materially. | `BLENDER-DOC` | `SRC-ENV-BLENDER-VOLUME-5.0`, `SRC-ENV-BLENDER-EEVEE-LIMITS-5.0` | Must be checked for exact engine/build settings. |
| `CLM-ENV-005` | Mist Pass is a depth-derived compositor aid, not participating-media transport. | `BLENDER-DOC` + `VA-RULE` | `SRC-ENV-BLENDER-MIST-5.0` | It remains useful for diagnostics/art direction. |
| `CLM-ENV-006` | The Preetham model is an inexpensive analytic daylight approximation. | `PRIMARY` | `SRC-ENV-PREETHAM-1999` | Historical model with documented domain weaknesses. |
| `CLM-ENV-007` | Hosek/Wilkie improves sunset and high-turbidity behaviour and includes ground-albedo/spectral treatment. | `PRIMARY` | `SRC-ENV-HOSEK-WILKIE-2012` | A fitted analytic sky model, not local scene transport. |
| `CLM-ENV-008` | Physically structured atmospheric references distinguish molecular, aerosol, absorption, multiple-scattering, and aerial-perspective contributions. | `PRIMARY` | `SRC-ENV-BRUNETON-NEYRET-2008`, `SRC-ENV-BRUNETON-2016` | Does not assert Blender implements the same solver. |
| `CLM-ENV-009` | Molecular Rayleigh scattering is strongly wavelength dependent and accurate optical depth depends on atmospheric properties beyond one blue colour. | `PRIMARY` | `SRC-ENV-BODHAINE-1999` | Approximate wavelength-power statements are conceptual unless a spectral calculation is specified. |
| `CLM-ENV-010` | Aerosol optical depth measures column extinction from scattering plus absorption and is not identical to horizontal visibility. | `AUTHORITATIVE` | `SRC-ENV-NOAA-AOD`, `SRC-ENV-NOAA-STAR-AEROSOL` | Spatial/vertical structure remains necessary for local scene visibility. |
| `CLM-ENV-011` | Aerosol composition and size change scattering and absorption behaviour. | `AUTHORITATIVE` + `PRIMARY` | `SRC-ENV-NASA-AEROSOLS`, `SRC-ENV-BERGSTROM-2007` | No universal RGB dust colour or anisotropy follows. |
| `CLM-ENV-012` | Most atmospheric ozone occupies a stratospheric vertical region rather than a uniform scene volume. | `AUTHORITATIVE` | `SRC-ENV-NASA-OZONE` | Blender's Ozone control is not automatically a vertical profile. |
| `CLM-ENV-013` | High-dynamic-range image-based lighting uses captured scene radiance and benefits from separating distant and local scene components. | `PRIMARY` | `SRC-ENV-DEBEVEC-1998`, `SRC-ENV-DEBEVEC-MALIK-1997` | Public HDRIs require independent capture/processing qualification. |
| `CLM-ENV-014` | An environment map has no finite-depth parallax around the capture point. | `PRIMARY` + geometric inference | `SRC-ENV-DEBEVEC-1998` | Local reconstruction is required when nearby geometry matters. |
| `CLM-ENV-015` | Pavement texture spans microtexture, macrotexture, megatexture, and longer-wave profile/roughness bands. | `AUTHORITATIVE` | `SRC-ENV-FHWA-TEXTURE`, `SRC-ENV-FHWA-SAFETY` | The exact band definitions follow the cited FHWA context. |
| `CLM-ENV-016` | Microtexture and macrotexture influence wet-weather friction and drainage/spray behaviour. | `AUTHORITATIVE` | `SRC-ENV-FHWA-TEXTURE`, `SRC-ENV-FHWA-SAFETY` | Rendering implementation does not simulate tyre friction automatically. |
| `CLM-ENV-017` | Wet pavement combines substrate optical change with water-interface reflection and cannot be represented generally by one roughness scalar. | `PRIMARY` + `VA-RULE` | `SRC-ENV-WET-ASPHALT-OPTICS` | Numerical shader mappings remain unresolved pending specific paper registration and experiment. |
| `CLM-ENV-018` | Paved-road dust includes resuspension of loose surface material. | `AUTHORITATIVE` | `SRC-ENV-EPA-AP42-PAVED` | Emission-factor equations are not rendering presets. |
| `CLM-ENV-019` | Unpaved-road dust involves wheel action and vehicle-wake turbulence. | `AUTHORITATIVE` | `SRC-ENV-EPA-AP42-UNPAVED` | Particle size, soil, moisture, traffic, and wind remain event-specific. |
| `CLM-ENV-020` | USDA soil texture class uses sand, silt, and clay proportions. | `AUTHORITATIVE` | `SRC-ENV-USDA-SOIL-TEXTURE`, `SRC-ENV-USDA-SOIL-TAXONOMY` | Soil behaviour also depends on structure, mineralogy, organic matter, density, and moisture. |
| `CLM-ENV-021` | DEM, DTM, and DSM semantics must be verified before using elevation data as terrain. | `AUTHORITATIVE` | `SRC-ENV-USGS-DEM`, `SRC-ENV-COPERNICUS-DEM` | Product-specific definitions, datums, accuracy, and processing control meaning. |
| `CLM-ENV-022` | WMO cloud description uses genera, species, varieties, supplementary features, and accessory clouds. | `AUTHORITATIVE` | `SRC-ENV-WMO-CLOUD-ATLAS` | Procedural clouds should not claim formal classification without morphological evidence. |
| `CLM-ENV-023` | Fog is a near-surface suspension of water droplets or ice crystals that reduces visibility. | `AUTHORITATIVE` | `SRC-ENV-NOAA-FOG`, `SRC-ENV-WMO-CLOUD-ATLAS` | Fog type and structure remain necessary for scene modelling. |
| `CLM-ENV-024` | Marshall-Palmer is a canonical rain drop-size distribution, not a universal event preset. | `PRIMARY` | `SRC-ENV-MARSHALL-PALMER-1948` | Rain regime, shutter, depth, lighting, and wind remain separate. |
| `CLM-ENV-025` | Snow albedo depends on effective grain size and illumination/state, not only a white diffuse colour. | `PRIMARY` | `SRC-ENV-WISCOMBE-WARREN-1980` | Initial Blender cards remain an approximation, not a spectral snow solver. |
| `CLM-ENV-026` | Finite built structures and vegetation provide parallax and reflection bands that an infinite World cannot. | `PRIMARY` + `VA-RULE` | `SRC-ENV-DEBEVEC-1998` | Geometry complexity and LOD depend on shot/reflection requirements. |
| `CLM-ENV-027` | Exposure, white balance, tone mapping, and flare are camera/display operations and must remain separate from scene energy ownership. | `BLENDER-DOC` + `VA-RULE` | `SRC-ENV-BLENDER-NODES-5.0`, `SRC-ENV-BLENDER-SKY-5.0` | Creative grading is allowed when separately labelled. |
| `CLM-ENV-028` | A visible emitter and a separate light can double count one physical source. | `VA-RULE` | `SRC-ENV-BLENDER-NODES-5.0` | Contribution passes are required; no universal split is prescribed. |
| `CLM-ENV-029` | Environment qualification must include motion because HDRI defects, LOD, procedural swimming, volume stepping, and reflection discontinuities can be invisible in one still. | `VA-RULE` | Domain synthesis | Requires retained motion evidence before production qualification. |
| `CLM-ENV-030` | Material parameters should not be retuned to compensate for unresolved environment bandwidth, horizon, exposure, or sun ownership. | `VA-RULE` | Domain synthesis | The correction owner must be recorded before promotion. |
| `CLM-ENV-031` | Blender Volume Coefficients accepts per-distance absorption and scattering coefficients, making measured or visibility-derived inputs preferable to an unexplained density scalar. | `BLENDER-DOC` + `VA-INFERENCE` | `SRC-ENV-BLENDER-VOLUME-COEFFICIENTS-5.0` | A visibility relation does not recover particle composition, vertical structure, or full spectral scattering. |
| `CLM-ENV-032` | Lensfun calibrations may separately depend on focal length, aperture, and focus distance and can include polynomial distortion, TCA, and vignetting models. | `UPSTREAM-DOC` | `SRC-ENV-LENSFUN-MANUAL`, `SRC-ENV-LENSFUN-CALIBRATION` | Blender's single-factor Lens Distortion node is not an equivalent representation. |
| `CLM-ENV-033` | A perspective/thin-lens camera does not reproduce the radiometry and aberrations of a traced multi-element lens prescription. | `PRIMARY-IMPLEMENTATION` | `SRC-ENV-PBRT-REALISTIC-CAMERA` | Use calibrated image-space models or a traced optical system when those effects matter. |
| `CLM-ENV-034` | Blender's Cycles UV pass encodes U and V in red and green and stores a constant one in blue; a generated Map UV field must preserve that validity convention. | `BLENDER-DOC` + `OBS-INSTRUMENT` | `SRC-ENV-BLENDER-RENDER-PASSES-5.0`, `SRC-ENV-BLENDER-MAP-UV-5.0` | Confirmed in Blender 5.2 by an initial black result with blue zero and a successful remap after setting blue to one. |
| `CLM-ENV-035` | A camera-specific Lensfun profile can be reproduced by channel coordinate maps and a scene-linear vignetting map without misusing Blender's single-factor Lens Distortion node. | `PRIMARY-IMPLEMENTATION` + `OBS-INSTRUMENT` | `SRC-ENV-LENSFUN-SOURCE-698A39`, `SRC-ENV-LENSFUN-CALIBRATION` | Verified for the pinned Canon 85 mm profile and current centred 16:9 crop only; PSF, flare, sensor, and camera colour remain outside this stage. |
| `CLM-ENV-036` | Compositor input images carry their own domains, so a low-resolution coordinate map can collapse a downstream Map UV operation to that smaller domain unless it is explicitly adapted to Render Size. | `BLENDER-DOC` + `OBS-INSTRUMENT` | `SRC-ENV-BLENDER-COMPOSITOR-SYSTEM-5.0`, `SRC-ENV-BLENDER-MAP-UV-5.0` | Observed as a 960 x 540 inset in a black 3840 x 2160 canvas; corrected with explicit Render Size scaling and retested at full resolution. |

## Conversion rule

When a claim is used to drive executable parameters or a production decision:

1. identify the exact claim ID;
2. read the registered source and conditions;
3. record whether the parameter is measured, derived, calibrated, an artist
   default, an implementation default, or unresolved;
4. link a controlled experiment where practical;
5. preserve contradictions rather than averaging them away;
6. promote to a machine-readable `CLM-*` record only when its evidence links and
   scope are sufficiently specific.
