# Blender scripts

Version-guarded automation, import forensics, builders, and regression tools.
Scripts must fail clearly when required APIs, nodes, or sockets are absent.

[`capture_runtime_manifest.py`](capture_runtime_manifest.py) is the first
reproducibility utility. It records conservative Blender runtime metadata
without mutating or rendering the scene. It remains **implementation code, not
locally observed Blender evidence**, until executed in Blender 5.0.1.
