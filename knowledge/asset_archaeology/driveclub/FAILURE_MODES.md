# DriveClub failure modes and parser rules

These rules turn community failures and common reverse-engineering mistakes into
explicit engineering constraints. Community examples remain `SRC-COMMUNITY`
until reproduced.

## 1. Package and version confusion

### Failure

A parser appears broken because the filesystem combines an unsupported build,
incomplete update, or incorrectly merged base and patch content.

### Rule

Record package/build identity, complete input inventory, checksums, and merge
policy before debugging resource formats. Never overwrite duplicate base/update
files without retaining both originals and a collision report.

## 2. Treating enum availability as decoder support

### Failure

A tool enumerates `RTUID_MESH` or `RTUID_MATERIAL`, so the pipeline assumes it
can export those resources semantically.

### Rule

Separate:

- type recognised;
- payload located;
- raw payload extracted;
- structure parsed;
- semantic fields validated;
- Blender representation qualified.

DriveClubFS currently recognises many more types than its RPK extraction path
decodes.

## 3. Using stride as the vertex layout

### Failure

`stride == 44` becomes a hard-coded position/normal/UV layout that silently
corrupts another 44-byte stream.

### Rule

Stride is only the byte distance between records. Resolve layout from declared
stream-format, attribute-set, binding, or repeated sample evidence. Unknown
bytes remain named by offset, width, and stream—not by guessed semantic.

## 4. Collapsing position and element streams

### Failure

Only the obvious position buffer is imported, producing geometry with missing
UVs, normals, colours, or custom fields. Alternatively, an element buffer is
mistaken for interleaved positions.

### Rule

Catalogue every buffer referenced by a mesh and preserve their independent
counts, strides, offsets, and declarations. Join streams only through an
explicit index or count relationship.

## 5. Replacing all UV sets with one

### Failure

An exporter chooses a single UV channel, calls the others corrupt, and destroys
material, detail, mask, or state coordinates.

### Rule

Import every finite UV-like stream under a stable source name. Selection for a
specific material is an experiment. Preserve per-material scale/offset or stream
selectors if discovered.

## 6. Incorrect subset indexing

### Failure

A submesh's indices are interpreted as local when they are absolute, or are
rebased twice. Symptoms include exploded triangles, huge allocations, or geometry
referencing unrelated vertices.

### Rule

Record:

```text
raw index offset
raw index count
raw minimum index
raw maximum index
declared or inferred base vertex
rebasing operation
final minimum and maximum
```

Validate every final index against the selected vertex range before allocating
or constructing faces.

`SRC-COMMUNITY`: forum scripts reported that subtracting a minimum index or
applying a vertex offset was necessary for some subsets. This is not assumed for
all resources.

## 7. Hard-coded header subtraction

### Failure

A community sample uses a 28-byte resource header, so every index or vertex
buffer is globally advanced by 28 bytes.

### Rule

Parse and validate the resource header for each payload. Header size is a field
or versioned structure, not folklore. Store the payload start and original file
offset separately.

## 8. Control-flow loss

### Failure

A missing UV set triggers `break`, accidentally leaving the enclosing mesh loop
and skipping the rest of the resource. A 2026 forum investigation identified a
similar issue while increasing displayed meshes.

### Rule

Use per-resource and per-submesh result objects:

```text
parsed
partial
unsupported-layout
out-of-bounds
missing-dependency
invalid-count
```

One failed attribute must not discard unrelated meshes. Exceptions and early
returns must identify their scope.

## 9. Normal decoding by visual convenience

### Failure

Packed bytes are normalized until the model looks acceptable, or Blender
recalculates normals and hides a decoding error.

### Rule

Retain raw packed values. Candidate decoders must be checked for:

- expected component range and unit length;
- distribution over the sphere;
- relation to triangle geometric normals;
- continuity across non-seam edges;
- deliberate splits at material or hard edges;
- consistency across transformed parts;
- handedness and tangent-frame compatibility.

Recalculated normals are a diagnostic comparison only, not source recovery.

## 10. Collision geometry substituted for render geometry

### Failure

A collision mesh has cleaner scale or transforms, so it is used as the visual
asset despite missing UVs, normals, bevels, and render detail.

### Rule

Collision geometry can validate scale, part extents, pivots, or hierarchy. It
must retain a distinct semantic class and cannot silently replace render
geometry.

## 11. Ignoring hierarchy transforms

### Failure

Separate vehicle parts appear at the origin, collapsed, mirrored, or offset;
manual transforms are then baked without recording their source.

### Rule

Preserve local transforms, parent relationships, bind transforms, and the exact
matrix convention. Test row/column order, handedness, axis mapping, and matrix
composition on a multi-part sample before applying to an entire car.

## 12. Unit and half-float errors

### Failure

A cabin is flattened or the car is the wrong scale because half-floats,
quantized values, endianness, or per-stream scale/bias are misread.

### Rule

Check bounds before visual judgment. Compare decoded extents against known
vehicle dimensions only as a diagnostic, not as permission to stretch the
model. Record every scale and bias applied.

## 13. Material names treated as shader truth

### Failure

A name containing `carbon`, `rain`, `damage`, or `lod3` is converted directly
into a Blender shader architecture.

### Rule

Names are semantic leads. Link them to material payloads, shader/GPU-program
references, texture dependencies, render-state flags, and controlled in-game
observations before assigning optical meaning.

## 14. FBX as the source of truth

### Failure

A flattened FBX export becomes the canonical asset, even though it may have
lost stream semantics, material IDs, LOD links, hierarchy metadata, and unknown
channels.

### Rule

An FBX is a derived convenience representation. Register it as an `AST` source
only when the original package is unavailable, describe known losses, and never
use it to infer that absent engine data never existed.

## 15. Unbounded allocation and malformed input

### Failure

A wrong count or offset causes multi-gigabyte allocation, out-of-range reads, or
silent integer overflow.

### Rule

Every parser must enforce:

- file and payload bounds;
- checked arithmetic;
- configurable count and allocation ceilings;
- exact consumed-byte accounting;
- deterministic failure messages;
- no write outside an explicit output root;
- hostile-input assumptions even for private files.

## 16. Premature visual cleanup

### Failure

The model is welded, decimated, smoothed, triangulated, or UV-repacked before
source defects and exporter defects are distinguished.

### Rule

Maintain three separate states:

```text
immutable source interpretation
reversible diagnostic reconstruction
production rehabilitation
```

Every destructive production edit must trace back to the diagnostic state and
carry a loss assessment.
