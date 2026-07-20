# Operational baseline

VirtualAuto is considered an operational foundation—not a finished automotive
pipeline—when all of the following are true:

- the canonical automotive master and deterministic retrieval index validate;
- JSON record contracts and cross-record identifiers validate;
- the packaged `virtualauto` command works on Windows and Linux Python 3.12;
- private source assets can be registered without copying or exposing them;
- Blender 5.0.1 can create a synthetic scene, capture its runtime, and inventory
  its structure through guarded scripts;
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
virtualauto blender-smoke --help
```

The current production baseline is Blender 5.0.1. Later versions may be tested,
but must not silently replace the baseline in an evidence record.
