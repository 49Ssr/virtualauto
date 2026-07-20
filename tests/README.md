# Tests

The standard-library test suite checks deterministic master generation,
repository policy, schema integrity, and private-source registration. Blender
tests are intentionally separate because the pinned 5.0.1 runtime is too large
for ordinary CI.

Run from a fresh checkout with:

```text
python -m pip install -e .
python -m unittest discover -s tests -v
```
