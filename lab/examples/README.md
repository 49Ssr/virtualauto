# Validated examples

These records exercise VirtualAuto's schemas and cross-reference rules without
containing proprietary assets. The core example graph describes a fictionalized
DriveClub F40 UV-forensics experiment and is example data only, not evidence
that any extraction or Blender reconstruction has been completed.

`blender_run.json` separately demonstrates the runtime-manifest schema. Its
values are explicitly fictional documentation and are not execution evidence.

`environment_profile.json` demonstrates environment ownership and uncertainty:
most physical and implementation values remain unresolved. It is useful for
research specification, not as a quick build recipe.

`environment_profile_f40_glass_starter.json` demonstrates the complementary
practical case: a `P2-buildable` Level 0 corridor with explicit values labelled
`implementation-default`. Those values are deterministic test inputs, not
measurements, physical calibration, DriveClub recovery, or evidence from the
private F40 model.

The repository validator treats these files as executable documentation: schema
or reference changes that invalidate them must be deliberate.