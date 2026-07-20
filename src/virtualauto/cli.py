"""VirtualAuto command-line entry point."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from .assets import register_source_asset
from .blender_runner import run_smoke
from .doctor import diagnose
from .driveclub import build_driveclubfs, unpack_filesystem, write_listing_report
from .paths import repository_root


def run_repository_script(root: Path, name: str, strict: bool = False) -> int:
    environment = os.environ.copy()
    if strict:
        environment["VIRTUALAUTO_STRICT_VALIDATION"] = "1"
    return subprocess.run(
        [sys.executable, str(root / "scripts" / name)],
        cwd=root,
        env=environment,
        check=False,
    ).returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="virtualauto")
    subcommands = parser.add_subparsers(dest="command", required=True)

    validate = subcommands.add_parser("validate", help="validate the repository")
    validate.add_argument("--non-strict", action="store_true")

    subcommands.add_parser("build-index", help="regenerate the canonical master index")

    doctor = subcommands.add_parser("doctor", help="inspect local prerequisites")
    doctor.add_argument("--strict", action="store_true")

    register = subcommands.add_parser(
        "register-source", help="hash and register a private source asset"
    )
    register.add_argument("input")
    register.add_argument("--output", required=True)
    register.add_argument("--id", required=True)
    register.add_argument("--title", required=True)
    register.add_argument("--source-kind", required=True)
    register.add_argument("--format", required=True)
    register.add_argument("--provenance", required=True)
    register.add_argument("--rights-status", required=True)
    register.add_argument("--storage-reference", required=True)
    register.add_argument("--notes")
    register.add_argument("--overwrite", action="store_true")

    smoke = subcommands.add_parser(
        "blender-smoke", help="execute the Blender 5.0.1 structural smoke test"
    )
    smoke.add_argument(
        "--output-directory",
        default="evidence/runs/EXP-VA-BLENDER-SMOKE-001",
    )
    smoke.add_argument("--blender")
    smoke.add_argument("--overwrite", action="store_true")

    driveclub = subcommands.add_parser(
        "driveclub", help="operate the guarded DriveClub extraction workspace"
    )
    driveclub_commands = driveclub.add_subparsers(
        dest="driveclub_command", required=True
    )
    driveclub_commands.add_parser(
        "build", help="publish the pinned DriveClubFS submodule"
    )
    list_files = driveclub_commands.add_parser(
        "list", help="preflight and record the indexed filesystem"
    )
    list_files.add_argument(
        "--input",
        default="pipelines/driveclub/workspace/driveclubfs/input",
    )
    list_files.add_argument(
        "--output",
        default="pipelines/driveclub/workspace/driveclubfs/output/files.json",
    )
    unpack = driveclub_commands.add_parser(
        "unpack", help="preflight and unpack the indexed filesystem"
    )
    unpack.add_argument(
        "--input",
        default="pipelines/driveclub/workspace/driveclubfs/input",
    )
    unpack.add_argument(
        "--output",
        default="pipelines/driveclub/workspace/driveclubfs/output/filesystem",
    )
    unpack.add_argument(
        "--skip-checksum-verification",
        action="store_true",
        help="explicitly disable upstream MD5 checks; not recommended",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = repository_root()
    if args.command == "validate":
        return run_repository_script(
            root, "validate_repository.py", strict=not args.non_strict
        )
    if args.command == "build-index":
        return run_repository_script(root, "build_master_index.py")
    if args.command == "doctor":
        report = diagnose(root)
        print(json.dumps(report, indent=2))
        if args.strict:
            required = (
                report["git"]["available"],
                report["git_lfs"]["available"],
                report["baseline_blender_available"],
                report["canonical_master_available"],
                report["master_index_available"],
            )
            return 0 if all(required) else 1
        return 0
    if args.command == "register-source":
        record = register_source_asset(
            input_path=args.input,
            output_path=args.output,
            asset_id=args.id,
            title=args.title,
            source_kind=args.source_kind,
            format_name=args.format,
            provenance=args.provenance,
            rights_status=args.rights_status,
            storage_reference=args.storage_reference,
            notes=args.notes,
            overwrite=args.overwrite,
            root=root,
        )
        print(json.dumps(record, indent=2))
        return 0
    if args.command == "blender-smoke":
        outputs = run_smoke(
            output_directory=args.output_directory,
            blender_path=args.blender,
            root=root,
            overwrite=args.overwrite,
        )
        print(
            json.dumps(
                {key: str(value.relative_to(root)) for key, value in outputs.items()},
                indent=2,
            )
        )
        return 0
    if args.command == "driveclub":
        try:
            if args.driveclub_command == "build":
                artifact = build_driveclubfs(root)
                print(
                    json.dumps({"artifact": str(artifact.relative_to(root))}, indent=2)
                )
                return 0
            if args.driveclub_command == "list":
                report = write_listing_report(
                    input_directory=args.input,
                    output=args.output,
                    root=root,
                )
                print(
                    json.dumps(
                        {
                            "entry_count": report["entry_count"],
                            "output": str(Path(args.output)),
                        },
                        indent=2,
                    )
                )
                return 0
            if args.driveclub_command == "unpack":
                manifest = unpack_filesystem(
                    input_directory=args.input,
                    output_directory=args.output,
                    skip_checksum_verify=args.skip_checksum_verification,
                    root=root,
                )
                print(json.dumps(manifest, indent=2))
                return 0
            raise AssertionError(
                f"Unhandled DriveClub command: {args.driveclub_command}"
            )
        except (OSError, ValueError, RuntimeError) as error:
            print(f"DriveClub operation failed: {error}", file=sys.stderr)
            return 2
    raise AssertionError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
