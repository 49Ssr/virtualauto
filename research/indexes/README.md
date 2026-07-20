# Generated retrieval views

Files here are deterministic navigation aids generated from canonical sources.
They are never edited manually and never outrank the source artifact.

`automotive_master.index.json` is regenerated with:

```bash
python dev/scripts/build_master_index.py
```

The generator first verifies the canonical master's SHA-256, byte size, UTF-8
decoding, and line count. Each indexed section records its parent ID, source
line range, deterministic retrieval key, optional canonical topic key, and a
hierarchy-derived ID. Retrieval keys are repository search aids, not a claim of
exact GitHub anchor generation. The compact JSON avoids duplicating the full
heading path thousands of times.

Use the CLI instead of feeding the complete append-only master into a prompt:

```text
virtualauto research find weave --prefix ABR-COMP
virtualauto research get ABR-COMP-010
```

Search defaults to canonical-keyed sections, excluding untagged legacy headings.
`get` returns the complete exact line range plus source checksum.
