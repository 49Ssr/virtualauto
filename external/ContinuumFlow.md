# Continuum Flow — VirtualAuto development build

The local variant fixes Blender workflow problems in Continuum Flow 0.4.0.
Its existing nodes, saved node identifiers and numerical kernels are retained.
This is not yet a validated replacement for a production car-fire setup.

## Source and files

- Upstream: <https://github.com/lutzr2000/Continuum_Flow>
- Revision: `30eb4728cbc2749fb26161b25fc5bd49ff2f8366`, held in
  [tools.lock.json](tools.lock.json). The builder reads this record.
- Changes: [changes.patch](../workflows/blender/continuum_flow/changes.patch).
- Build command: [continuum.py](../src/virtualauto/continuum.py).
- Executed checks: [verify.py](../workflows/blender/continuum_flow/verify.py) and
  [preview_check.py](../workflows/blender/continuum_flow/preview_check.py).

Upstream source, dependency wheels, caches and generated ZIPs live in ignored
`build/continuum-flow/` and `dist/`. They are not copied into tracked source.

## Changes in 0.4.1 VirtualAuto

1. Reuse OpenCL preview staging buffers while their capacity is sufficient.
   They can grow and remain at peak capacity until the job ends. This reduces
   allocation churn; it does not eliminate Blender's texture uploads.
2. Keep the existing Viewer smoke/flame appearance controls editable during a
   bake and apply changes to the current preview immediately. Simulation
   controls and the Live Preview toggle retain their existing restrictions.
3. Align imported VDB sequences with the requested simulation start frame and
   set their duration from the file indices. Ordinary Blender Volume sequence
   playback is still used.
4. Stop exporting at the last sample within the requested duration. The small
   fixture previously wrote eight files for frames 41–47; it now writes seven.
   This bounds cache output; it does not redesign the solver's time stepping.

No new panels, scene handlers, materials or scene-conversion logic were added.
Installing this variant does not convert a Mantaflow setup.

## Build and install

With VirtualAuto installed in a Python 3.12+ environment that has pip and Git:

```text
virtualauto continuum build
virtualauto continuum check --blender "C:\path\to\blender.exe"
```

The build fetches the pinned source and Windows CPython 3.13 wheels, applies
the patch, and writes `dist/continuum_flow-0.4.1-virtualauto-windows-x64.zip`.
The check runs factory Blender with an original small emitter; it does not
open a user's scene or enable an add-on in their preferences. Its result is
`build/continuum-flow/verification.json`.

For Blender 5.2.3, install the ZIP through Preferences → Extensions →
Install from Disk. It uses the upstream `continuum_flow` extension ID, so it
replaces the ordinary installation rather than registering duplicate nodes.
Stop active Continuum jobs and restart Blender before changing installations.

## Validation on 2026-11-07

Executed on Blender 5.2.3 LTS, Windows x64, RTX 5090 Laptop GPU, using OpenCL:

| Check | Result |
| --- | --- |
| Staging-buffer growth/shrinkage, same GPU readback | Field replacements 9 → 1; counter replacements 9 → 0 |
| Existing Viewer appearance properties while job marked active | Current preview values updated |
| Small smoke/fire solve and VDB export | Seven files with nonempty density; approximately one second with compiled kernels cached |
| Requested start frame 41 | File 1 loads at 41, file 2 at 42, file 7 at 47 |
| Small warmed worker cancellation | Approximately 0.015 seconds in this fixture |
| Blender extension archive validator | Passed |
| Actual ZIP installed and enabled in a fresh Blender profile | Passed; 5090 detected through bundled dependencies |

These results do not establish large-domain speed, real-time playback,
long-bake stability, physical accuracy or equivalence to Fumaris. First-use
kernel compilation was approximately five seconds in the initial small run.
Blender 5.2 does not expose the proposed `GPUTexture.update` Python API; that
approach was rejected before packaging.

## Licence and redistribution

The upstream extension manifest declares GPL-3.0-or-later. The patch and
Blender verification helpers have the same licence; see
[LICENSE](../workflows/blender/continuum_flow/LICENSE).

The bundled `continuum_vdb_writer` native wheel's metadata provides no licence
or source link. Its build source has not been traced. This local development
package is not cleared for public binary redistribution. Source patches can
be reviewed independently; a public installable release needs that dependency
resolved. Other VirtualAuto code and research retain their existing status.
