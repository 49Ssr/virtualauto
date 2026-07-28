# Environment source register

This register identifies the evidence class and intended use of sources cited by
the environment domain. A source being listed does not mean every statement in
it has been independently reproduced by VirtualAuto.

## Blender documentation

### SRC-ENV-BLENDER-SKY-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — Sky Texture Node](https://docs.blender.org/manual/en/5.0/render/shader_nodes/textures/sky.html)
- Use: authoritative user-facing Sky Texture families, inputs, outputs, and
  properties for Blender 5.0.
- Key scope: Preetham, Hosek/Wilkie, Nishita, sun, turbidity, ground albedo,
  altitude, air, dust, ozone.
- Limitation: documentation labels and examples do not establish a physical-unit
  mapping for every control.

### SRC-ENV-BLENDER-VOLUME-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — Volumes](https://docs.blender.org/manual/en/5.0/render/materials/components/volume.html)
- Use: volume components, density interpretation, manifold-volume requirements,
  world-volume warning, and multiple-scattering limitations.
- Limitation: renderer implementation and defaults must still be checked for the
  exact Blender build.

### SRC-ENV-BLENDER-WORLD-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — World Environment](https://docs.blender.org/manual/en/5.0/render/lights/world.html)
- Use: World surface/volume ownership and environment lighting context.

### SRC-ENV-BLENDER-ENV-TEXTURE-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — Environment Texture Node](https://docs.blender.org/manual/en/5.0/render/shader_nodes/textures/environment.html)
- Use: projection-aware environment-map sampling in shader World context.

### SRC-ENV-BLENDER-EEVEE-VOLUME-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — EEVEE Volumes](https://docs.blender.org/manual/en/5.0/render/eevee/render_settings/volumes.html)
- Use: resolution, stepping, depth bounds, and real-time volume controls.

### SRC-ENV-BLENDER-EEVEE-LIMITS-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — EEVEE Limitations](https://docs.blender.org/manual/en/5.0/render/eevee/limitations/limitations.html)
- Use: engine-specific reflection, refraction, volume, and scattering boundaries.

### SRC-ENV-BLENDER-MIST-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — Mist Pass](https://docs.blender.org/manual/en/5.0/render/layers/passes.html)
- Use: classification of Mist as a depth-derived render pass rather than a full
  participating-media solution.

### SRC-ENV-BLENDER-NODES-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — Shader Nodes Introduction](https://docs.blender.org/manual/en/5.0/render/shader_nodes/introduction.html)
- Use: surface, volume, emission, and background shader ownership.

### SRC-ENV-BLENDER-VOLUME-COEFFICIENTS-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — Volume Coefficients](https://docs.blender.org/manual/en/5.0/render/shader_nodes/shader/volume_coefficients.html)
- Use: per-distance absorption, scattering, and emission coefficients plus
  supported scattering phase functions.
- Limitation: the node accepts parameters; it does not establish that a chosen
  atmosphere profile was measured or fitted.

### SRC-ENV-BLENDER-RENDER-PASSES-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — Render Passes](https://docs.blender.org/manual/en/5.0/render/layers/passes.html)
- Use: Cycles UV-pass channel convention: U in red, V in green, and a constant
  value of one in blue.
- Limitation: this documents the render-pass representation; a generated
  compositor coordinate map still requires its own operation-domain and
  resampling tests.

### SRC-ENV-BLENDER-MAP-UV-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — Map UV Node](https://docs.blender.org/manual/en/5.0/compositing/types/transform/map_uv.html)
- Use: compositor texture remapping from a UV coordinate pass and supported
  filter behaviour.
- Limitation: Map UV is documented primarily for applying textures to rendered
  UV-mapped objects; VirtualAuto's full-frame lens use is a tested repurposing,
  not an advertised camera-calibration feature.

### SRC-ENV-BLENDER-COMPOSITOR-SYSTEM-5.0

