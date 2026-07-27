# Environment validation and experiment backlog

## 1. Qualification philosophy

Environment validation is role-specific. A scene can be accepted for artistic
presentation while rejected for material measurement, geometry diagnosis, or
weather research.

Every experiment records:

- Blender version and engine;
- source environment/profile revision;
- world/direct/volume ownership;
- camera, exposure, white balance, and display transform;
- scene scale and coordinate system;
- random seed;
- controlled variable;
- evidence outputs;
- quantitative and visual acceptance criteria;
- known confounders;
- result status.

No visual judgement becomes `VA-VALIDATED` without retained evidence.

## 2. Canonical diagnostic kit

### 2.1 Objects

- chrome sphere;
- 18% diffuse-grey sphere and card;
- white diffuse card below clipping;
- black glossy curved panel;
- rough dielectric spheres at several roughness values;
- solid metallic panel;
- clearcoat paint panel;
- clear glass slab and curved windshield proxy;
- tyre-rubber cylinder;
- metric road tile;
- black/white visibility targets at known distances.

### 2.2 Camera views

- orthographic top/side for scale;
- low automotive three-quarter;
- grazing road view;
- long-lens horizon view;
- interior-through-windshield;
- moving vehicle and moving camera;
- fixed exposure bracket.

### 2.3 Contribution passes

- world only;
- direct emitters only;
- local volume only;
- full combined;
- no-volume baseline;
- surface dry/wet/dust masks;
- geometric/custom normals;
- depth and Mist Pass;
- reflection/reference spheres;
- motion vectors when available.

## 3. Environment profile acceptance matrix

| Use | Minimum evidence |
| --- | --- |
| material look development | stable radiance structure, no accidental sun double count, chrome/grey/black/glass diagnostics |
| geometry/Class-A diagnosis | broad controlled reflection bands, finite local geometry or studio cards, motion/orbit test |
| exterior hero render | horizon, ground, local parallax, weather/surface state, camera pipeline, rights record |
| weather test | dry baseline, state progression, wind/motion, surface response, volume/reflection checks |
| HDRI qualification | metadata, clipping test, orientation, lower hemisphere, role-specific diagnostics |
| real-time/EEVEE profile | explicit divergence from Cycles, reflection/probe/volume limitations, performance capture |

## 4. Experiment backlog

### EXP-ENV-SKY-001 — Sky-family comparison

**Question:** How do Preetham, Hosek/Wilkie, and Nishita differ over an automotive
diagnostic rig at matched sun direction and camera exposure?

**Controlled variables:** camera, geometry, direct-light policy, colour
management, ground, and render settings.

**Outputs:** zenith/horizon luminance samples, chrome/grey/paint/glass renders,
world panorama, turntable.

**Acceptance:** differences are documented without declaring one universally
more physical; model controls remain correctly labelled.

---

### EXP-ENV-SUN-002 — Direct-sun ownership

**Question:** What energy and highlight errors arise from analytic/HDRI sun plus
a separate Sun light?

Cases:

1. world sun only;
2. Sun light only with neutral world;
3. both unmodified;
4. deliberately separated/calibrated approximation.

Inspect shadow direction, penumbra, chrome peak, paint glint, road irradiance,
and exposure.

---

### EXP-ENV-NISHITA-003 — Parameter sensitivity

Vary one of Air, Dust, Ozone, Altitude, and sun elevation at a time. Record sky
panoramas, horizon/zenith ratios, direct-beam appearance, and automotive
reflection changes.

**Boundary:** this does not map controls to real atmospheric units.

---

### EXP-ENV-VOL-004 — Bounded extinction calibration

Construct a metric volume with black/white targets at several known distances.
Test neutral extinction against `T(d) = exp(-sigma_t d)` where the node model
allows.

Compare:

- absorption only;
- scattering only;
- combined;
- several anisotropy values;
- Cycles and EEVEE.

---

### EXP-ENV-VOL-005 — World versus bounded volume

Compare a World volume and a bounded atmosphere volume for the same hero-car
scene. Inspect camera view, paint reflections, windshield transmission,
headlights, horizon, and sampling.

Expected outcome is an engine/version-specific limitation record, not a claim
that one setup always looks better.

---

### EXP-ENV-HDRI-006 — Solar clipping and map bandwidth

For several legally usable HDRIs:

- inspect maximum/channel plateaus;
- render exposure brackets;
- measure apparent solar-disc width in pixels/degrees where metadata permits;
- compare HDRI-only shadows against extracted Sun light;
- inspect clearcoat and chrome.

Classify each map by role: lighting, reflection, background, or reference.

---

### EXP-ENV-HDRI-007 — Parallax failure

Reconstruct one nearby wall/tree/building from an HDRI as simple geometry.
Translate camera and car around the capture point. Compare world-only versus
local reconstruction in paint, glass, and visible background.

---

### EXP-ENV-ROAD-008 — Road texture scale bands

Build one metric asphalt tile with independent microtexture, macrotexture,
megatexture, and profile controls.

Disable each band separately. Inspect grazing light, tyre contact, lower-body
reflections, silhouette, and moving camera.

