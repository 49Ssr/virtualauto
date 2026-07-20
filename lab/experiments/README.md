# Experiments

Experiments convert sourced knowledge or hypotheses into reproducible evidence.

## Lifecycle

`planned -> active -> accepted | rejected | blocked | superseded`

Rejection is a recorded result, not a deletion. Copy
[`TEMPLATE.md`](TEMPLATE.md) for the human-readable plan and create a manifest
that validates against [`experiment.schema.json`](../schemas/experiment.schema.json).

Evidence records validate against [`evidence.schema.json`](../schemas/evidence.schema.json),
and observations validate against [`observation.schema.json`](../schemas/observation.schema.json).

Do not commit copyrighted source assets, extracted game data, or unlicensed
third-party material as evidence.