- Class: `BLENDER-DOC`
- Source: [Blender 5.0 Manual — Compositor System](https://docs.blender.org/manual/en/5.0/compositing/compositor_system.html)
- Use: image domains, operation domains, input-node identity domains, output
  render-size domains, and the rule that many operations inherit one designated
  input's domain.
- Limitation: exact domain ownership of a repurposed multi-node calibration
  graph still requires execution at every qualified delivery resolution.

## Camera and lens calibration references

### SRC-ENV-CANON-5D4

- Class: `MANUFACTURER-DOC`
- Source: [Canon EOS 5D Mark IV](https://www.usa.canon.com/shop/p/eos-5d-mark-iv)
- Use: full-frame sensor format, 30.4 MP capture dimensions, pixel-pitch
  derivation, and confirmation that an optical low-pass filter is installed.
- Limitation: no OLPF transfer function, CFA spectral sensitivity, demosaic,
  sharpening, noise, or complete camera-response function is disclosed.

### SRC-ENV-CANON-EF85-14L

- Class: `MANUFACTURER-DOC`
- Source: [Canon EF 85mm f/1.4L IS USM](https://www.usa.canon.com/shop/p/ef-85mm-f-1-4l-is-usm)
- Use: lens identity, 14-element/10-group construction, nine-blade aperture,
  and Canon's ASC flare/ghost-suppression claim.
- Limitation: product specifications do not disclose the optical prescription,
  field-dependent PSF, pupil shape at f/8, or measured flare kernel.

### SRC-ENV-CANON-MTF

- Class: `MANUFACTURER-DOC`
- Source: [Canon â€” Reading and Understanding Lens MTF Charts](https://www.usa.canon.com/learning/training-articles/training-articles-list/reading-and-understanding-lens-mtf-charts)
- Use: Canon's statement that current lens MTF charts are measured wide open.
- Limitation: the chart cannot be converted into the selected lens's f/8 PSF.

### SRC-ENV-AIRY-DISK

- Class: `AUTHORITATIVE-TECHNICAL`
- Source: [Edmund Optics â€” The Airy Disk](https://www.edmundoptics.com/knowledge-center/application-notes/imaging/limitations-on-resolution-and-contrast-the-airy-disk/)
- Use: ideal circular-aperture diffraction relation and first-zero diameter.
- Limitation: the ideal Airy model omits real pupil geometry, aberrations,
  coatings, focus error, field position, sensor filtering, and processing.

### SRC-ENV-BLENDER-CONVOLVE-5.2

- Class: `BLENDER-DOC`
- Source: [Blender 5.2 Python API â€” Compositor Convolve Node](https://docs.blender.org/api/5.2/bpy.types.CompositorNodeConvolve.html)
- Use: confirmation that Blender exposes a compositor image-convolution node;
  exact socket behaviour was separately probed and impulse-tested in 5.2.0.
- Limitation: node availability does not validate the supplied optical kernel.

### SRC-ENV-LENSFUN-MANUAL

- Class: `UPSTREAM-DOC`
- Source: [Lensfun manual](https://lensfun.github.io/manual/latest/)
- Use: open calibration database and reversible correction/simulation support
  for distortion, transverse chromatic aberration, and vignetting.
- Limitation: coverage and calibration completeness vary by lens.

### SRC-ENV-LENSFUN-CALIBRATION

- Class: `UPSTREAM-DOC`
- Source: [Lensfun calibration data format](https://lensfun.github.io/manual/v0.3.1/elem_calibration.html)
- Audited database commit: `698a39eea69be00f4f25b6da6c1ad34b1f162b50`
- Use: exact distortion, TCA, and aperture/distance-dependent vignetting model
  fields used by Lensfun profiles.
- Limitation: coefficients must be evaluated with the matching Lensfun model;
  they are not Blender Lens Distortion values.

### SRC-ENV-LENSFUN-SOURCE-698A39

- Class: `PRIMARY-IMPLEMENTATION`
- Source: [Lensfun source at pinned commit](https://github.com/lensfun/lensfun/tree/698a39eea69be00f4f25b6da6c1ad34b1f162b50)
- Use: coordinate normalization, focal-preserving PTLens coefficient rescaling,
  reverse PTLens solving, poly3 TCA rescaling and reverse solving, PA
  vignetting coefficient rescaling/evaluation, callback order, and
  aperture/distance interpolation behaviour used by the 85 mm compositor
  implementation.
- Limitation: VirtualAuto reproduced the relevant equations in generated maps;
  it did not link the Lensfun binary into Blender. Scope is pinned to the
  audited source revision and current supported model subset.

### SRC-ENV-PBRT-REALISTIC-CAMERA

- Class: `PRIMARY-IMPLEMENTATION`
- Source: [PBRT — Realistic Cameras](https://www.pbr-book.org/3ed-2018/Camera_Models/Realistic_Cameras)
- Use: reference implementation for tracing rays through multi-element lens
  prescriptions and the resulting radiometric and aberration effects.
- Limitation: this is not Blender's native camera model.

## Daylight and atmospheric rendering research

### SRC-ENV-PREETHAM-1999

- Class: `PRIMARY`
- Citation: A. J. Preetham, Peter Shirley, and Brian Smits, “A Practical Analytic
  Model for Daylight,” SIGGRAPH 1999.
- DOI: [10.1145/311535.311545](https://doi.org/10.1145/311535.311545)
- Use: historical and mathematical basis for Blender's Preetham sky family.
- Limitation: later models document weaknesses at sunset and high turbidity.

### SRC-ENV-HOSEK-WILKIE-2012

- Class: `PRIMARY`
- Citation: Lukas Hosek and Alexander Wilkie, “An Analytic Model for Full
  Spectral Sky-Dome Radiance,” ACM Transactions on Graphics 31(4), 2012.
- Project page: [Charles University Sky-Dome Research](https://cgg.mff.cuni.cz/projects/SkylightModelling/)
- DOI: [10.1145/2185520.2185591](https://doi.org/10.1145/2185520.2185591)
- Use: basis for Hosek/Wilkie family, improved high-turbidity/sunset fit, ground
  albedo, and spectral treatment.

### SRC-ENV-BRUNETON-NEYRET-2008

- Class: `PRIMARY`
- Citation: Eric Bruneton and Fabrice Neyret, “Precomputed Atmospheric
  Scattering,” Computer Graphics Forum 27(4), 2008.
- Project page: [INRIA atmospheric scattering](https://ebruneton.github.io/precomputed_atmospheric_scattering/)
- Use: physically structured reference for Rayleigh/Mie multiple scattering,
  aerial perspective, and ground-to-space atmosphere.
- Limitation: not a statement that Blender Sky Texture implements the same model.

### SRC-ENV-BRUNETON-2016

- Class: `PRIMARY`
- Citation: Eric Bruneton, “A Qualitative and Quantitative Evaluation of 8 Clear
  Sky Models,” IEEE Transactions on Visualization and Computer Graphics, 2017
  prepublication/evaluation work.
- Use: model-comparison methodology and warning against treating all sky models
  as equivalent.

### SRC-ENV-BODHAINE-1999

- Class: `PRIMARY`
- Citation: B. A. Bodhaine et al., “On Rayleigh Optical Depth Calculations,”
  Journal of Atmospheric and Oceanic Technology 16, 1999.
- DOI: [10.1175/1520-0426(1999)016<1854:ORODC>2.0.CO;2](https://doi.org/10.1175/1520-0426%281999%29016%3C1854%3AORODC%3E2.0.CO%3B2)
- Use: first-principles Rayleigh optical-depth considerations.

### SRC-ENV-HENYEY-GREENSTEIN-1941

- Class: `PRIMARY`
- Citation: Louis G. Henyey and Jesse L. Greenstein, “Diffuse Radiation in the
  Galaxy,” Astrophysical Journal 93, 1941.
- Use: provenance for the common one-parameter anisotropic phase-function
  approximation.
- Limitation: the phase function is a mathematical approximation, not a particle
  classifier.

## Aerosol, visibility, and ozone references

### SRC-ENV-NOAA-AOD

- Class: `AUTHORITATIVE`
- Source: [NOAA SURFRAD — Aerosol Optical Depth](https://gml.noaa.gov/grad/surfrad/aod/)
- Use: definition and interpretation of aerosol optical depth as direct-beam
  extinction through an atmospheric column.

### SRC-ENV-NOAA-STAR-AEROSOL

- Class: `AUTHORITATIVE`
- Source: [NOAA STAR Aerosol Optical Depth](https://www.star.nesdis.noaa.gov/smcd/spb/aq/AerosolWatch/)
- Use: aerosol scattering/absorption and aerosol-class examples.

### SRC-ENV-NASA-AEROSOLS

- Class: `AUTHORITATIVE`
- Source: [NASA Earth Observatory — Aerosols](https://earthobservatory.nasa.gov/features/Aerosols)
- Use: composition-dependent aerosol scattering/absorption and climate context.

### SRC-ENV-BERGSTROM-2007

- Class: `PRIMARY`
- Citation: Robert W. Bergstrom et al., “Spectral Absorption Properties of
  Atmospheric Aerosols,” Atmospheric Chemistry and Physics 7, 2007.
- Use: spectral aerosol absorption and Ångström absorption-exponent limitations.

### SRC-ENV-NASA-OZONE

- Class: `AUTHORITATIVE`
- Source: [NASA Ozone Watch — Facts](https://ozonewatch.gsfc.nasa.gov/facts/SH.html)
- Use: broad vertical location and role of stratospheric ozone.

## Image-based lighting and HDR capture

### SRC-ENV-DEBEVEC-1998

- Class: `PRIMARY`
- Citation: Paul Debevec, “Rendering Synthetic Objects into Real Scenes:
  Bridging Traditional and Image-Based Graphics with Global Illumination and
  High Dynamic Range Photography,” SIGGRAPH 1998.
- Project page: [Image-Based Lighting](https://www.pauldebevec.com/Research/IBL/)
- DOI: [10.1145/280814.280864](https://doi.org/10.1145/280814.280864)
- Use: measured HDR scene radiance, distant/local scene decomposition, and IBL
  provenance.

### SRC-ENV-DEBEVEC-MALIK-1997

- Class: `PRIMARY`
- Citation: Paul Debevec and Jitendra Malik, “Recovering High Dynamic Range
  Radiance Maps from Photographs,” SIGGRAPH 1997.
- Use: foundational multi-exposure HDR radiance recovery.

### SRC-ENV-POLYHAVEN

- Class: `AUTHORITATIVE-UPSTREAM`
- Source: [Poly Haven licence](https://polyhaven.com/license)
- Use: example of a CC0 asset provider and capture metadata source.
- Limitation: licence and metadata do not guarantee scene suitability, sun
  preservation, calibration, or absence of capture defects.

## Pavement and road references

### SRC-ENV-FHWA-TEXTURE

- Class: `AUTHORITATIVE`
- Source: [FHWA Technical Advisory T 5040.36 — Surface Texture for Asphalt and
  Concrete Pavements](https://www.fhwa.dot.gov/pavement/t504036.cfm)
- Use: microtexture, macrotexture, megatexture, and pavement-roughness scale
  bands; relation to friction and drainage.

### SRC-ENV-FHWA-SAFETY

- Class: `AUTHORITATIVE`
- Source: [FHWA Pavement Friction Management](https://highways.dot.gov/safety/rwd/keep-vehicles-road/pavement-friction)
- Use: aggregate microtexture, macrotexture, wet-weather friction, and drainage
  context.

### SRC-ENV-ASTM-E1845

- Class: `STANDARD-REFERENCE`
- Source: ASTM E1845, Standard Practice for Calculating Pavement Macrotexture
  Mean Profile Depth.
- Use: provenance for pavement macrotexture measurement terminology.
- Limitation: full standard text may require licensed access; do not reproduce it.

### SRC-ENV-WET-ASPHALT-OPTICS

- Class: `PRIMARY`
- Citation family: angular/spectral and polarized reflectance studies of dry,
  wet, icy, and snowy asphalt surfaces.
- Use: evidence that wet pavement response changes by angle, material, water
  state, and polarization rather than one universal roughness scalar.
- Status: individual papers must be registered before numerical values are used.

## Soil, terrain, and dust references

### SRC-ENV-USDA-SOIL-TEXTURE

- Class: `AUTHORITATIVE`
- Source: [USDA NRCS Soil Texture Calculator and guide](https://www.nrcs.usda.gov/resources/education-and-teaching-materials/soil-texture-calculator)
- Use: sand/silt/clay texture-class terminology.

### SRC-ENV-USDA-SOIL-TAXONOMY

- Class: `AUTHORITATIVE`
- Source: [USDA NRCS Soil Taxonomy](https://www.nrcs.usda.gov/resources/guides-and-instructions/soil-taxonomy)
- Use: standardized soil classification and warning against treating `dirt` as
  one material.

### SRC-ENV-USGS-DEM

- Class: `AUTHORITATIVE`
- Source: [USGS 3D Elevation Program](https://www.usgs.gov/3d-elevation-program)
- Use: DEM/terrain-data provenance, resolution, and bare-earth context.

### SRC-ENV-COPERNICUS-DEM

- Class: `AUTHORITATIVE-UPSTREAM`
- Source: [Copernicus DEM Product Handbook](https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM)
- Use: global elevation-product metadata and known dataset limitations.

### SRC-ENV-EPA-AP42-PAVED

- Class: `AUTHORITATIVE`
- Source: [US EPA AP-42, Section 13.2.1 — Paved Roads](https://www.epa.gov/air-emissions-factors-and-quantification/ap-42-fifth-edition-volume-i-chapter-13-miscellaneous-sources)
- Use: paved-road fugitive dust and resuspension context.

### SRC-ENV-EPA-AP42-UNPAVED

- Class: `AUTHORITATIVE`
- Source: [US EPA AP-42, Section 13.2.2 — Unpaved Roads](https://www.epa.gov/air-emissions-factors-and-quantification/ap-42-fifth-edition-volume-i-chapter-13-miscellaneous-sources)
- Use: tyre pulverization/lifting and vehicle-wake dust mechanisms.
- Limitation: emissions-factor methodology is not a rendering-particle preset.

## Weather, cloud, rain, and snow references

### SRC-ENV-WMO-CLOUD-ATLAS

- Class: `AUTHORITATIVE`
- Source: [WMO International Cloud Atlas](https://cloudatlas.wmo.int/)
- Use: cloud genera, species, varieties, supplementary features, accessory
  clouds, and official descriptive vocabulary.

### SRC-ENV-NOAA-FOG

- Class: `AUTHORITATIVE`
- Source: [NOAA/NWS Glossary — Fog](https://forecast.weather.gov/glossary.php?word=fog)
- Use: fog definition and near-surface visibility context.

### SRC-ENV-MARSHALL-PALMER-1948

- Class: `PRIMARY`
- Citation: J. S. Marshall and W. McK. Palmer, “The Distribution of Raindrops
  with Size,” Journal of Meteorology 5, 1948.
- DOI: [10.1175/1520-0469(1948)005<0165:TDORWS>2.0.CO;2](https://doi.org/10.1175/1520-0469%281948%29005%3C0165%3ATDORWS%3E2.0.CO%3B2)
- Use: canonical statistical drop-size-distribution reference.
- Limitation: not a universal distribution for all rain events.

### SRC-ENV-WISCOMBE-WARREN-1980

- Class: `PRIMARY`
- Citation: Warren J. Wiscombe and Stephen G. Warren, “A Model for the Spectral
  Albedo of Snow,” Journal of the Atmospheric Sciences 37, 1980.
- Use: effective snow grain size, illumination, and spectral-albedo dependence.

## Source-use rules

1. Numerical values require the exact source, units, conditions, and uncertainty.
2. A Blender manual parameter description is not automatically a meteorological
   calibration.
3. Government guidance can establish terminology and mechanisms without
   supplying a direct shader mapping.
4. A primary paper can motivate an implementation without proving Blender uses
   the same equations.
5. Secondary tutorials may locate techniques but do not promote claims alone.
6. External images, HDRIs, scans, and datasets require separate rights and asset
   records.
7. Any future source that contradicts this register is recorded in
   [Open questions and contradictions](OPEN_QUESTIONS_AND_CONTRADICTIONS.md), not
   silently reconciled.
