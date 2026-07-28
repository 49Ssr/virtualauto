# DriveClub Ferrari F40 archaeology status

## State

`active research; sparse 1.28 filesystem inspected, matching base required`

## Current baseline

- Blender production baseline: `5.0.1`
- Live MCP restoration build: Blender `5.2.0 LTS`; this is recorded separately
  and does not relabel earlier 5.0.1 synthetic evidence
- Original package or installed root: a private European `CUSA00003` 1.28
  update and a separate 1.28-labelled full-size container have been inspected;
  its extracted indexed filesystem is a sparse patch/repack composition and
  still requires the matching base contribution
- Existing third-party export: reported in private possession; not registered or
  committed
- Retained evidence: none
- Archaeology plan: [F40 target plan](../../asset_archaeology/driveclub/F40_TARGET.md)
- Private-source registration command: implemented and unit-tested
- Blender structural inventory: executed successfully on a synthetic 5.0.1 fixture
- DriveClubFS, ShadPKG, LibOrbisPkg, and 010GameTemplates: pinned as exact-commit
  submodules; a temporary, uncommitted DriveClubFS diagnostic patch read the
  accessible index far enough to expose the sparse-overlay failure mode
- DriveClubFS build: reproduced from the pinned source with .NET SDK 9.0.316;
  build warnings were retained as upstream findings, not silently treated as
  VirtualAuto validation
- Split-PKG inspector/assembler: implemented and tested; the real five-part
  1.28 update passed consecutive-index, single-header, uniform-chunk,
  declared-size, and immutable-source checks, then produced a checksummed
  19,191,300,096-byte private package
- Outer-package stage: implemented and tested; the real package yielded 39
  unencrypted outer entries with per-file SHA-256 records, while three encrypted
  entries and the PFS payload were explicitly skipped
- Indexed-filesystem wrapper: path-preflight and output verification are
  implemented and unit-tested; the new read-only structural inspector has run
  against a real filesystem and classified it without extracting payloads

## Private Blender working-copy state

`OBS-INSTRUMENT`, live MCP session on 2026-07-27; files remain outside Git:

- the current private working copy is `F40_MCP.blend` under the user's F40
  project directory;
- imported exterior materials, windows, lamps, badges, grilles, engine-bay
  parts, and preserved material slots have received a first controlled repair
  pass; this does not establish original DriveClub shader fidelity;
- a pre-camera/atmosphere checkpoint and two 640 x 360 A/B renders were retained
  in the private project directory;
- the active World uses its Sky Texture through an explicit Background closure,
  with a 0.533-degree solar angular diameter and no second Sun-light owner;
- a closed 120 x 120 x 42 m Cycles volume remains available as a local-mist
  experiment, but the user has excluded it from viewport and render; the
  current camera/compositor work is therefore atmosphere-off;
- ground visibility is an explicit 1500 m implementation prior, producing an
  extinction coefficient of 0.002608 1/m, split into scattering and absorption
  by a 0.95 single-scatter-albedo prior;
- the volume uses Blender 5.2 Volume Coefficients with a Mie phase function,
  12 um particle-diameter prior, and vertical density falloff;
- Mist, Z, Environment, Normal, and denoising-data passes are enabled, but Mist
  is disconnected from beauty and labelled diagnostic-only;
- the compositor order is noisy scene-linear radiance, guided denoise, an
  optional calibrated 85 mm distortion/TCA/vignetting stage, neutral fallback,
  a qualified ideal f/8 diffraction kernel for 3840 x 2160, a disabled generic
  Fog Glow approximation, then output;
- the original 36 x 24 mm / 50 mm `Camera2` remains untouched and ideal;
- a non-destructive 35/50/85 mm full-frame camera suite now shares one focus
  target while changing camera distance with focal length; the user selected
  the 85 mm compressed view as the current active camera;
- camera metadata records Canon EOS 5D Mark IV and Canon EF prime-lens
  candidates, verified aperture-blade counts, and pinned Lensfun calibration
  rows; the Canon EF 85 mm f/1.4L IS USM profile now has a generated,
  source-exact, hash-locked distortion/TCA/vignetting implementation active for
  the current 85 mm camera;
  a separately qualified ideal circular-aperture diffraction component is
  active for f/8 at 3840 x 2160, while the measured lens PSF, sensor MTF/noise,
  shutter, white balance, and camera response remain unapplied or unset;
