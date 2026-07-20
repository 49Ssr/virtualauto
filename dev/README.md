# Development

Repository maintenance lives here so operator workflows remain uncluttered.

- [`scripts/`](scripts/) — deterministic index generation and repository validation
- [`tests/`](tests/README.md) — unit tests and lawful synthetic fixtures

Run the supported commands from the repository root:

```text
virtualauto build-index
virtualauto validate
python -m unittest discover -s dev/tests -v
```
