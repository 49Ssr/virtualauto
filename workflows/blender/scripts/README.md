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

[`audit_camera_pipeline.py`](audit_camera_pipeline.py) is a read-only render-state
gate. It compares a loaded scene with a machine-readable camera contract and
returns failure when a camera-specific lens or diffraction stage is being used
with the wrong camera, aperture, resolution, colour-management state, or node
configuration. It does not render or claim optical validation.
For generated Lensfun maps it also verifies the active image names, dimensions,
packed state, and exact float32 pixel hashes recorded in the contract.

[`build_lensfun_maps.py`](build_lensfun_maps.py) regenerates packed reverse
distortion/TCA/vignetting maps from the source-pinned equations and coefficients
in a camera contract. It deliberately does not wire nodes, save the file, or
promote the result; those remain separate review and qualification steps.

[`test_mapuv_identity.py`](test_mapuv_identity.py) is a tiny compositor
regression gate for generated coordinate maps. It proves which pixel-centre
encoding reproduces an identity mapping in the running Blender version and
fails if that invariant changes.

These scripts are Blender-hosted entrypoints called by `virtualauto
blender-smoke`; users do not need to hunt for and run them manually.
