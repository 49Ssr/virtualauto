# Blender scripts

Version-guarded automation, import forensics, builders, and regression tools.
Scripts must fail clearly when required APIs, nodes, or sockets are absent.

[`capture_runtime_manifest.py`](capture_runtime_manifest.py) is the first
reproducibility utility. It records conservative Blender runtime metadata
without mutating or rendering the scene.

[`asset_inventory.py`](asset_inventory.py) captures structural scene evidence.
[`create_smoke_scene.py`](create_smoke_scene.py) builds the original synthetic
fixture. [`test_addon.py`](test_addon.py) registers the development add-on and
executes its export operator. [`test_tangent_frame.py`](test_tangent_frame.py)
checks the first automotive-math invariant in Blender's own `mathutils` backend.

These scripts are Blender-hosted entrypoints called by `virtualauto
blender-smoke`; users do not need to hunt for and run them manually.
