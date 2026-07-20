# Private conversion workspaces

VirtualAuto does not track operating workspaces in Git. Create one outside the
checkout for each independent conversion or investigation:

```text
virtualauto workspace init D:\VirtualAutoWorkspace --run-id dc-f40-001
```

The command creates:

```text
runs/dc-f40-001/
  workspace.json
  pkgtoolbox/input/  pkgtoolbox/output/
  shadpkg/input/     shadpkg/output/
  driveclubfs/input/ driveclubfs/output/
  rpk/input/         rpk/output/
  blender/input/     blender/output/
```

Each run is immutable by identity: creating the same run twice fails instead of
reusing stale output. VirtualAuto does not delete a completed run automatically;
reverse-engineering outputs can be expensive and may contain unknown evidence.
Delete or archive them only after reviewing their manifests and custody needs.

Commands require explicit input and output paths. This prevents concurrent runs
from overwriting each other and prevents a checkout from becoming an accidental
asset store. A stage may pass a validated output path directly to the next tool;
the directory boundaries do not mandate redundant copying.
