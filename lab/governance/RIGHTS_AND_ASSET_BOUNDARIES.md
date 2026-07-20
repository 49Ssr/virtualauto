# Rights and asset boundaries

VirtualAuto documents tools and workflows for assets the operator is legally
entitled to access. The repository is not a distribution channel for game data,
third-party models, textures, package keys, bypass material, or confidential OEM
information.

## Never commit

- console or game package files;
- decrypted or extracted game resources;
- third-party vehicle models and textures without redistribution permission;
- private reference photography without consent;
- credentials, keys, tokens, licences, or account data;
- local caches, package databases, or workstation metadata;
- copyrighted documents copied in full when a citation or private reference is
  sufficient.

The `.gitignore` is a guardrail, not authorization. Review staged files and
history before every push.

## What may be committed

- VirtualAuto-owned source code and documentation;
- exact external repository links, commits, and license observations;
- schemas and fictionalized examples;
- small original diagnostic assets;
- checksums, byte sizes, transformation logs, and manifests that do not expose
  restricted content;
- lawful excerpts within applicable quotation limits;
- original Blender test scenes after an explicit binary-storage decision.

## Private storage records

A source-asset manifest may point to private storage without exposing a public
URL. Record:

- stable asset ID;
- provenance and custody state;
- rights status;
- checksum and byte size when available;
- immutable source versus derived output;
- transformations and tool revisions;
- whether the source is currently available.

Do not put access credentials or decryption material in manifests.

## External code

An external repository's software licence applies to its code, not to game
assets processed by that code. A permissive tool licence does not grant rights
to redistribute extracted meshes, textures, audio, or package contents.

Record license anomalies rather than resolving them by assumption. Unlicensed
or unclear repositories remain research references until permission is
clarified.

## Evidence and publication

Reference-only evidence can support a private observation record but should not
be copied into Git. Prefer a checksum, private locator, lawful thumbnail, or
textual measurement. Before publishing derived imagery or models, separately
review the source rights, transformation, amount used, and intended audience.

## Removal and incident response

If restricted material is committed:

1. stop further pushes and record the affected commit;
2. remove the file from the active branch;
3. assess whether Git history must be rewritten;
4. rotate any exposed credential immediately;
5. document the remediation without reproducing the sensitive content.

A deleted file can remain in Git history. Normal deletion is not sufficient for
secrets or prohibited source assets.
