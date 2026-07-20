# Operational baseline

VirtualAuto is considered an operational foundation, not a finished automotive
pipeline, when all of the following are true:

- the canonical automotive master and deterministic retrieval index validate;
- JSON record contracts and cross-record identifiers validate;
- the packaged `virtualauto` command works on Windows and Linux Python 3.12;
- private source assets can be registered without copying or exposing them;
- Blender 5.0.1 can create a synthetic scene, capture its runtime, and inventory
  its structure through guarded scripts;
- the development add-on registers, exports the same structural inventory, and
  unregisters cleanly inside Blender 5.0.1;
- the panel-relative tangent-frame invariant passes inside Blender's math backend
  with retained scope and numeric evidence;
- the resulting evidence is retained with explicit scope and checksums;
- external tools are pinned and legally classified before integration;
- CI repeats the platform-independent checks from a fresh checkout.

This baseline does **not** establish that DriveClub packages can be decrypted,
that DriveClub geometry can be decoded, or that an automotive material is
physically validated. Those remain separate experiments requiring lawful input
and retained evidence.

## Daily entry points

```text
virtualauto doctor
virtualauto build-index
virtualauto validate
virtualauto register-source --help
virtualauto record-evidence --help
virtualauto research --help
virtualauto workspace --help
virtualauto blender-smoke --help
virtualauto driveclub --help
```

The DriveClub filesystem stage additionally requires the pinned DriveClubFS
submodule and a .NET 9 SDK. Its guarded wrapper can build, preflight-list, and
unpack the indexed filesystem. Package access, RPK extraction, geometry decoding,
and Blender reconstruction remain distinct stages and are not implied by a
successful filesystem unpack.

The current production baseline is Blender 5.0.1. Later versions may be tested,
but must not silently replace the baseline in an evidence record.
