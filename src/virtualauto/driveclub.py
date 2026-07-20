"""Guarded orchestration for the pinned DriveClubFS research instrument."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import subprocess
import tempfile
import unicodedata
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

from .assets import atomic_json_write
from .paths import repository_root

DRIVECLUBFS_COMMIT = "836d5f09677dd7f30b92991a0f32e029487ae5cd"
LISTING_PATTERN = re.compile(
    r"^(?P<name>.+) \((?P<size>\d+) bytes, Dat Index: (?P<dat>\d+), "
    r"Offset: 0x(?P<offset>[0-9A-Fa-f]+)\)$"
)
WINDOWS_INVALID = re.compile(r"[<>:\"|?*]")
WINDOWS_RESERVED = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def submodule_path(root: Path) -> Path:
    return root / "external/vendor/DriveClubFS"


def resolve_user_path(value: str | Path, root: Path) -> Path:
    path = Path(value).expanduser()
    return (path if path.is_absolute() else root / path).resolve()


def verify_submodule(root: Path) -> Path:
    path = submodule_path(root)
    project = path / "DriveClubFS/DriveClubFS.csproj"
    if not project.is_file():
        raise ValueError(
            "DriveClubFS submodule is unavailable; run "
            "`git submodule update --init --recursive`"
        )
    result = subprocess.run(
        ["git", "-C", str(path), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    actual = result.stdout.strip()
    if result.returncode != 0 or actual != DRIVECLUBFS_COMMIT:
        raise ValueError(
            f"DriveClubFS pin mismatch: expected {DRIVECLUBFS_COMMIT}, got {actual!r}"
        )
    return project


def find_dotnet() -> Path:
    configured = os.environ.get("VIRTUALAUTO_DOTNET")
    candidate = configured or shutil.which("dotnet")
    if not candidate or not Path(candidate).is_file():
        raise ValueError(
            ".NET SDK 9 is required. Install it or set VIRTUALAUTO_DOTNET to dotnet."
        )
    return Path(candidate).resolve()


def require_dotnet_9_sdk(dotnet: Path, root: Path) -> None:
    result = subprocess.run(
        [str(dotnet), "--list-sdks"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    versions = [line.split()[0] for line in result.stdout.splitlines() if line.strip()]
    if result.returncode != 0 or not any(
        version.startswith("9.") for version in versions
    ):
        raise ValueError(
            ".NET SDK 9 is not available. Runtime installations alone cannot build "
            "the pinned DriveClubFS project."
        )


def build_driveclubfs(root: Path | None = None) -> Path:
    root = root or repository_root()
    project = verify_submodule(root)
    dotnet = find_dotnet()
    require_dotnet_9_sdk(dotnet, root)
    output = root / "build/external/DriveClubFS"
    output.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [
            str(dotnet),
            "publish",
            str(project),
            "--configuration",
            "Release",
            "--no-self-contained",
            "--output",
            str(output),
        ],
        cwd=root,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"DriveClubFS build failed with exit code {result.returncode}"
        )
    dll = output / "DriveClubFS.dll"
    if dll.is_file():
        return dll
    binary = output / ("DriveClubFS.exe" if os.name == "nt" else "DriveClubFS")
    if binary.is_file():
        return binary
    raise RuntimeError("DriveClubFS build completed but no runnable artifact was found")


def find_driveclubfs(root: Path) -> tuple[Path, list[str]]:
    configured = os.environ.get("VIRTUALAUTO_DRIVECLUBFS")
    candidates = [Path(configured).expanduser()] if configured else []
    candidates.extend(
        (
            root / "build/external/DriveClubFS/DriveClubFS.dll",
            root / "build/external/DriveClubFS/DriveClubFS.exe",
            root / "build/external/DriveClubFS/DriveClubFS",
        )
    )
    for candidate in candidates:
        if not candidate.is_file():
            continue
        candidate = candidate.resolve()
        if candidate.suffix.lower() == ".dll":
            return candidate, [str(find_dotnet()), str(candidate)]
        return candidate, [str(candidate)]
    raise ValueError("DriveClubFS is not built; run `virtualauto driveclub build`")


def validate_filesystem_input(
    input_directory: str | Path, root: Path | None = None
) -> Path:
    root = root or repository_root()
    directory = resolve_user_path(input_directory, root)
    if not directory.is_dir():
        raise ValueError(f"DriveClub filesystem input is not a directory: {directory}")
    if (
        not (directory / "game.ndx").is_file()
        and not (directory / "game.dat").is_file()
    ):
        raise ValueError(
            "Input must contain game.ndx or an older embedded-index game.dat"
        )
    if (directory / "game.ndx").is_file() and not list(directory.glob("game*.dat")):
        raise ValueError("game.ndx is present but no game*.dat files were found")
    return directory


def safe_internal_name(name: str) -> str:
    if "\\" in name:
        raise ValueError(f"DriveClub entry uses an ambiguous path separator: {name!r}")
    normalized = name
    if (
        not normalized
        or normalized.startswith("/")
        or re.match(r"^[A-Za-z]:", normalized)
    ):
        raise ValueError(f"Unsafe absolute DriveClub entry path: {name!r}")
    path = PurePosixPath(normalized)
    if any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError(f"Unsafe DriveClub entry path component: {name!r}")
    for part in path.parts:
        if WINDOWS_INVALID.search(part) or part.endswith((" ", ".")):
            raise ValueError(f"DriveClub entry is not portable to Windows: {name!r}")
        stem = part.split(".", 1)[0].upper()
        if stem in WINDOWS_RESERVED:
            raise ValueError(f"DriveClub entry uses a reserved Windows name: {name!r}")
    return path.as_posix()


def parse_listing(text: str) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    seen: dict[str, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        match = LISTING_PATTERN.fullmatch(line)
        if not match:
            raise ValueError(
                f"Unrecognized DriveClubFS listing line {line_number}: {line!r}"
            )
        name = safe_internal_name(match.group("name"))
        collision_key = unicodedata.normalize("NFC", name).casefold()
        if collision_key in seen:
            raise ValueError(
                "Case-insensitive output collision: "
                f"{seen[collision_key]!r} and {name!r}"
            )
        seen[collision_key] = name
        entries.append(
            {
                "path": name,
                "size": int(match.group("size")),
                "dat_index": int(match.group("dat")),
                "offset": int(match.group("offset"), 16),
            }
        )
    if not entries:
        raise ValueError("DriveClubFS produced an empty file listing")
    return entries


def validate_required_dat_files(
    directory: Path, entries: list[dict[str, object]]
) -> None:
    if not (directory / "game.ndx").is_file():
        return
    missing = sorted(
        {
            f"game{int(entry['dat_index']):03}.dat"
            for entry in entries
            if not (directory / f"game{int(entry['dat_index']):03}.dat").is_file()
        }
    )
    if missing:
        raise ValueError("Indexed data files are missing: " + ", ".join(missing[:20]))


def verify_extracted_files(output: Path, entries: list[dict[str, object]]) -> list[str]:
    failures: list[str] = []
    for entry in entries:
        target = (output / str(entry["path"])).resolve()
        try:
            target.relative_to(output)
        except ValueError as error:
            raise AssertionError(
                "Preflight path escaped during verification"
            ) from error
        if not target.is_file():
            failures.append(f"missing:{entry['path']}")
        elif target.stat().st_size != entry["size"]:
            failures.append(
                f"size:{entry['path']}:{target.stat().st_size}!={entry['size']}"
            )
    expected = {str(entry["path"]) for entry in entries}
    actual = {
        path.relative_to(output).as_posix()
        for path in output.rglob("*")
        if path.is_file()
    }
    failures.extend(f"unexpected:{path}" for path in sorted(actual - expected))
    return failures


def require_separate_trees(source: Path, output: Path) -> None:
    for parent, child in ((source, output), (output, source)):
        try:
            child.relative_to(parent)
        except ValueError:
            continue
        raise ValueError(
            f"DriveClub input and output trees must not overlap: {source} and {output}"
        )


def run_listing(
    input_directory: str | Path, root: Path | None = None
) -> tuple[list[dict[str, object]], str]:
    root = root or repository_root()
    directory = validate_filesystem_input(input_directory, root)
    _, command = find_driveclubfs(root)
    with tempfile.TemporaryDirectory(prefix="virtualauto-driveclub-list-") as temporary:
        result = subprocess.run(
            [*command, "listfiles", "--input", str(directory)],
            cwd=temporary,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"DriveClubFS listfiles failed ({result.returncode}):\n"
                f"{result.stdout}\n{result.stderr}"
            )
        listing_path = Path(temporary) / "files.txt"
        if not listing_path.is_file():
            raise RuntimeError(
                "DriveClubFS returned success without creating files.txt"
            )
        entries = parse_listing(listing_path.read_text(encoding="utf-8-sig"))
        validate_required_dat_files(directory, entries)
    return entries, (result.stdout + result.stderr)


def write_listing_report(
    *, input_directory: str | Path, output: str | Path, root: Path | None = None
) -> dict[str, object]:
    root = root or repository_root()
    directory = validate_filesystem_input(input_directory, root)
    entries, log = run_listing(directory, root)
    output_path = resolve_user_path(output, root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        raise ValueError(f"Listing report already exists: {output_path}")
    report = {
        "schema_version": "1.0.0",
        "tool": "DriveClubFS",
        "tool_commit": DRIVECLUBFS_COMMIT,
        "captured_at": datetime.now(UTC).isoformat(),
        "input_label": directory.name,
        "entry_count": len(entries),
        "entries": entries,
        "log": log,
        "scope": "preflight listing; no payload extraction or semantic decoding",
    }
    atomic_json_write(output_path, report)
    return report


def input_manifest(directory: Path) -> list[dict[str, object]]:
    candidates = sorted(path for path in directory.glob("game*.dat") if path.is_file())
    index = directory / "game.ndx"
    if index.is_file():
        candidates.insert(0, index)
    return [
        {
            "name": path.name,
            "byte_size": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path in candidates
    ]


def unpack_filesystem(
    *,
    input_directory: str | Path,
    output_directory: str | Path,
    skip_checksum_verify: bool = False,
    root: Path | None = None,
) -> dict[str, object]:
    root = root or repository_root()
    source = validate_filesystem_input(input_directory, root)
    output = resolve_user_path(output_directory, root)
    require_separate_trees(source, output)
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"Extraction output must be absent or empty: {output}")
    output.mkdir(parents=True, exist_ok=True)

    entries, listing_log = run_listing(source, root)
    expected_output_bytes = sum(int(entry["size"]) for entry in entries)
    free_bytes_before = shutil.disk_usage(output).free
    if free_bytes_before < expected_output_bytes:
        raise ValueError(
            "Insufficient free space for the listed payload: "
            f"need {expected_output_bytes} bytes, have {free_bytes_before} bytes"
        )
    source_manifest = input_manifest(source)
    _, command = find_driveclubfs(root)
    started = datetime.now(UTC)
    arguments = [
        *command,
        "unpack-all",
        "--input",
        str(source),
        "--output",
        str(output),
    ]
    if skip_checksum_verify:
        arguments.append("--skip-verifying-checksum")
    result = subprocess.run(
        arguments,
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    verification_failures = (
        verify_extracted_files(output, entries) if result.returncode == 0 else []
    )
    metadata = output / "_virtualauto"
    metadata.mkdir(parents=True, exist_ok=True)
    (metadata / "driveclubfs.txt").write_text(
        listing_log + "\n[unpack-all]\n" + result.stdout + result.stderr,
        encoding="utf-8",
        newline="\n",
    )
    manifest = {
        "schema_version": "1.0.0",
        "tool": "DriveClubFS",
        "tool_commit": DRIVECLUBFS_COMMIT,
        "started_at": started.isoformat(),
        "completed_at": datetime.now(UTC).isoformat(),
        "status": (
            "completed"
            if result.returncode == 0 and not verification_failures
            else "failed"
        ),
        "checksum_verification_requested": not skip_checksum_verify,
        "input_files": source_manifest,
        "preflight_entry_count": len(entries),
        "expected_output_bytes": expected_output_bytes,
        "free_bytes_before": free_bytes_before,
        "output_label": output.name,
        "exit_code": result.returncode,
        "verification_failure_count": len(verification_failures),
        "verification_failures": verification_failures[:100],
        "boundaries": [
            "Every listed path passed traversal, portability, and collision checks.",
            "Checksum verification is requested from upstream; older formats may "
            "not carry checksums and upstream may disable that check.",
            "This manifest does not establish semantic correctness of extracted "
            "resources.",
        ],
    }
    atomic_json_write(metadata / "manifest.json", manifest)
    atomic_json_write(
        metadata / "files.json",
        {"schema_version": "1.0.0", "entries": entries},
    )
    if result.returncode != 0 or verification_failures:
        raise RuntimeError(
            f"DriveClubFS extraction failed; retained diagnostics in {metadata}"
        )
    return manifest
