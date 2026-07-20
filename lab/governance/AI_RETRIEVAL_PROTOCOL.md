# AI retrieval protocol

VirtualAuto is designed to be queried by humans and retrieval-based assistants
without allowing search convenience to erase evidence state.

## Query order

1. Resolve exact stable IDs when the request contains one.
2. Read the domain index and the complete relevant record, not a search snippet
   alone.
3. Follow source, evidence, experiment, supersession, and contradiction links.
4. Prefer the newest non-superseded record that matches the requested Blender
   version, asset revision, engine, market, and physical state.
5. Return unresolved boundaries with the answer.

## Required answer distinctions

An assistant must distinguish:

- **observed**: directly recorded from a retained artifact;
- **sourced**: supported by an identified external source;
- **hypothesis**: plausible but unverified;
- **implemented**: constructed in code or Blender;
- **observed in Blender**: rendered or executed under a declared setup;
- **production qualified**: passed still, motion, performance, fresh-file, and
  target-asset checks;
- **rejected or superseded**: retained for provenance but not current doctrine.

Code availability, a forum report, or a node diagram is not execution evidence.
A pinned external commit is not proof that VirtualAuto reproduced its output.

## Retrieval-friendly writing

Technical records should include:

- stable ID and unambiguous title;
- explicit scope and material or format family;
- Blender version and engine where applicable;
- direct dependencies and owned parameters;
- known failure signatures;
- source and evidence IDs;
- status, confidence, and boundaries;
- useful synonyms without keyword stuffing.

Keep decisive context in the same record as the claim. Do not place a critical
limitation only in a distant appendix.

## Canonical and generated knowledge

The unified automotive master remains authoritative. Generated domain files are
retrieval views and must carry the source checksum, section ID, line range, and
generator version. Git supplies the commit identity of both source and index.
When a generated view and canonical source disagree, stop and report the
integrity failure rather than selecting whichever text is more convenient.

The current deterministic heading index is
[`research/indexes/automotive_master.index.json`](../../research/indexes/automotive_master.index.json).
Resolve a section there, then read the complete recorded line range from the
canonical master. A heading match alone is not enough context for a technical
decision.

For routine work, use `virtualauto research find` and `virtualauto research get`.
The default search excludes untagged historical headings and returns canonical
topic keys such as `CP12-*`, `ABR-*`, and `ABR5-*`. This is a retrieval filter,
not deletion: the complete append-only source remains authoritative, and
`--include-untagged` is available for historical audits.

## Repository-wide audit requests

A request such as "prove the whole repository has no contradictions" cannot be
satisfied by semantic search alone. Perform an iterative audit with:

- a fixed commit;
- complete file inventory;
- deterministic validation;
- domain-by-domain reading;
- external source verification;
- an audit ledger recording covered ranges and unresolved items.

Absence of a retrieved contradiction is not proof that none exists.

## Prompt contract for technical agents

A technical agent working from VirtualAuto should be instructed to:

1. cite repository paths and stable IDs;
2. state the commit or branch examined;
3. inspect exact Blender 5.0.1 sockets at runtime before graph mutation;
4. preserve raw and unknown source data;
5. avoid inventing unavailable OEM, game-format, optical, or manufacturing
   constants;
6. create the smallest falsifiable experiment before expanding a system;
7. write conclusions back as records with evidence links rather than prose-only
   chat memory.

## Search examples

High-reliability requests:

```text
Retrieve NODE-DC-UV-DIAGNOSTIC-001 and every linked experiment.
Show unresolved UNK records for the DriveClub F40 target.
Find claims about clearcoat that are validated in Blender 5.0.1.
List transformations that used EXT-DRIVECLUBFS and their loss assessments.
```

Low-reliability requests that require decomposition:

```text
Read everything and find every mistake.
Tell me the definitive DriveClub material format.
Generate a production shader from all current research.
```
