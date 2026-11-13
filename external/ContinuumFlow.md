# Continuum Flow — VirtualAuto development build

The local variant fixes Blender workflow problems in Continuum Flow 0.4.0 Alpha.
Upstream labels it an alpha pre-release; this variant retains that experimental status.
Its existing nodes and saved node identifiers are retained. Pressure, advection
and combustion kernels are unchanged. Surface voxelization and the turbulence
force are corrected below.
This is not yet a validated replacement for a production car-fire setup.

## Source and files

- Upstream: <https://github.com/lutzr2000/Continuum_Flow>
- Revision: `30eb4728cbc2749fb26161b25fc5bd49ff2f8366`, held in
  [tools.lock.json](tools.lock.json). The builder reads this record.
- Changes: [changes.patch](../workflows/blender/continuum_flow/changes.patch).
- Build command: [continuum.py](../src/virtualauto/continuum.py).
- Executed checks: [verify.py](../workflows/blender/continuum_flow/verify.py),
  [solid_check.py](../workflows/blender/continuum_flow/solid_check.py) and
  [preview_check.py](../workflows/blender/continuum_flow/preview_check.py).

Upstream source, dependency wheels, caches and generated ZIPs live in ignored
`build/continuum-flow/` and `dist/`. They are not copied into tracked source.

## Changes in 0.4.5 VirtualAuto

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
5. Export evaluated local triangles directly, without selecting objects,
   changing mode or creating temporary scene objects. The previous exporter
   failed in Pose Mode and could leave a temporary object behind. The shape
   snapshot now comes from the simulation's start frame, independent of the
   frame the artist was viewing.
6. Load the VDB through Blender's data API, preserving mode and selection.
   The Output node's native **Material** picker assigns the same chosen
   material on each bake, including after Free Bake.
7. Reject voxel cells beyond the actual triangle's surface tolerance. Upstream
   marked cells near its plane anywhere in its bounding box, including points
   well outside the triangle. This could overfill collision/source masks.
   GPU checks cover an interior point, a nearby edge, a distant exterior point,
   reversed winding and a degenerate triangle.
8. Skip timeline sampling when a control has no animation. Constant physics,
   source and force settings no longer trigger redundant scene-frame updates.