- three 960 x 540 / 32-sample perspective renders, an 85 mm beauty A/B, four
  calibration-pattern renders, a scene-linear 3840 x 2160 source, a full-size
  lens A/B, and pre-suite/pre-lens checkpoints are retained privately; the
  original 3840 x 2160 effective render configuration and 250-sample setting
  were restored after the comparisons.

### Render-cost audit

`OBS-INSTRUMENT`, read-only audit plus unsaved/restored 960 x 540 ablation on
2026-07-28:

- Cycles is using the RTX 4070 Laptop GPU through OptiX; the CPU device is not
  enabled for the active OptiX backend.
- The render-visible scene contains 287 meshes and approximately 249,218 source
  polygons. No render subdivision modifier is active, and the excluded bounded
  mist is not linked into the World.
- The final state uses 250 samples, adaptive threshold 0.01, OIDN, GPU/full-
  precision compositing, Light Tree, 10 maximum bounces, 10 transmission
  bounces, and reflective/refractive caustics.
- After one persistent-data warm-up, a controlled 960 x 540 / 32-sample raw
  render took 1.675 s at the final bounce/caustic state. Disabling caustics took
  1.657 s, and also reducing diffuse/glossy/transmission bounces took 1.638 s.
  The 1.1-2.2 percent timing reduction is too small to justify changing final
  transport settings from this test.
- The two lower-cost images differ from baseline by about 51.3 dB PSNR at only
  32 samples. That comparison includes path/noise-sequence changes and is not a
  claim of perceptual equivalence.
- The same-source 4K compositor gates took approximately 58 s both before and
  after ideal diffraction, placing the added convolution cost within timing
  noise. The existing multi-channel Lensfun remap and full-resolution operation
  domain, not the Airy kernel, dominate the post stage.
- Repeating the gate after the source-exact Lensfun V2 correction took 60.4 s
  without diffraction and 58.4 s with it. The reversed timing confirms that
  this two-run difference is timing noise; it does not establish zero
  convolution cost.

No production render setting was changed. The largest defensible speed lever is
therefore a separate preview/draft state or fewer final samples after a real
noise-convergence sweep, not unvalidated bounce deletion. Persistent Data may
help repeated frames, but remains off until VRAM and stale-data behaviour are
tested at full resolution.

The active research contract is documented in
[Real camera and atmosphere pipeline](../../environment/REAL_CAMERA_AND_ATMOSPHERE_PIPELINE.md).

## Sparse-filesystem findings

`OBS-INSTRUMENT`, retained outside Git; observed 2026-07-22:

- the extracted root contains `game.ndx`, `game.chc`, and 88 split DAT files;
- the version-4300 `DATX` index declares 8,018 records, of which 1,135 carry a
  nonzero logical size;
- all 43 DAT indices referenced by active records are present as files, but 441
  active records cross one or more zero-sized logical chunks;
- 39 parsed DAT files use a zeroed `DATA` sentinel, and both expected index
  sentinels are zeroed;
- the reusable VirtualAuto inspector therefore classifies the set as
  `overlay_or_repack_requires_base`, not as a complete extractable filesystem.

File count and apparent byte size were misleading here: the split-DAT tables
encode missing base contribution inside files that still exist. This result is
structural evidence of an incomplete base/patch composition, not proof of bad
decryption and not an authenticity judgment about the package source.

## F40 resource evidence from the sparse overlay

`OBS-INSTRUMENT`, private partial output; no resource payload is committed:

- a valid `Resource PacK file` header associated with the Ferrari F40 was found
  in the logical stream represented by `game448.dat`;
- its table names `ferrari_f40.evomeshes`, `ferrari_f40.def`,
  `ferrari_f40.hkx`, original authoring paths, and body, window, lamp,
  dashboard, and detail textures;
- 144 structurally readable resource records were catalogued before the sparse
  stream became incomplete: 76 vertex buffers, 37 pixel buffers, 26 stream
  formats, 3 index buffers, 1 material, and 1 unresolved record;
- many referenced resource ranges extend into absent base chunks, so this is a
  dependency/format breakthrough rather than a complete model extraction.

The resource table confirms that the original asset is materially richer than
the third-party FBX export. It does not yet establish individual vertex
semantics, usable UV streams, shader behaviour, or manufacturer-accurate
material values.

## Direct user observations

`OBS-USER`, no repository artifact yet:

- the DriveClub-derived F40 export appears to have a substantial polygon and
  mechanical-detail advantage over typical competing-title exports;
