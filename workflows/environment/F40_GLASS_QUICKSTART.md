# F40 glass diagnostic quickstart

This is the first practical environment task for the sourced DriveClub F40 export.
It is intentionally smaller than the full environment research domain.

Status: `P2-buildable`; the repository has not yet executed this rig in Blender
`5.0.1` against the private F40 export.

## Goal

Determine whether the symmetrical windshield triangles are locked to:

- faces/topology;
- imported custom loop normals;
- reconstructed tangents;
- UV or colour/custom attributes;
- overlapping shells/depth;
- the material;
- the reflected environment;
- the render engine.

The goal is not a final beauty render.

## Build the corridor

From a Blender `5.0.1` command line:

```text
blender --background your_f40_workfile.blend --python workflows/environment/build_f40_glass_corridor.py -- --output your_f40_diag.blend
```

To rebuild only the VirtualAuto-owned corridor:

```text
blender --background your_f40_diag.blend --python workflows/environment/build_f40_glass_corridor.py -- --replace-existing --output your_f40_diag.blend
```

The builder:

- requires Blender `5.0.1` exactly;
- does not edit the F40;
- creates `VA_ENV_F40_GLASS_DIAGNOSTIC`;
- creates a neutral World, dry ground, asymmetric reflection bands, a dark
  absorber, diagnostic spheres, an overhead fill, and a 50 mm camera;
- switches the scene to Cycles and records the previous engine, World, and camera
  names as scene custom properties;
- labels its numerical values as deterministic implementation defaults.

The values are not physical calibration and are not a DriveClub reconstruction.

## Place the vehicle

The builder assumes the useful part of the vehicle is near the world origin, with
ground contact near `Z = 0`.

Do not apply scale, merge objects, recalculate normals, or edit the windshield just
to fit the rig. Move the vehicle root or the diagnostic collection first. Source
geometry changes must remain separate transformations.

## Immutable windshield copies

Create linked or full duplicates with explicit names:

```text
F40_WINDSHIELD_SOURCE_IMMUTABLE
F40_WINDSHIELD_TEST_IMPORTED_NORMALS
F40_WINDSHIELD_TEST_RECALCULATED_NORMALS
F40_WINDSHIELD_TEST_GEOMETRIC
```

Do not overwrite the source object. Record whether each duplicate shares or copies
the mesh datablock.

## Material sequence

Run the same camera and environment sequence for each stage.

### Stage A — opaque diffuse

- one Principled BSDF;
- mid-grey Base Color;
- Metallic `0`;
- moderate Roughness;
- no Coat, Transmission, Alpha, Normal, Bump, or texture inputs.

Purpose: reveal topology, overlapping surfaces, material-slot boundaries, and
normal interpolation without glass transport.

### Stage B — opaque specular dielectric

- retain neutral Base Color;
- lower Roughness enough to show broad bands;
- no Transmission;
- no normal or roughness map.

Purpose: test whether the triangular pattern follows reflected direction.

### Stage C — minimal glass

- use a single Glass BSDF or minimal verified Principled transmission setup;
- neutral colour;
- no tint, dirt, normal, bump, alpha, or roughness map;
- isolate outer and inner shells if both exist.

Purpose: determine whether the artefact appears only under reflection/refraction.

### Stage D — one source input at a time

Reintroduce separately:

1. UV layer;
2. colour attribute;
3. normal map;
4. bump;
5. roughness map;
6. tint/absorption;
7. alpha or mask;
8. second shell;
9. complete material.

Never reintroduce two unknown contributors in one step.

## Normal sequence

For each test duplicate, retain screenshots and a machine-readable inventory.

1. imported custom split normals unchanged;
2. geometric face/vertex normals visualized;
3. custom split normal data cleared on a duplicate only;
4. normals recalculated outside;
5. flat shading;
6. smooth shading;
7. any modifier added one at a time.

Weighted Normal is a comparison, not a repair verdict. If it hides the triangles,
record that result without concluding the source normals were wrong.

## Environment sequence

For each material/normal stage:

1. fixed camera, full corridor;
2. fixed camera, hide left bright band;
3. fixed camera, hide right bright band;
4. fixed camera, hide absorber;
5. rotate/move the bright bands while the car remains fixed;
6. orbit the camera while the environment remains fixed;
7. neutral World only;
8. direct/area light only;
9. Cycles baseline;
10. EEVEE comparison only after classification in Cycles.

## Interpretation matrix

| Observation | Strongest lead | Not yet proof of |
| --- | --- | --- |
| patch stays on exact triangles under all lighting | topology/loop data | bad vertex positions |
| patch disappears after clearing custom normals | imported loop normals | correct replacement normals |
| patch rotates with normal map/tangent changes | tangent or UV basis | original game tangent semantics |
| patch appears only with one UV/attribute | exporter stream or material binding | original DriveClub shader behaviour |
| patch changes with camera but not environment movement | view/refraction or overlap | engine bug |
| patch changes with environment bands | small normal/curvature discontinuity | need for more geometry |
| patch disappears when one shell is hidden | overlap/depth or duplicate layer | which shell the game intended |
| Cycles and EEVEE disagree | engine implementation boundary | source asset corruption |

## Required evidence

Retain outside the public repository when it contains the private model:

- exact source and test-file checksums;
- Blender runtime manifest;
- object/mesh/UV/attribute/material inventory;
- screenshots or EXR/PNG diagnostic renders;
- camera and environment transforms;
- material node inventory;
- custom-normal presence and change record;
- result classification and unresolved questions.

The public repository may retain lawful manifests, checksums, scripts, and small
non-proprietary diagrams according to its evidence policy.

## Stop conditions

Stop adding complexity when:

- the artefact is visible in opaque grey;
- multiple windshield shells have not been isolated;
- imported normals have not been compared on a duplicate;
- camera/exposure changes between cases;
- HDRI, rain, droplets, bloom, glare, or depth of field are hiding the pattern;
- the user is about to retopologize before identifying whether the fault belongs to
  positions, loops, attributes, or material binding.

## Exit condition

This task is complete when the artefact has one supported classification, retained
evidence, and a reversible next action. A visually clean windshield alone is not a
successful diagnosis.