# DriveClub pipeline boundary

## Intended chain

```text
lawfully accessible PS4 package or root installation
    -> package inspection/extraction candidate
    -> DriveClub .ndx/.dat filesystem
    -> DriveClubFS filesystem extraction
    -> RPK catalogue and dependency graph
    -> raw resource preservation
    -> format-specific decoders
    -> VirtualAuto semantic intermediate
    -> Blender 5.0.1 importer
    -> diagnostics and controlled reconstruction
```

Each arrow is a recorded transformation. A successful later stage does not
retroactively validate an earlier one.

## Stage 0 — Source custody

Create an `AST` record before processing. Record source provenance, custody,
rights status, checksum, byte size, game/build identity where known, and whether
the source is a base package, update, combined root, or third-party export.

Never commit the source package or extracted data.

## Stage 1 — Package layer

Candidate instruments:

- `EXT-SHADPKG`: package analysis and extraction candidate;
- `EXT-PKGTOOLBOX`: inspection candidate, blocked from integration pending
  license clarification.

`SRC-UPSTREAM-DOC`: both projects describe PS4 package operations.

`UNRESOLVED`: VirtualAuto has not established which package states, keys,
licensing environments, or DriveClub revisions each tool can process safely and
losslessly. Package access must be tested on a lawful sample before either tool
becomes a dependency.

## Stage 2 — Evolution filesystem

`SRC-UPSTREAM-DOC`: DriveClubFS accepts a DriveClub `.ndx` index paired with
`.dat` data and documents support for versions 1.00, 1.28, and an alpha/prototype
build.

Required outputs:

- exact input file inventory and checksums;
- file listing before extraction;
- extraction log;
- output inventory with checksums;
- failed or missing entries;
- DriveClubFS commit and command line;
- build/version assumption.

`SRC-COMMUNITY`: the ResHax thread reports that base and update files may need to
be combined without replacing duplicate names. Treat this as a test hypothesis,
not a universal instruction. Preserve the original base and update inventories
and prove the merge policy on a controlled file graph.

## Stage 3 — RPK catalogue

Do not begin by exporting textures or models. First create a catalogue for every
resource pack:

```json
{
  "pack": "private/path/example.rpk",
  "root_identifier": "...",
  "required_packs": [],
  "resources": [
    {
      "uid": "...",
      "type_id": 8,
      "type_name": "RTUID_MESH",
      "offset": 0,
      "size": 0,
      "names": [],
      "source_asset_paths": [],
      "dependencies": []
    }
  ]
}
```

`SRC-CODE`: DriveClubFS already reads resource IDs, offsets, sizes,
dependencies, names, source-asset paths, root identity, and possible required
resource packs. The first VirtualAuto extension should export those facts
without decoding payload semantics.

## Stage 4 — Raw resource preservation

For each referenced resource, preserve:

- pack identity and exact byte range;
- resource UID and type ID;
- original names and source paths;
- dependency edges;
- raw payload checksum;
- parser version;
- parse status and error;
- all unknown bytes.

Do not use file extensions as proof of semantic type. Keep the engine resource
identifier beside any convenience extension.

## Stage 5 — Semantic intermediate

The intermediate must be independent of FBX and Blender. A vehicle package may
contain:

```text
vehicle
  meshes
    submeshes
      position streams
      element streams
      index streams
      stream-format declarations
      material references
  materials
    shader and GPU-program references
    textures and parameters
  hierarchy and transforms
  LOD and state relationships
  collision or physics geometry
  vehicle custom data
  unknown resources
```

Required design properties:

- byte-preserving unknown-field sidecars;
- explicit coordinate-system and unit metadata;
- multiple UV and colour streams;
- original and rebased index values;
- per-stream format declarations;
- no automatic normal recalculation;
- no implicit triangulation changes;
- deterministic serialization;
- loss report for every conversion.

## Stage 6 — Blender import

Blender 5.0.1 receives a derived copy, never the immutable source.

The importer should create stable custom attributes such as:

```text
dc_resource_uid
dc_mesh_index
dc_submesh_index
dc_material_uid
dc_lod
dc_source_stream
dc_unknown_<id>
```

Names are provisional until the intermediate schema exists. Unknown values must
not be assigned confident semantic names merely to make the Blender UI tidy.

## Stage 7 — Diagnostics before materials

First-pass outputs:

1. object and submesh inventory;
2. axis, handedness, unit, and bounds report;
3. triangle validity and index-range report;
4. normal length and orientation display;
5. every UV stream under an indexed grid;
6. vertex-colour and unknown-byte visualizations;
7. material and dependency graph;
8. hierarchy and transform comparison;
9. source-versus-import checksum and count report.

Only after these pass should VirtualAuto construct replacement automotive
materials.
