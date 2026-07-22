# DriveClub open questions and research order

Questions are ordered to prevent downstream shader or Blender work from hiding
upstream extraction errors.

## Package and filesystem

Current evidence resolves the available package as the European `CUSA00003`
1.28 update targeting 1.27. VirtualAuto can now validate and assemble its five
numbered fragments without mutation. It does not yet resolve the matching base,
payload access, or installed-filesystem merge semantics.

1. Which matching base package or installed root will accompany the acquired
   European 1.28 update?
2. Which reviewed package-access path can expose the update payload with output
   containment and reproducible evidence?
3. Can the source distribution manifest or equivalent upstream hashes be
   recovered to verify the locally retained fragment hashes?
4. How are base and update files combined, and how are duplicate names resolved?
5. Does the resulting `.ndx/.dat` inventory match DriveClubFS expectations?
6. Can extraction be repeated from checksummed inputs with identical outputs?

## Resource graph

1. Which RPK contains the chosen vehicle root?
2. What does `RootIdentifier` point to for a vehicle pack?
3. Are `RequiredResourcePacksMaybe` entries hard dependencies, search paths, or
   optional references?
4. Are names and source-asset paths complete enough to recover authoring intent?
5. Are dependencies internal to one RPK, cross-pack, aliased, or versioned?
6. Which resources remain unreachable from the root but are still vehicle-related?

## Mesh and stream format

1. What is the versioned structure of `RTUID_MESH`?
2. How are submeshes, model indices, vertex buffers, index buffers, offsets,
   counts, and material references represented?
3. What do `RTUID_STREAM_FORMAT`, `RTUID_ATTRIBUTE_SET`, and
   `RTUID_ATTRIBUTE_SET_BINDINGS` declare?
4. Are positions isolated from element streams consistently or only for some
   layouts?
5. Which scalar encodings occur: float32, float16, normalized integers, packed
   signed formats, or scale/bias quantization?
6. How are per-stream and per-submesh counts reconciled?
7. Are indices 16-bit, 32-bit, mixed, strip-based, or always triangle lists?
8. What defines base vertex and index rebasing?
9. Which bytes remain unconsumed after a valid parse?

## Normals, tangents, colours, and UVs

1. Is a packed normal stored alone or with tangent sign, AO, or another scalar?
2. Are tangents explicit, reconstructed, or encoded through an attribute set?
3. How many UV streams can a mesh declare, and how does a material choose one?
4. Are UV transforms stored in materials or shader parameters?
5. Do colour-like attributes represent colour, masks, AO, damage, process
   direction, or packed unrelated values?
6. Are seams encoded through vertex duplication, indices, material boundaries,
   or explicit flags?
7. How do mirrored parts preserve tangent handedness?

## Materials, shaders, and state

1. What is the internal structure of `RTUID_MATERIAL`?
2. How does a material reference `RTUID_SHADER`, `RTUID_GPU_PROGRAM`, textures,
   and attribute bindings?
3. Which fields are stable parameter names versus hashes or program-specific
   slots?
4. Are paint face/flop, flakes, clearcoat, damage, rain, dirt, and LOD represented
   as parameters, shader variants, textures, material-name conventions, or
   separate resources?
5. How are sRGB and linear texture roles declared?
6. Are material names generated from a grammar or manually authored labels?
7. How are state variants selected at runtime?

## Hierarchy, rig, and vehicle semantics

1. What transforms are stored in `RTUID_HIERARCHY`, and in which matrix
   convention?
2. How are wheel, steering, suspension, doors, lights, wipers, gauges, engine
   parts, and damage pieces identified?
3. Are collision and render hierarchies shared or separate?
4. Where are LOD groups and switching thresholds stored?
5. What is contained by `RTUID_VEHICLE_CUSTOM_DATA`?
6. Are dashboard displays and status icons mesh/material resources, dynamic
   textures, GUI resources, or vehicle-state bindings?
7. Which resources drive windshield rain and vehicle particle states?

## Blender reconstruction

1. What coordinate conversion maps source axes and handedness without reflection
   or negative-scale side effects?
2. Which source attributes map directly to Blender mesh attributes, and which
   require sidecar records?
3. Can custom split normals be imported without recalculation?
4. How should multiple UV, colour, and unknown streams be named deterministically?
5. How are source material variants represented without producing hundreds of
   opaque Blender materials?
6. Can one importer output both a raw forensic collection and a separately
   rehabilitated production collection?
7. Which diagnostics must run automatically after every import?

## Research order

```text
source custody
-> filesystem reproducibility
-> RPK catalogue
-> dependency graph
-> one mesh payload
-> one position/index pair
-> every element stream
-> hierarchy
-> material graph
-> Blender diagnostics
-> physical reconstruction
```

Do not prioritize rain simulation, dashboard UI, paint recreation, or cinematic
rendering before the source geometry and dependency graph are reproducible.
