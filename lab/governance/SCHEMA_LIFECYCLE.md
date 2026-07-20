# Schema lifecycle

VirtualAuto records must remain interpretable after schemas evolve. A schema
change is therefore a data migration decision, not only a validator edit.

## Version policy

- Every schema-backed record carries `schema_version`.
- Patch changes clarify validation without changing accepted record meaning.
- Minor changes may add optional fields or enum values while retaining old
  valid records.
- Major changes may alter meaning or required structure and require migration.
- Stable record IDs are never reassigned during migration.

## Change requirements

A pull request that changes a schema must include:

1. the reason and compatibility class;
2. updated executable examples;
3. migration code or an explicit statement that no migration is required;
4. fixtures for the oldest retained version affected;
5. validator coverage for both migrated and current records;
6. a record of fields whose meaning, units, or evidence status changed.

Historical records may remain on an old schema only when the repository retains
the matching schema and identifies the supported reader. Silent coercion is
prohibited.

## Deprecation

Deprecated fields remain readable for at least one minor schema cycle. Removal
requires a major version, a deterministic migration, and a repository-wide
search showing that no current records depend on the old field.
