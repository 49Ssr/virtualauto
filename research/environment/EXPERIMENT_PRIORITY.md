# Environment experiment priority

The 20-experiment backlog is retained, but it is not a 20-item active queue.
Priority is based on current F40 usefulness, Blender implementation readiness, and
information gained per unit of work.

## P0 — execute next

### 1. F40 glass corridor classification

Derived from `EXP-ENV-F40-019`, narrowed to the Level 0 windshield problem.

Deliverables:

- executed Blender `5.0.1` corridor;
- immutable source/test windshield inventory;
- opaque/specular/minimal-glass sequence;
- custom/geometric/recalculated normal comparison;
- left/right band and camera/environment motion matrix;
- supported classification and reversible next action.

This is the only environment experiment that should block current F40 glass work.

### 2. Camera and colour lock

Subset of `EXP-ENV-CAMERA-017`.

Deliverables:

- exact view transform, look, exposure, white-balance state, lens, sensor, and
  camera transform;
- one scene-linear capture and one display-referred reference;
- proof that comparison variants do not silently change the camera pipeline.

### 3. Reflection-band continuity on known-good objects

A practical precursor to material conclusions.

Deliverables:

- chrome sphere;
- grey sphere/card;
- black-gloss panel or sphere;
- glass proxy;
- fixed camera plus environment movement;
- confirmation that the rig itself does not generate triangular or discontinuous
  reflections on clean geometry.

## P1 — execute after the windshield is classified

### 4. Direct-sun ownership

`EXP-ENV-SUN-002`.

Use only when the Level 1 dry exterior rig introduces an analytic sky or HDRI plus
separate Sun light.

### 5. HDRI clipping and reflection bandwidth

`EXP-ENV-HDRI-006`.

Qualify a small number of legally usable maps. Do not build a giant HDRI library
before one map has passed the automotive rig.

### 6. Road scale-band visibility

`EXP-ENV-ROAD-008`.

Implement only the bands visible at the target camera distance. The experiment
should determine which features require geometry/displacement and which can remain
normal/roughness detail.

### 7. F40 dry robustness matrix

Dry subset of `EXP-ENV-F40-019`:

- neutral diagnostic corridor;
- controlled studio-like bands;
- clear dry outdoor;
- structured overcast.

Do not include active rain yet.

## P2 — shot-dependent production research

- `EXP-ENV-VOL-004` bounded extinction calibration;
- `EXP-ENV-HDRI-007` local parallax reconstruction;
- `EXP-ENV-ROAD-009` dry-to-wet progression;
- `EXP-ENV-ROAD-010` drainage-driven puddles;
- `EXP-ENV-FOG-012` vertical fog structure;
- `EXP-ENV-ENGINE-018` Cycles/EEVEE divergence;
- `EXP-ENV-MOTION-020` temporal stability.

Execute only when a named scene or system needs the result.

## P3 — parked research

- full sky-family comparison beyond the active sky choice;
- broad Nishita parameter sweep;
- world-volume comparison unless a world-volume proposal exists;
- deposited/suspended dust coupling;
- rain shutter/depth system;
- windshield acceleration and wiper simulation;
- cloud-structure study;
- snow-grain proxy.

These remain valid research questions. They are parked because they do not improve
the current F40 glass diagnosis enough to justify their cost.

## Kill criteria

Stop or narrow an experiment when:

- the result will not change a Blender build decision;
- the test requires an unimplemented system larger than the question;
- a simpler diagnostic already isolates the variable;
- the required reference cannot be licensed, measured, or reproduced;
- the test would force per-environment material retuning;
- runtime cost prevents the repeated motion/orbit tests needed for automotive
  validation;
- results cannot be retained without exposing private source assets.

## Promotion rule

A broad research experiment is promoted into the active queue only when it has:

1. a named project or reusable asset consumer;
2. a Blender `5.0.1` implementation path;
3. one controlled variable;
4. a retained evidence plan;
5. an acceptance or rejection decision that changes future work.