# DriveClubFS gap audit

Inspected revision:
`836d5f09677dd7f30b92991a0f32e029487ae5cd`

This is a VirtualAuto code-review record, not a condemnation of the upstream
project. DriveClubFS supplies valuable filesystem, RPK, resource-catalogue, and
texture groundwork. The purpose here is to identify assumptions VirtualAuto
must not inherit blindly when building a new semantic pipeline.

## Audit states

- `CODE-FACT`: directly visible in the pinned source;
- `ANOMALY`: deserves a targeted test but is not yet proven wrong;
- `GAP`: intentionally or currently unsupported behaviour;
- `VA-RULE`: requirement for VirtualAuto-owned code.

## 1. Resource catalogue is broader than payload decoding

`CODE-FACT`: `ResourceTypeId` enumerates mesh, material, shader, stream-format,
attribute, hierarchy, GPU-program, vehicle, and particle resources.

`CODE-FACT`: `ResourcePack.GetResourceData<T>` currently constructs decoders for
pixel buffers, BIN, XML, and top-mips resources. The command-line RPK extractor
writes pixel buffers, BIN, and XML.

`GAP`: recognising a type ID does not decode its payload.

`VA-RULE`: VirtualAuto status must distinguish `enumerated`, `located`,
`raw-extracted`, `structurally-parsed`, `semantically-validated`, and
`Blender-qualified`.

## 2. Resource names are trusted as output paths

`CODE-FACT`: BIN, XML, and DDS output paths are built from resource names through
`Path.Combine`, and the inspected path does not visibly normalize the result to
an approved output root.

`ANOMALY`: a name containing rooted paths or parent traversal could escape the
intended directory; different names could also collide after extension changes.

`VA-RULE`:

- treat resource names as metadata, not trusted filesystem paths;
- generate safe deterministic filenames from UID and type;
- preserve the original name in the manifest;
- reject traversal and rooted paths;
- report collisions instead of overwriting.

## 3. First-name assumptions

`CODE-FACT`: several extraction paths access `Names[0]`.

`ANOMALY`: `ResourceInfo` permits a zero-length name list, so unnamed resources
can produce an index failure in those paths.

`VA-RULE`: unnamed resources remain exportable by stable UID. Names are optional
aliases.

## 4. Resource-pack lifetime

`CODE-FACT`: `ResourcePack` implements `IDisposable` for its own stream.

`CODE-FACT`: the inspected command-line RPK path opens the main and top-mip packs
without an enclosing `using` declaration, and `ResourcePack.Dispose` does not
visibly iterate and dispose `TopMipsPacks`.

`ANOMALY`: repeated batch extraction can retain file handles or streams longer
than intended.

`VA-RULE`: every opened pack has explicit ownership and deterministic disposal,
including dependency and top-mip packs.

## 5. Broad exception handling

`CODE-FACT`: top-mip lookup catches a general `Exception`, does not use the
captured exception object, and converts the failure to a console message.

`ANOMALY`: corruption, programming errors, and an expected missing dependency
can become indistinguishable.

`VA-RULE`: use typed failure records with resource UID, expected pack, exception
class, byte location where available, and recovery scope. One missing top mip
must not hide unrelated parser defects.

## 6. Pixel-format naming and mapping anomaly

`CODE-FACT`: the PS4 enum contains separate `DXT3_*`, `DXT5_*`, `BC4`, `BC5`,
`BC6H`, and `BC7` values.

`CODE-FACT`: the inspected mapping sends `DXT3_*` to BC3 and `DXT5_*` to BC5.

`ANOMALY`: conventional DirectX naming normally associates DXT5 with BC3,
whereas BC5 is a two-channel format. Evolution's enum names may be historical or
non-standard, so the mapping cannot be declared wrong from naming alone.

`VA-RULE`: validate each enum against payload size, channel behaviour, known
reference textures, alpha use, and an independent decoder. Preserve the source
enum even after DDS conversion.

## 7. Block-compressed allocation assumptions

`CODE-FACT`: output size is calculated from `width * height * bits-per-pixel / 8`.

`ANOMALY`: block-compressed formats require block-rounded dimensions; the simple
formula is equivalent for many power-of-two textures but can be wrong for small
or non-multiple-of-four dimensions.

`VA-RULE`: calculate compressed storage from block count and validate the source
payload length before deswizzling.

## 8. Mip metadata requires verification

`CODE-FACT`:

- the DDS flags include mipmap state when the source reports more than one mip;
- `LastMipmapLevel` is assigned a constant in the inspected construction;
- a loop that would reduce width and height by `StartMip` is commented out;
- top-mip resources can replace the local data array.

`ANOMALY`: dimensions, mip count, top-mip selection, and written DDS payload may
not describe every source combination correctly.

`VA-RULE`: enumerate each mip explicitly with source location, dimensions,
format, byte length, and checksum. Do not infer a full chain from one flag.

## 9. Table-of-contents and count hardening

`CODE-FACT`: the RPK parser reads table offsets, resource counts, alias and
dependency counts, string-pool sizes, and version-dependent counts.

`ANOMALY`: the inspected high-level code does not visibly apply configurable
ceilings or report exact consumed versus declared byte ranges.

`VA-RULE`: use checked arithmetic, file-bound validation, count ceilings,
allocation ceilings, and retained unconsumed-byte reports. Private game files
are still treated as hostile parser input.

## 10. Generic decoder type cast

`CODE-FACT`: `GetResourceData<T>` chooses a decoder from the resource type and
casts the resulting base object to caller-supplied `T`.

`ANOMALY`: an incorrect caller type produces a runtime cast failure rather than
a compile-time or explicit semantic error.

`VA-RULE`: expose a non-generic decoded-resource result or verify requested type
against resource type before reading payload bytes.

## 11. Console output is not a provenance log

`CODE-FACT`: extraction state is primarily written to the console.

`GAP`: the inspected workflow does not produce a deterministic machine-readable
manifest of every input, output, resource status, warning, and checksum.

`VA-RULE`: all VirtualAuto transformations emit JSON records and a stable text
log. Console output is a convenience view only.

## 12. No semantic intermediate

`GAP`: outputs are files and DDS resources rather than a loss-accounted vehicle
asset graph.

`VA-RULE`: never extend the extractor directly into an opaque FBX writer. Build:

```text
raw catalogue
-> byte-preserving resource decoders
-> semantic intermediate
-> Blender importer
```

## Upstream reuse decision

DriveClubFS should be treated as:

- a high-value reference implementation;
- a candidate submodule for reproducible filesystem/RPK extraction after local
  execution tests;
- a source of resource IDs and format hypotheses;
- not the architectural core of VirtualAuto's Blender importer.

Where practical, improvements should be contributed upstream rather than kept
as silent private fixes. VirtualAuto-specific provenance and semantic layers can
remain separate adapters.
