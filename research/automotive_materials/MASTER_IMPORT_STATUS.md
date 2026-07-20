# Authoritative master import status

Status: **imported byte for byte; canonical checksum enforced**

The exact authoritative source is available in the active project artifact
workspace as:

`Automotive_Body_RnD_Master_v5_PRACTICAL_UNIFIED.md`

Verified artifact facts:

- lines: `56,769`
- size: approximately `1,830.3 KiB`
- SHA-256: `62f0a3663811b7b7259dcd194798c2345e1475c7bcd2c387bc34630dd05f774d`
- Blender production baseline declared by the master: `5.0.1`

The imported repository artifact is:

`research/automotive_materials/Automotive_Body_RnD_Master.md`

Its machine-readable provenance record is
[`master.provenance.json`](master.provenance.json). Repository validation now
recalculates the checksum, byte size, UTF-8 decoding, and line count.

## Canonical destination

`research/automotive_materials/Automotive_Body_RnD_Master.md`

The unified master remains authoritative. The generated heading index is
produced only by
[`dev/scripts/build_master_index.py`](../../dev/scripts/build_master_index.py) and
records the source checksum, byte and line counts, content-derived section IDs,
source line ranges, and generator version. It copies no source prose and never
becomes a competing manually edited master.

## Completed import checks

1. The supplied source checksum was recalculated before transfer.
2. The source decoded as UTF-8 and matched the recorded line and byte counts.
3. A targeted sensitive-string scan found no private keys, service tokens,
   embedded base64 payloads, local user paths, or email addresses.
4. The unified source was copied without rewriting or regeneration.
5. The provenance manifest records the exact artifact identity and boundaries.
6. The deterministic retrieval index copies no source prose.

These checks do not validate every historical citation, URL, physical claim, or
Blender hypothesis inside the master. Its internal evidence labels remain
authoritative for those distinctions.
