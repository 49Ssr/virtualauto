# VirtualAuto

Blender tools and practical research for automotive materials, rendering and
game-asset reconstruction.

VirtualAuto brings the reusable parts of our vehicle and environment work into
one place: material references, Blender diagnostics, camera tools, extraction
utilities and a modified Continuum Flow build. The aim is an editable scene and
a convincing render, with clear controls and a manageable cost.

## Start with the job

| I want to… | Start here | What is available |
| --- | --- | --- |
| Simulate fire and smoke on the GPU | [Continuum Flow](external/ContinuumFlow.md) | Patched Windows add-on build, installation instructions and actual Blender/OpenCL checks |
| Connect to an open Blender scene | [Blender MCP](workflows/blender/mcp/README.md) | Connector setup and live-operation workflow |
| Inspect a mesh or imported vehicle | [Blender tools](workflows/blender/README.md) | Read-only inventory script and development sidebar add-on |
| Work on paint, glass, carbon, metal or lamps | [Material reference](research/automotive_materials/README.md) | Automotive material research and searchable source sections |
| Check camera and compositor settings | [Camera scripts](workflows/blender/scripts/README.md) | Camera-state audit, Lensfun map generation and compositor coordinate checks |
| Build the environment around a car | [Environment workflow](workflows/environment/README.md) | Lighting, sky, atmosphere, ground and reflection guidance |
| Investigate DriveClub assets | [DriveClub runbook](workflows/driveclub/RUNBOOK.md) | Package inspection, filesystem tools and the F40 research status |

## Continuum Flow development build

The VirtualAuto variant keeps Continuum's existing nodes and solver. It fixes
preview-buffer reallocation, allows appearance adjustments during a bake,
aligns VDB sequences with the requested timeline start and bounds the number of
exported frames.

```text
virtualauto continuum build
virtualauto continuum check --blender "C:\path\to\blender.exe"
```

The Windows ZIP has been installed and tested in Blender **5.2.3 LTS** on an
**RTX 5090 Laptop GPU**. See the [build record](external/ContinuumFlow.md) for
the measured results and installation steps. These are small simulation checks,
not a benchmark against other solvers or a production car-fire qualification.
Installing the add-on does not convert an existing Mantaflow scene.

The source patch is available here. A public binary release is pending the
upstream native VDB writer's source and redistribution details.

## Install the command-line tools

Use Python **3.12 or newer** from a checkout of this repository:

```text
python -m pip install -e .
virtualauto --help
virtualauto doctor
```

Blender is needed for Blender operations; it is not required to read the
research or run the ordinary repository tools. Set `VIRTUALAUTO_BLENDER` to
your Blender executable when using the structural Blender test. That original
test targets 5.0.1 and checks scene structure; it is not a smoke/fluid simulation.
Compatibility is recorded per workflow rather than treating one Blender
version as proof that every tool works.

For material research, retrieve the relevant section instead of reading the
whole master:

```text
virtualauto research find weave --prefix ABR-COMP
virtualauto research get ABR-COMP-010
```

DriveClub extraction additionally uses Git submodules and .NET 9. Follow its
runbook for those dependencies and the private asset workspace.

## Where the project stands

- **Blender:** inventory, camera/compositor diagnostics and the Continuum
  development build are executable tools. Their individual records state what
  was tested. The sidebar add-on currently provides mesh inventory, not a
  complete vehicle or material editor.
- **NFS Rivals:** material, glass, lamp and wet-road work has been developed in
  individual scenes. The older local project branch still needs consolidation
  before those scripts can be presented here as reusable tools.
- **DriveClub:** package and filesystem inspection are implemented. F40
  source reconstruction is still research; see the [project status](research/projects/driveclub_f40/STATUS.md).
  Its private Blender camera work and earlier 5.0.1 tests remain dated records,
  not a blanket compatibility claim for the current tools.
- **Materials and environments:** the references support scene decisions;
  they are not a collection of finished, automatically calibrated presets.

Blender work should preserve source meshes and UVs, use plainly labelled native
controls, and be checked in the intended shot. Add groups, helpers and extra
geometry when they solve a concrete problem.

## Repository map

| Folder | Contents |
| --- | --- |
| [research/](research/README.md) | Materials, rendering, environments, source-format research and project records |
| [workflows/](workflows/README.md) | Blender scripts, add-on source and practical operating instructions |
| [src/virtualauto/](src/virtualauto/) | Command-line tools and build orchestration |
| [external/](external/README.md) | Third-party tool versions, patches, build instructions and licences |
| [dev/](dev/README.md) | Tests and repository maintenance |
| [lab/](lab/README.md) | Experiments, schemas and supporting records |

Generated installers and build files go in ignored `dist/` and `build/`
directories. Private models, textures, game packages, scenes and caches stay
outside the published source.

## Development

```text
virtualauto validate
python -m unittest discover -s dev/tests -v
```

The repository checks cover links, manifests and code behaviour. Visual quality
and material accuracy still require Blender tests and judgement.

See [contributing](CONTRIBUTING.md) and [licensing](lab/governance/LICENSING_STATUS.md)
for changes and reuse. Third-party components retain their own licences;
VirtualAuto has not selected a repository-wide open-source licence.
