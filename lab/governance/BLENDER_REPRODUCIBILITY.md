# Blender reproducibility baseline

VirtualAuto distinguishes a documented Blender proposal from a captured runtime
and from validated visual evidence. A node diagram or Python script alone is not
proof that Blender executed it correctly.

## Baseline execution

The production baseline is Blender `5.0.1`. Automated checks should start from
factory settings and avoid user startup files:

```text
blender --background --factory-startup scene.blend \
  --python-exit-code 1 \
  --python workflows/blender/scripts/capture_runtime_manifest.py -- \
  --id RUN-PROJECT-TEST-001 \
  --output lab/evidence/manifests/blender-run.json
```

The capture script refuses a version other than `5.0.1` unless the caller uses
the explicit `--allow-version-mismatch` research override. That override must
not be described as baseline validation. It also refuses paths outside the
repository and will not overwrite an existing manifest unless `--overwrite` is
supplied intentionally.

The packaged smoke harness creates an original temporary scene and captures a
runtime manifest plus structural inventory:

```text
virtualauto blender-smoke
```

Blender evaluates command-line options in order, so `--python-exit-code 1`
must appear before `--python`. The first local execution caught this exact
failure-propagation risk and also confirmed that Blender 5.0.1 exposes EEVEE as
the `BLENDER_EEVEE` RNA enum. These are runtime observations, not assumptions
carried over from an older Blender release.

## Manifest boundary

The runtime manifest records:

- exact Blender version and build identifiers;
- platform and bundled Python version;
- scene name, saved-file checksum, and non-sensitive filename;
- engine, resolution, frame, samples, denoising, and device where exposed;
- display, view transform, look, exposure, and gamma;
- an external OCIO configuration checksum when `OCIO` explicitly overrides the
  Blender default.

It deliberately does not claim:

- visual correctness;
- deterministic equality across CPU and GPU backends;
- addon or extension completeness;
- driver-level reproducibility;
- evidence of a successful render.

Those require linked experiment, evidence, observation, and performance records.

## Two validation tiers

1. **Structural CPU tier:** fresh file, node/socket discovery, deterministic
   manifests, scene loading, and failure-on-exception.
2. **Visual/performance tier:** declared device and driver, retained renders,
   raw-versus-denoised comparisons, motion tests, timings, and tolerances.

Exact image hashes are appropriate only when the platform and render path are
known to be bit-stable. Otherwise use declared numeric or perceptual tolerances.