---

### EXP-ENV-ROAD-009 — Dry-to-wet progression

Use one substrate and fixed exposure. Progress through dry, damp, wet film, and
ponded states.

Inspect:

- substrate darkening;
- water-film Fresnel;
- cavity filling;
- low-point accumulation;
- reflection sharpness;
- tyre contact/spray eligibility.

Reject if the sequence can be reproduced only by lowering one roughness value.

---

### EXP-ENV-ROAD-010 — Drainage-driven puddles

Use a known height field with crown, rut, kerb, and drain. Compare arbitrary
noise puddles with basin/flow-derived accumulation.

Retain topographic, flow, and final water masks.

---

### EXP-ENV-DUST-011 — Deposited versus suspended dust

Create separate systems for surface deposit and airborne plume. Trigger
resuspension from a known road reservoir under a moving tyre/wake proxy.

Inspect mass-source consistency, settling, crosswind, vehicle contamination,
and no-emission wet case.

---

### EXP-ENV-FOG-012 — Vertical structure

Compare equal integrated extinction in:

- shallow ground fog;
- uniform tall haze;
- elevated layer;
- spatial fog bank.

Use known-distance targets, terrain silhouettes, headlights, car reflections,
and motion.

---

### EXP-ENV-RAIN-013 — Rain shutter and depth

Render world-space drops at multiple shutter times and camera velocities.
Validate streak length/orientation against drop and camera relative motion.

Include an image-space streak approximation as a labelled comparator.

---

### EXP-ENV-WATER-014 — Windshield acceleration response

Use a curved windshield proxy and controlled droplet field. Cases:

- stationary;
- acceleration;
- braking;
- left/right cornering;
- crosswind;
- wiper sweep.

Retain tangent-force and velocity diagnostics. No real-car fidelity claim until
compared with suitable reference.

---

### EXP-ENV-CLOUD-015 — Overcast reflection structure

Compare:

- uniform grey World;
- low-frequency cloud luminance;
- structured cloud field with matched mean exposure.

Inspect broad body curvature, windshield, black trim, chrome, and shadow
readability.

---

### EXP-ENV-SNOW-016 — Grain/roughness proxy study

Build a limited snow surface proxy varying effective grain/structure and
illumination direction. Inspect albedo clipping, shadow colour, grazing
sparkle, and contamination.

This is not a full spectral snow model.

---

### EXP-ENV-CAMERA-017 — Exposure versus environment compensation

Hold scene energy fixed and vary camera exposure; then hold camera fixed and
vary world strength. Show why these are not interchangeable once clipping,
noise, bloom, volumes, and local lights are considered.

---

### EXP-ENV-ENGINE-018 — Cycles/EEVEE environment divergence

Use the same scene graph where possible. Compare:

- sky and direct light;
- bounded fog;
- paint reflections;
- windshield transmission;
- volumetric headlight beams;
- probes/reflections;
- wet road;
- rain particles;
- performance and noise.

No forced visual match is required. Record incompatibilities.

---

### EXP-ENV-F40-019 — F40 environment robustness matrix

After the F40 export is registered and diagnosed, render it in five controlled
profiles:

1. clear dry midday;
2. hazy dry low sun;
3. bright overcast damp;
4. active rain/wet road;
5. post-rain drying low sun.

Materials may not be retuned per environment without creating a recorded
variant. The objective is to expose glass, paint, grille, tyre, carbon, and
normal-field fragility.

---

### EXP-ENV-MOTION-020 — Environment temporal stability

Drive camera and/or vehicle through road, terrain, local reflectors, atmosphere,
and weather. Inspect:

- procedural swimming;
- texture repetition;
- LOD popping;
- reflection discontinuity;
- volume stepping;
- particle attachment;
- horizon instability;
- shadow mismatch.

## 5. Quantitative aids

Quantitative measurement does not need to imply complete physical calibration.
Useful aids include:

- image luminance samples in scene-linear output;
- peak/percentile values;
- target contrast versus distance;
- shadow angle and penumbra width;
- sun-disc angular size;
- map histogram and clipped-pixel counts;
- world-space feature-size checks;
- performance time/memory;
- deterministic image hashes only where floating/render determinism permits;
- geometry and parameter manifests.

## 6. Fresh-file regression

An environment system is not production-qualified until either:

- a deterministic builder reconstructs it in a fresh Blender `5.0.1` file; or
- a minimal `.blend` asset plus manifest can be linked/imported reproducibly.

The regression records:

- Blender build/version;
- enabled add-ons;
- external assets and checksums;
- generated datablocks;
- random seeds;
- render command;
- expected evidence paths;
- known nondeterminism.

## 7. Stop conditions

Stop and investigate when:

- a change intended for atmosphere alters material parameters;
- HDRI gain is used to fix direct-sun clipping;
- exposure changes between experiment variants without being the tested variable;
- water appears without a source/accumulation state;
- procedural scale is undocumented;
- EEVEE and Cycles outputs are silently mixed;
- compositor effects are described as scene transport;
- a source cannot be licensed or reproduced;
- a visually impressive result cannot be decomposed into owned contributions.