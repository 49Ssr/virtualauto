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
from .driveclub import (
    build_driveclubfs,
    inspect_indexed_filesystem,
    unpack_filesystem,
    write_listing_report,
)
from .evidence import ARTIFACT_TYPES, RIGHTS_STATUSES, record_evidence
from .paths import repository_root
from .pkg import (
    assemble_fragments,
    extract_outer_entries,
    inspect_fragments,
    list_pkg_entries,
)
from .research import find_sections, get_section
from .workspace import initialise_workspace


def run_repository_script(root: Path, name: str, strict: bool = False) -> int:
    environment = os.environ.copy()
    if strict:
        environment["VIRTUALAUTO_STRICT_VALIDATION"] = "1"
    return subprocess.run(
        [sys.executable, str(root / "dev/scripts" / name)],
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

    evidence = subcommands.add_parser(
        "record-evidence",
        help="hash a retained artifact and create its evidence record",
    )
    evidence.add_argument("artifact")
    evidence.add_argument("--id", required=True)
    evidence.add_argument("--experiment-id")
    evidence.add_argument(
        "--artifact-type", choices=sorted(ARTIFACT_TYPES), required=True
    )
    evidence.add_argument("--provenance", required=True)
    evidence.add_argument(
        "--rights-status", choices=sorted(RIGHTS_STATUSES), required=True
    )
    evidence.add_argument("--output")
    evidence.add_argument("--blender-version")
    evidence.add_argument("--render-engine")
    evidence.add_argument("--scene-revision")
    evidence.add_argument("--retention-note")
    evidence.add_argument("--overwrite", action="store_true")

    smoke = subcommands.add_parser(
        "blender-smoke", help="execute the Blender 5.0.1 structural smoke test"
    )
    smoke.add_argument(
        "--output-directory",
        default="tmp/blender-smoke",
    )
    smoke.add_argument("--blender")
    smoke.add_argument("--overwrite", action="store_true")

    workspace = subcommands.add_parser(
        "workspace", help="create a private run workspace outside Git"
    )
    workspace_commands = workspace.add_subparsers(
        dest="workspace_command", required=True
    )
    initialise = workspace_commands.add_parser(
        "init", help="create isolated per-utility input/output boundaries"
    )
    initialise.add_argument("directory")
    initialise.add_argument("--run-id", required=True)

    package = subcommands.add_parser(
        "pkg", help="inspect or assemble byte-split PS4 PKG containers"
    )
    package_commands = package.add_subparsers(dest="pkg_command", required=True)
    inspect = package_commands.add_parser(
        "inspect", help="validate fragment structure and read public metadata"
    )
    inspect.add_argument("--input", required=True)
    inspect.add_argument("--output")
    inspect.add_argument(
        "--hash-fragments",
        action="store_true",
        help="compute full local SHA-256 hashes without assembling",
    )
    assemble = package_commands.add_parser(
        "assemble", help="stream validated fragments into a new PKG"
    )
    assemble.add_argument("--input", required=True)
    assemble.add_argument("--output", required=True)
    entries = package_commands.add_parser(
        "entries", help="list the public outer entry table of one assembled PKG"
    )
    entries.add_argument("--input", required=True)
    extract_outer = package_commands.add_parser(
        "extract-outer",
        help="copy only unencrypted outer PKG entries to a fresh directory",
    )
    extract_outer.add_argument("--input", required=True)
    extract_outer.add_argument("--output", required=True)

    research = subcommands.add_parser(
        "research", help="retrieve exact sections from the canonical master"
    )
    research_commands = research.add_subparsers(dest="research_command", required=True)
    get = research_commands.add_parser(
        "get", help="print one complete section by canonical or index ID"
    )
    get.add_argument("identifier")
    find = research_commands.add_parser(
        "find", help="find canonical section headings without legacy noise"
    )
    find.add_argument("query")
    find.add_argument("--prefix")
    find.add_argument("--limit", type=int, default=20)
    find.add_argument("--include-untagged", action="store_true")

    driveclub = subcommands.add_parser(
        "driveclub", help="operate the guarded DriveClub extraction workspace"
    )
    driveclub_commands = driveclub.add_subparsers(
        dest="driveclub_command", required=True
    )
    driveclub_commands.add_parser(
        "build", help="publish the pinned DriveClubFS submodule"
    )
    inspect_filesystem = driveclub_commands.add_parser(
        "inspect", help="classify an indexed filesystem before decompression"
    )
    inspect_filesystem.add_argument("--input", required=True)
    inspect_filesystem.add_argument("--output")
    list_files = driveclub_commands.add_parser(
        "list", help="preflight and record the indexed filesystem"
    )
    list_files.add_argument(
        "--input",
        required=True,
    )
    list_files.add_argument(
        "--output",
        required=True,
    )
    unpack = driveclub_commands.add_parser(
        "unpack", help="preflight and unpack the indexed filesystem"
    )
    unpack.add_argument(
        "--input",
        required=True,
    )
    unpack.add_argument(
        "--output",
        required=True,
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
    if args.command == "record-evidence":
        try:
            record = record_evidence(
                artifact=args.artifact,
                evidence_id=args.id,
                experiment_id=args.experiment_id,
                artifact_type=args.artifact_type,
                provenance=args.provenance,
                rights_status=args.rights_status,
                output=args.output,
                blender_version=args.blender_version,
                render_engine=args.render_engine,
                scene_revision=args.scene_revision,
                retention_note=args.retention_note,
                overwrite=args.overwrite,
                root=root,
            )
        except (OSError, ValueError) as error:
            print(f"Evidence recording failed: {error}", file=sys.stderr)
            return 2
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
    if args.command == "workspace":
        if args.workspace_command == "init":
            try:
                manifest = initialise_workspace(
                    args.directory,
                    run_id=args.run_id,
                    repository=root,
                )
            except (OSError, ValueError) as error:
                print(f"Workspace creation failed: {error}", file=sys.stderr)
                return 2
            print(json.dumps(manifest, indent=2))
            return 0
        raise AssertionError(f"Unhandled workspace command: {args.workspace_command}")
    if args.command == "pkg":
        try:
            if args.pkg_command == "inspect":
                report = inspect_fragments(
                    args.input, hash_fragments=args.hash_fragments
                )
                if args.output:
                    destination = Path(args.output).expanduser().resolve()
                    if destination.exists():
                        raise ValueError(
                            f"Refusing to overwrite existing report: {destination}"
                        )
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_text(
                        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8",
                        newline="\n",
                    )
                print(json.dumps(report, indent=2, ensure_ascii=False))
                return 0
            if args.pkg_command == "assemble":
                manifest = assemble_fragments(args.input, args.output)
                print(json.dumps(manifest, indent=2, ensure_ascii=False))
                return 0
            if args.pkg_command == "entries":
                report = list_pkg_entries(args.input)
                print(json.dumps(report, indent=2, ensure_ascii=False))
                return 0
            if args.pkg_command == "extract-outer":
                manifest = extract_outer_entries(args.input, args.output)
                print(json.dumps(manifest, indent=2, ensure_ascii=False))
                return 0
            raise AssertionError(f"Unhandled PKG command: {args.pkg_command}")
        except (OSError, ValueError) as error:
            print(f"PKG operation failed: {error}", file=sys.stderr)
            return 2
    if args.command == "research":
        try:
            if args.research_command == "get":
                result = get_section(args.identifier, root)
                metadata = {
                    "source_path": result["source_path"],
                    "source_sha256": result["source_sha256"],
                    "section": result["section"],
                }
                print(json.dumps(metadata, indent=2))
                print("\n--- canonical section ---\n")
                print(result["content"])
                return 0
            if args.research_command == "find":
                results = find_sections(
                    args.query,
                    prefix=args.prefix,
                    include_untagged=args.include_untagged,
                    limit=args.limit,
                    root=root,
                )
                print(json.dumps(results, indent=2))
                return 0
        except (OSError, ValueError) as error:
            print(f"Research retrieval failed: {error}", file=sys.stderr)
            return 2
        raise AssertionError(f"Unhandled research command: {args.research_command}")
    if args.command == "driveclub":
        try:
            if args.driveclub_command == "build":
                artifact = build_driveclubfs(root)
                print(
                    json.dumps({"artifact": str(artifact.relative_to(root))}, indent=2)
                )
                return 0
            if args.driveclub_command == "inspect":
                report = inspect_indexed_filesystem(args.input, root)
                if args.output:
                    destination = Path(args.output).expanduser().resolve()
                    if destination.exists():
                        raise ValueError(
                            f"Refusing to overwrite existing report: {destination}"
                        )
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_text(
                        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8",
                        newline="\n",
                    )
                    summary = {
                        "status": report["status"],
                        "report": str(destination),
                        "active_entry_count": report["index"]["active_entry_count"],
                        "present_dat_file_count": report["present_dat_file_count"],
                        "zero_data_marker_count": report["zero_data_marker_count"],
                        "active_entries_touching_zero_chunks": report[
                            "active_entries_touching_zero_chunks"
                        ],
                        "warnings": report["warnings"],
                    }
                    print(json.dumps(summary, indent=2, ensure_ascii=False))
                else:
                    print(json.dumps(report, indent=2, ensure_ascii=False))
                return 0 if report["status"] == "complete_for_index" else 3
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
