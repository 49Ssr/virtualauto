# Binary asset policy

VirtualAuto keeps code, records, and small evidence in Git. Proprietary game
data, extracted resources, third-party vehicle meshes, raw captures, and private
working scenes stay in access-controlled storage outside this repository.

## Repository-owned Blender files

The default is a deterministic Python builder rather than a committed `.blend`.
If a repository-owned regression scene becomes necessary, it may live only
under `blender/assets/` or `tests/fixtures/blender/` and must:

- contain no extracted, proprietary, or externally licensed asset;
- be tracked through Git LFS, never as a raw Git blob;
- have an adjacent provenance record naming its builder, Blender version,
  checksum, rights state, and regeneration status;
- remain small enough to justify its review and storage cost.

All other `.blend`, mesh, package, texture, EXR, and video artifacts are rejected
by repository validation. Git LFS changes transport; it does not grant rights to
redistribute content.

## Private source registration

`virtualauto register-source` hashes a private file and writes a schema-checked
record. It stores an opaque custody label, not the private filesystem path, and
does not copy the source into the repository.