- object, rig, and material-slot organization appears surprisingly conventional;
- UV behaviour appears incorrect, incomplete, or disconnected from the intended
  game material system.

These reports do not establish whether the fault lies in the original resource,
third-party exporter, missing material metadata, stream selection, transforms,
or Blender import.

## Current interpretation space

Possible causes of the UV symptom include:

1. the exporter selected the wrong UV stream;
2. several UV streams or per-material transforms were flattened;
3. the original shader used object/world coordinates for some effects;
4. vertex attributes or material parameters selected mapping behaviour;
5. topology or vertex-stream alignment was damaged during export;
6. the supplied file combines render, collision, LOD, or state meshes without
   their original semantic graph.

No cause is preferred until the existing export is registered and diagnosed.

## Package findings

`OBS-INSTRUMENT`, retained in the private run workspace rather than Git:

- content ID: `EP9000-CUSA00003_00-XXXXXXXDRIVECLUB`;
- `APP_VER`: `01.28`;
- `TARGET_APP_VER`: `01.27`;
- `CATEGORY`: `gp`;
- combined and header-declared byte size: `19,191,300,096`;
- combined SHA-256:
  `1fb9d39c3e596f9fae0ecf53a6bad54ff5775c60e8c9a30ac67a9819c1da10e0`.

These establish local byte custody and update identity. They do not establish
distribution authenticity, payload decryption, a complete base installation,
or permission to redistribute the package.

## Package-tool observations

`OBS-INSTRUMENT`, reproduced on 2026-07-22:

- ShadPKG `sfo-info` agreed with the VirtualAuto package identity.
- ShadPKG `pfs-info` crashed with access violation `0xC0000005` before listing
  files. Source review found unchecked invalid-RSA-result and missing-PFSC-magic
  paths that can feed invalid pointer arithmetic.
- LibOrbisPkg enumerated all 42 outer entries and validated the full PFS image,
  package body, digest table, entry groups, and package-header digest.
- LibOrbisPkg disagreed with five higher-level digests. This is retained as an
  unresolved validator/package-format discrepancy rather than silently treated
  as package corruption.
- LibOrbisPkg refused payload enumeration because the PFS is encrypted and no
  decryption key was supplied.
- VirtualAuto copied 39 unencrypted outer entries and skipped `.image_key`,
  `nptitle.dat`, and `npbind.dat` as encrypted. The accessible set includes
  `param.sfo`, PlayGo metadata for 96 chunks, update notes, images, delta tables,
  and trophy containers.

## Blockers

- matching `CUSA00003` base package or an installed-and-updated root remains
  necessary; the sparse 1.28 filesystem cannot reconstruct unchanged base
  chunks by itself;
- package payload access is blocked by encryption/key availability, not by the
  five-part assembly; the matching base or an accessible installed root remains
  the practical next source;
- exact existing-export provenance and exporter are unknown;
- no fresh Blender 5.0.1 forensic report exists;
- original mesh/material/hierarchy resources have not been catalogued;
- DriveClub mesh and element-stream semantics remain incomplete.

## Runtime configuration boundary

- Machine-readable F40 project manifest: not implemented
- Machine-readable camera/compositor contract: implemented and live-audited
- Material or asset compiler: not implemented
- Panel Colour Offset: unknown; no source or calibration record
- Bumper Gloss Mismatch: unknown; no source or calibration record
- Geometry attributes written from project overrides: none

This Markdown status is deliberately not an executable parameter source. A
future manifest may drive a compiler only after each value has units,
provenance, confidence, ownership, and one of the states `OEM-disclosed`,
`measured`, `calibrated`, or `artist-default`. Until then, the CLI must leave
these values unresolved rather than inventing plausible defaults.

## Next smallest actions

1. Register the existing export as an immutable private source asset with
   checksum and import provenance.
2. Run a non-destructive Blender 5.0.1 inventory of objects, mesh counts,
   attributes, UV layers, material slots, hierarchy, and custom normals.
3. Capture indexed-grid views for every UV layer without editing the mesh.
4. Compose a private base-plus-1.28 filesystem, rerun `driveclub inspect`, and
   require `complete_for_index` before listing or unpacking.
5. Catalogue the complete F40 RPK dependency graph before writing a model
   converter; preserve every unknown vertex and material field.
6. Run `audit_camera_pipeline.py` before the next final camera render; bypass or
   regenerate camera-specific stages when camera, aperture, resolution, colour
   management, or node state differs from the qualified contract.