9. Replace the identical x/y/z turbulence force with the curl of three
   decorrelated noise potentials. The field moves continuously through space
   instead of multiplying a fixed pattern by a sine that periodically becomes
   zero. Amplitude, Scale, Frequency and Seed remain the existing controls;
   Frequency now controls movement through the noise field. This uses analytic
   noise derivatives, with GPU checks against finite differences. The approach
   follows [Bridson et al.'s curl-noise construction](https://www.cs.ubc.ca/~rbridson/docs/bridson-siggraph2007-curlnoise.pdf);
   its boundary-aware potential modulation is not implemented here.
10. Clear smoke, fuel, oxygen and flame in solid cells after scalar advection and
    combustion. The earlier obstacle boundary pass ran before these operations,
    allowing them to repopulate collision cells before VDB export and preview.
    Fluid cells, temperature and velocity are left unchanged by this final pass.

No new panels, scene handlers, automatic materials or scene-conversion logic
were added. Installing this variant does not convert a Mantaflow setup.

## Build and install

With VirtualAuto installed in a Python 3.12+ environment that has pip and Git:

```text
virtualauto continuum build
virtualauto continuum check --blender "C:\path\to\blender.exe"
```

The build fetches the pinned source and Windows CPython 3.13 wheels, applies
the patch, and writes `dist/continuum_flow-0.4.5-virtualauto-windows-x64.zip`.
The check runs factory Blender with an original small emitter; it does not
open a user's scene or enable an add-on in their preferences. Its result is
`build/continuum-flow/verification.json`. The ZIP is then installed in an isolated
profile, and another Blender process checks that its nodes and GPU access survive
a normal startup. Those results are in `build/continuum-flow/package_verification.json`.

For Blender 5.2.3, install the ZIP through Preferences → Extensions →
Install from Disk. It uses the upstream `continuum_flow` extension ID, so it
replaces the ordinary installation rather than registering duplicate nodes.
Save the scene and stop active Continuum jobs before updating the extension.
Blender may request a restart when compiled dependency wheels change; their
versions are unchanged in this variant.

## Validation on 2026-11-13

The 0.4.5 check passed on Blender 5.2.3 LTS and the RTX 5090 Laptop GPU:

- A GPU fixture clears all four scalar fields in stationary and moved solid cells.
  Fluid cells and unmapped pool capacity remain bit-for-bit unchanged.
- A seven-frame bake with a moving collision wall has zero smoke, fuel or flame
  values in solid cells at every actual cache submission. It writes seven VDBs,
  loads at the requested frames and visibly changes the Cycles test image.
- The actual ZIP installs and enables in an isolated profile. Node registration
  and OpenCL GPU detection also pass after a separate normal Blender startup.

The scalar exclusion pass prevents values inside voxelized solids. It does not
make openings narrower than the voxel size resolvable, or guarantee that a
backtraced fluid path never crosses a wall. Check the result around thin panels.

The following checks were first recorded on 2026-11-08 and rerun with 0.4.5:

Executed on Blender 5.2.3 LTS, Windows x64, RTX 5090 Laptop GPU, using OpenCL:

| Check | Result |
| --- | --- |
| Staging-buffer growth/shrinkage, same GPU readback | Field replacements 9 → 1; counter replacements 9 → 0 |
| Existing Viewer appearance properties while job marked active | Current preview values updated |
| Evaluated subdivision mesh exported from Pose Mode | Triangles match; source vertices/UVs, selection and mode unchanged; no temporary scene objects |
| VDB loaded from Pose Mode with the chosen material | Material assigned; mode and selection unchanged |
| Triangle voxelization on the GPU | Upstream incorrectly marks the distant exterior cell; corrected kernel rejects it and retains the surface/edge cells |
| Turbulence on the GPU | Axis correlations change from 1.0 to approximately 0.10, 0.06 and -0.06 in the sampled field; the field is nonzero at time zero, scales with amplitude and changes with seed/time |
| Analytic noise gradient and curl | Maximum gradient error versus finite differences approximately 0.00036; sampled divergence RMS approximately 0.00034, versus 3.31 for the old diagonal force |
| Unanimated Source controls | Zero scene-frame updates during animation export |
| Cycles image with VDB versus the same image without it | Nonzero pixel difference (mean absolute RGBA difference approximately 0.029 at 64 x 64) |
| Small smoke/fire solve and VDB export | Seven files with nonempty density; approximately 1.4 seconds with compiled kernels cached in the moving-wall fixture |
| Requested start frame 41 | File 1 loads at 41, file 2 at 42, file 7 at 47 |
| Small warmed worker cancellation | Approximately 0.015 seconds in this fixture |
| Blender extension archive validator | Passed |
| Actual ZIP installed and enabled in a fresh Blender profile | Passed; 5090 detected through bundled dependencies |

In the local stationary-car scene, seven mesh emitters and one closed box
collision proxy produced 120 frames at 0.06 m cell size in **18.94 seconds**,
including geometry export, simulation, VDB writing and loading. The 120 VDBs
occupied approximately 223 MiB. A five-second 640 x 360 camera preview at
12 fps showed flames at the hood and cabin openings with downwind smoke.
The maximum domain was 12 x 40 x 20 m with adaptive bounds. The project and
its assets are private and are not included as a reproducible benchmark.

These results do not establish large-domain speed, real-time playback,
long-bake stability, physical accuracy or equivalence to Fumaris. First-use
kernel compilation was approximately five seconds in the initial small run.
Blender 5.2 does not expose the proposed `GPUTexture.update` Python API; that
approach was rejected before packaging.

## Using existing emitters

Reference each emitter object with a Geometry node and connect it to a Source
node. Source controls set fuel, smoke, temperature and velocity. Geometry
nodes feeding an Obstacle node provide collision surfaces. Mantaflow Flow,
Effector and Domain modifier settings do not drive this solver; retain them
disabled if you need to return to the old setup.

Domain **Resolution** is a cell size in metres, not Mantaflow's resolution
division count: a smaller value is finer and more expensive. The Reference
Frame object's origin places the bottom centre of the domain. Leave enough
space above and downwind; adaptive simulation stays within those bounds.

The exporter evaluates modifiers once at the start frame, then samples object
world transforms. It does **not** export a changing mesh on every frame. In
particular, bone-deformed panels and collision surfaces do not continuously
follow the rig. This remains an upstream limitation, not a supported feature
of this variant.

For rigid moving panels, a separate low-detail collider driven by the panel's
bone through an object constraint can use the supported object-transform
animation. Keep the render mesh and its UVs intact. Check source/collider
overlap at the chosen cell size: detailed engine/interior collision copies can
block the emitters, and voxel thickness can close small openings. A single
chassis box alone cannot stop smoke passing through the rest of the body.

Choose a volume material on the Output node before baking. Density, flame and
temperature grids need a shader as well as a completed cache. Use a small
camera render to check their actual visibility: nonempty VDB grids alone do
not establish a useful image. The fixture rendering check proves that exported
smoke can be rendered; it does not qualify a particular fire shader or car shot.

## Licence and redistribution

The upstream extension manifest declares GPL-3.0-or-later. The patch and
Blender verification helpers have the same licence; see
[LICENSE](../workflows/blender/continuum_flow/LICENSE).

The bundled `continuum_vdb_writer` native wheel's metadata provides no licence
or source link. Its build source has not been traced. This local development
package is not cleared for public binary redistribution. Source patches can
be reviewed independently; a public installable release needs that dependency
resolved. Other VirtualAuto code and research retain their existing status.
