# DriveClub resource and semantic model

This document deliberately separates facts visible in pinned source code from
community reverse-engineering observations and VirtualAuto hypotheses.

## Code-proven resource identity

`SRC-CODE` at DriveClubFS commit
`836d5f09677dd7f30b92991a0f32e029487ae5cd`:

- a resource identifier is stored as a 64-bit value;
- the high 16 bits are interpreted as `ResourceTypeId`;
- the remaining 48 bits are exposed as the resource ID;
- each `ResourceInfo` records size, pack offset, dependency identifiers, names,
  and source-asset paths.

This is already enough to build a useful dependency graph without decoding mesh
payloads.

## Code-proven type catalogue

The pinned enum includes these high-value types:

| ID | Enum | Immediate research relevance |
| ---: | --- | --- |
| 2 | `RTUID_STREAM_FORMAT` | likely declares element or stream layout |
| 3 | `RTUID_VERTEX_BUFFER` | raw vertex stream storage |
| 4 | `RTUID_INDEX_BUFFER` | triangle/index storage |
| 5 | `RTUID_PIXEL_BUFFER` | textures and image data |
| 6 | `RTUID_SHADER` | shader-level resource |
| 7 | `RTUID_MATERIAL` | material resource |
| 8 | `RTUID_MESH` | mesh/submesh resource |
| 9 | `RTUID_RESOURCE_COLLECTION` | grouped resource graph |
| 11 | `RTUID_HIERARCHY` | transforms or scene relationships |
| 14 | `RTUID_MESHES` | mesh collection resource |
| 15 | `RTUID_SCENE` | scene-level resource |
| 28 | `RTUID_GPU_PROGRAM` | GPU program resource |
| 29 | `RTUID_GPU_PROGRAMBASE` | shared GPU-program data |
| 30 | `RTUID_ATTRIBUTE_SET` | candidate attribute semantics |
| 31 | `RTUID_ATTRIBUTE_SET_BINDINGS` | candidate attribute-to-stream bindings |
| 38 | `RTUID_BIN` | generic binary payload |
| 39 | `RTUID_XML` | XML payload |
| 60 | `RTUID_VEHICLE_CUSTOM_DATA` | vehicle-specific state or configuration |
| 62 | `RTUID_PROCEDURAL_PLACEMENT` | procedural placement data |
| 71 | `RTUID_TOP_MIPS` | separately stored high-resolution mip data |
| 76 | `RTUID_VEHICLE_PARTICLES_DATA` | vehicle particle-system data |

Enum names are strong orientation clues, not proof of each payload's internal
semantics.

## Current DriveClubFS decode boundary

`SRC-CODE`:

- the RPK parser validates a `Resource PacK file` header;
- it reads the resource information block, name pools, source-path pools,
  dependencies, and possible required-pack names;
- generic data construction is currently implemented for pixel buffers, binary
  resources, XML resources, and top-mip resources;
- the command-line RPK extraction switch currently writes pixel buffers, BIN,
  and XML payloads;
- mesh, material, shader, stream-format, hierarchy, and GPU-program payloads are
  enumerated but not decoded by that extraction path.

Therefore DriveClubFS is the filesystem and catalogue foundation, not yet a
complete car converter.

## Texture path visible in code

`SRC-CODE`:

- pixel buffers can obtain data from a linked top-mips resource;
- PS4 data is passed through a swizzle/deswizzle utility before DDS output;
- the code maps several linear, sRGB, float, BC1, BC3, BC4, BC5, BC6H, and BC7
  formats to DXGI/DDS representations;
- older PS3 pixel-buffer handling is explicitly skipped in the inspected path.

VirtualAuto must preserve the source pixel-format enum and sRGB/linear identity
beside every exported DDS. A successful DDS write does not establish the
texture's material role.

## Community-reported mesh structure

`SRC-COMMUNITY` from the ResHax DriveClub thread:

- mesh records were reported to reference model/submesh indices, vertex-buffer
  IDs, index-buffer IDs, vertex counts, index offsets, and index counts;
- position data and richer element data may be stored in separate vertex
  buffers;
- some investigated assets reportedly use multiple vertex and index files;
- observed strides include 12, 20, 24, 36, and 44 bytes in different contexts;
- half-float positions or attributes were reported in some assets;
- three UV sets were reported by a 2026 Noesis investigation;
- hierarchy resources were suspected or observed to supply per-part transforms,
  particularly for collision meshes.

None of those observations is promoted to a universal layout. The same stride
can describe different element sequences, and a community script that works on
one sample does not prove version-wide semantics.

## Community-reported element leads

A 2026 forum investigation reported element-stream cases resembling:

- a compact normal-like byte triplet plus one unknown byte;
- three UV-like entries selected by values observed as 0, 3, and 4;
- a three-float element;
- four-byte elements;
- colour-like four-byte elements.

These descriptions are retained only as parser hypotheses. VirtualAuto must tie
an element to its stream-format or attribute declaration, preserve raw bytes,
and test candidate decoders statistically and visually.

## Community-reported material-name leads

Forum output included semantic-looking names such as:

```text
glass_windscreen_outside_rain
body_livery_damage_carbon_lod3
wheel_paint_damage
```

These strings suggest that DriveClub material identity may encode part, state,
damage, weather, substrate, and LOD information. They do not prove how the
shader implements those states or whether every token has a stable grammar.

VirtualAuto should tokenize names only as a reversible secondary index. The
original full string remains authoritative.

## Proposed semantic graph

`HYP`:

```text
Mesh
  -> Position VertexBuffer
  -> Element VertexBuffer(s)
  -> IndexBuffer(s)
  -> StreamFormat
  -> AttributeSet
  -> AttributeSetBindings
  -> Material
       -> Shader
       -> GPUProgram / GPUProgramBase
       -> PixelBuffer(s)
  -> Hierarchy
  -> ResourceCollection / Scene / VehicleCustomData
```

The graph is intentionally broader than a conventional mesh exporter. Every
edge must come from a resource dependency, source field, or controlled
inference with confidence and evidence.

## Required raw catalogue fields

For each resource:

```text
pack SHA-256
pack-relative offset
payload size
resource UID
resource type ID and enum name
all names
all source-asset paths
all declared dependencies
raw payload SHA-256
parse status
parser commit
unknown trailing or unconsumed byte ranges
```

A parser that consumes the expected fields but leaves unexplained bytes must
report them. Silent trailing data is an unresolved field, not padding by
default.