The operational tooling is ready for step 1. Filesystem unpack remains blocked
until a composed base-plus-update set passes the structural inspector. No F40
record has been fabricated: private packages, exports, partial RPK data, and
extracted assets remain absent from this checkout.

## Changelog

### 2026-07-28

- Audited the pinned Lensfun implementation rather than relying only on its
  database schema. The audit found that the first map generator used PTLens
  database coefficients directly and omitted Lensfun's focal-preserving source
  rescaling. The visually plausible V1 maps are retained but marked
  superseded; the mistake is now explicit negative implementation evidence.
- Added a portable, `bpy`-free source-pinned implementation of Lensfun
  normalization, PTLens rescaling and reverse solving, poly3 TCA, and PA
  vignetting, plus a Blender-hosted packed-map generator that does not wire,
  save, or qualify its own output.
- Generated source-exact V2 maps, then rejected their Blender adapter after an
  identity-map falsification test proved that `x/(width-1)` is not Blender's
  Map UV pixel-centre convention. The permanent 64 x 32 test measured 17.21 dB
  PSNR for that convention and bit-exact reproduction for
  `(x+0.5)/width`, `(y+0.5)/height`.
- Generated V3 with the verified Map UV convention and froze its 960 x 540
  float32 hashes in the camera contract. Relative to V2 at 4K with diffraction,
  V3 measured 34.59 dB PSNR, 86.80 percent strong-edge-gradient ratio, and an
  overall luminance ratio of 0.99901. The larger edge difference reveals V2's
  resampling error rather than a new optical effect.
- Repeated straight-grid, flat-field, centred-edge, and off-axis-edge gates.
  The 0.5 scene-linear flat field measured 0.50001 at centre and 0.41920 one
  pixel inside every corner, with no unexpected asymmetry, fringe, halo, or
  framing failure.
- Re-ran the ideal-diffraction gate after the V3 correction: mean-luminance
  ratio 1.00030, strong-edge gradient ratio 0.95615, and PSNR 55.24 dB relative
  to the source-exact V3 bypass.
- Expanded the read-only live audit from 34 to 50 checks. It now verifies the
  four active map names, dimensions, packed state, and exact float32 pixel
  hashes in addition to camera, render, colour-management, and node state; the
  recovered live file passes all 50 checks against V3.
- Hardened the Blender map generator against stale imported code by explicitly
  reloading the portable Lensfun module on each run. An initial V3 generation
  attempt exposed Blender's persistent module cache by returning V2 hashes and
  was rejected before wiring.
- Preserved hash-matched pre-correction, post-implementation, and
  post-validation `.blend` checkpoints outside Git.

- Recovered cleanly from a Blender crash caused by a temporary probe retaining
  an RNA vector after its source node had been deleted; this was a probe-lifetime
  error, not a render, GPU, or scene failure. The failed probe did not remain in
  the saved file.
- Restored Lens Distortion dispersion to zero and retained a byte-identical
  pre-change recovery checkpoint.
- Added an ideal circular-aperture f/8 diffraction component using a
  pixel-integrated 9 x 9 Airy intensity kernel at 550 nm for the current
  3840 x 2160 output. It remains explicitly distinct from a measured Canon lens
  or sensor PSF.
- Passed a synthetic impulse test: all 81 coefficients were recovered and the
  normalized output energy was 1.0.
- Passed a same-source 4K beauty gate: mean-luminance ratio 1.00030, strong-edge
  gradient ratio 0.9563, and PSNR 55.29 dB relative to bypass, with no observed
  glow halo, chromatic fringe, or framing change.
- Preserved pre-implementation, post-implementation, and post-validation `.blend`
  checkpoints outside Git.
- Added a machine-readable camera/compositor contract and a read-only audit;
  its initial live run passed all 34 camera, render, sampling, denoising,
  colour-management, compositor-device, and node checks. The V3 work above
  subsequently expanded this to 50 checks.
- Proved the audit fails closed by temporarily changing the unsaved aperture to
  f/5.6: it returned exit status 2 and identified only the aperture mismatch;
  f/8 was restored before resaving.
- Left unmeasured flare, ghosts, veiling glare, optical low-pass-filter MTF,
  CFA/demosaic response, sensor noise, Canon colour response, white balance, and
  sharpening unset rather than creating stylistic substitutes.
- Audited the render-cost state and ran a small caustic/bounce ablation. The
  proposed transport cuts saved only 1.1-2.2 percent in the controlled low-cost
  screen, so final render settings were left unchanged.

