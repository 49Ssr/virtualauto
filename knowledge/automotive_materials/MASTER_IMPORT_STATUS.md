# Authoritative master import status

Status: **verified source available; repository transfer pending**

The exact authoritative source is available in the active project artifact
workspace as:

`Automotive_Body_RnD_Master_v5_PRACTICAL_UNIFIED.md`

Verified artifact facts:

- lines: `56,769`
- size: approximately `1,830.3 KiB`
- SHA-256: `62f0a3663811b7b7259dcd194798c2345e1475c7bcd2c387bc34630dd05f774d`
- Blender production baseline declared by the master: `5.0.1`

These facts describe the available source artifact; they do **not** claim that
it is already committed to VirtualAuto.

## Intended canonical destination

`knowledge/automotive_materials/Automotive_Body_RnD_Master.md`

The unified master remains authoritative. Any smaller retrieval files will be
generated deterministically from it and must identify the source commit,
master checksum, section ID, and source line range. Generated views must never
become competing manually edited masters.

## Controlled import gate

Before committing the file:

1. Recalculate SHA-256 from the exact transfer candidate and compare it with the
   value above.
2. Review for copyrighted, proprietary, personal, or extracted-game data.
3. Confirm Markdown structure and local-link behaviour.
4. Commit the unified source without rewriting or regenerating its content.
5. Add a provenance manifest recording the source artifact, transfer date,
   checksum, byte size, and repository commit.
6. Generate retrieval views only through a reviewed script and verify that a
   clean regeneration produces no diff.

Until the transfer is complete, no summarized or reconstructed prose may be
represented as the authoritative master.