### 2026-07-27

- Implemented the first Lensfun Canon EF 85 mm f/1.4L IS USM PTLens
  distortion, poly3 TCA, and aperture/distance-interpolated PA vignetting as a
  packed, bypassable compositor stage. This historical V1 omitted source-level
  PTLens coefficient rescaling and was superseded by V2 on 2026-07-28.
- Found and corrected an initially black Map UV result: Blender's Cycles UV-pass
  convention requires red/green coordinates with a constant blue validity
  channel of one. The failure was retained as a diagnostic result rather than
  hidden by an arbitrary node substitution.
- Passed neutral/profile grid, flat-field, hard-edge, and F40 beauty A/B checks.
- The first 3840 x 2160 gate exposed a compositor-domain failure: 960 x 540 map
  inputs caused Map UV to produce a quarter-size result in a black full-size
  canvas. Added explicit Render Size scaling for all coordinate and vignetting
  maps, then passed the repeated full-resolution gate.
- The corrected profile retained 97.98 percent of the neutral central strong-edge
  gradient metric and 97.51 percent of mean display-referred luminance. These
  are implementation diagnostics, not measured MTF or exposure claims.
- Activated the then-calibration-checked V1 profile for the current 85 mm camera through
  `LF85_09_CAMERA_SPECIFIC_MIX`. A proposed automatic camera-compatibility driver
  was invalid in the live compositor and was removed; Factor 0 is the required
  manual bypass before selecting the 35 or 50 mm cameras.
- Recorded the user's current atmosphere-off state: the bounded mist experiment
  remains in the file but is excluded from viewport and render.
- Recorded the first live Blender 5.2 F40 restoration state without committing
  private game-derived assets or the `.blend` file.
- Replaced compositor-only atmosphere intent with a bounded, coefficient-driven
  Mie volume illuminated by the same World sky as the car.
- Preserved Mist Pass as a diagnostic rather than a lighting claim.
- Added an explicitly neutral camera pipeline and a pinned, disabled Lensfun
  candidate instead of inventing lens distortion, TCA, vignetting, or PSF.
- Added a non-destructive 35/50/85 mm full-frame perspective suite, retained the
  original camera, and selected the 50 mm view as the active hero baseline after
  controlled low-resolution comparison renders.
- Retained atmosphere-off and atmosphere-on comparison renders outside Git.

### 2026-07-22

- Inspected the new 1.28-labelled package and its accessible filesystem without
  committing private data.
- Identified sparse split-DAT chunks and classified the set as a patch/repack
  overlay requiring matching base content.
- Recovered a genuine partial F40 RPK table and a 144-record resource catalogue;
  stopped short of claiming model extraction because payload ranges cross
  absent base chunks.
- Added a pure-Python, read-only filesystem classifier so this condition is
  detected before DriveClubFS listing or extraction.

- Validated the five numbered fragments of the European 1.28 update without
  modifying them.
- Read the retained package header and `param.sfo`, identifying the package as
  an update from 1.27 to 1.28 rather than a base installation.
- Assembled a new private package through the guarded PKG stage and retained
  fragment/output hashes plus the operation manifest outside Git.
- Built and tested pinned ShadPKG; retained its successful SFO result, PFS crash,
  and source-level failure analysis without running its write extractor.
- Built and tested pinned LibOrbisPkg as an independent parser; retained both
  its successful whole-PFS/body validation and its higher-level digest
  disagreements.
- Added a VirtualAuto-owned, containment-checked outer-entry extractor and ran
  it on the real package. Encrypted entries and the PFS remain untouched.

### 2026-07-20

- Established the F40 as VirtualAuto's first DriveClub archaeology target.
- Recorded the existing export only as an unverified user observation.
- Deferred material recreation and geometry cleanup until source semantics can
  be separated from exporter damage.
- Added a tested private-source registrar and non-mutating Blender 5.0.1
  inventory path without claiming that either has run on the F40.
- Pinned DriveClubFS and reproduced its .NET 9 build without claiming a real
  game-data extraction.
- Added private per-stage workspaces plus guarded filesystem listing and unpack
  commands.
- Consolidated repository navigation into `research/`, `workflows/`, `lab/`, and
  `dev/`; reran the Blender 5.0.1 synthetic smoke path and corrected custom
  property enumeration against the live Blender API.
- Defined the non-fabrication boundary for future project overrides and material
  compilation; no F40 optical parameter was promoted from status prose.
