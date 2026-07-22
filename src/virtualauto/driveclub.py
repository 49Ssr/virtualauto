"""Guarded orchestration for the pinned DriveClubFS research instrument."""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import struct
import subprocess
import tempfile
import unicodedata
from datetime import UTC, datetime, timedelta
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
WINDOWS_EPOCH = datetime(1601, 1, 1, tzinfo=UTC)
DAT_INDEX_16BIT_CUTOFF = datetime(2014, 8, 20, tzinfo=UTC)


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


def _read_exact(handle, size: int, label: str) -> bytes:
    value = handle.read(size)
    if len(value) != size:
        raise ValueError(f"Truncated {label}: expected {size} bytes, got {len(value)}")
    return value


def _filetime_datetime(value: int) -> datetime:
    return WINDOWS_EPOCH + timedelta(microseconds=value // 10)


def _inspect_dat_header(path: Path) -> tuple[dict[str, object], list[int]]:
    with path.open("rb") as handle:
        magic = _read_exact(handle, 4, f"{path.name} magic")
        (version,) = struct.unpack("<I", _read_exact(handle, 4, "DAT version"))
        timestamp, toc_offset = struct.unpack(
            "<qQ", _read_exact(handle, 16, "DAT timestamp/TOC")
        )
        if magic != b"DATF":
            raise ValueError(f"{path.name} does not start with DATF")
        if version != 4300:
            raise ValueError(
                f"{path.name} uses unsupported split-DAT version {version}"
            )
        chunk_count, buffer_size = struct.unpack(
            "<iI", _read_exact(handle, 8, "DAT chunk header")
        )
        if chunk_count < 0 or chunk_count > 10_000_000:
            raise ValueError(f"{path.name} has implausible chunk count {chunk_count}")
        if buffer_size == 0:
            raise ValueError(f"{path.name} declares a zero-byte logical chunk size")
        chunk_magic = _read_exact(handle, 4, "DAT CHNK marker")
        if chunk_magic != b"CHNK":
            raise ValueError(f"{path.name} is missing the CHNK marker")
        packed = _read_exact(handle, chunk_count * 4, "DAT chunk-size table")
        chunk_sizes = list(struct.unpack(f"<{chunk_count}I", packed))
        data_magic = _read_exact(handle, 4, "DAT DATA marker")
        if data_magic not in {b"DATA", bytes(4)}:
            raise ValueError(
                f"{path.name} has unsupported DATA marker {data_magic.hex()}"
            )
        data_start = handle.tell()

    packed_payload_bytes = sum(chunk_sizes)
    byte_size = path.stat().st_size
    if data_start + packed_payload_bytes > byte_size:
        raise ValueError(
            f"{path.name} chunk table declares {packed_payload_bytes} payload bytes "
            f"but only {byte_size - data_start} are present"
        )
    zero_chunks = sum(size == 0 for size in chunk_sizes)
    report = {
        "name": path.name,
        "byte_size": byte_size,
        "version": version,
        "timestamp_filetime": timestamp,
        "toc_offset": toc_offset,
        "chunk_count": chunk_count,
        "buffer_size": buffer_size,
        "chunk_marker": chunk_magic.decode("ascii"),
        "data_marker": data_magic.decode("ascii", errors="replace"),
        "data_marker_hex": data_magic.hex(),
        "data_start": data_start,
        "packed_payload_bytes": packed_payload_bytes,
        "packed_stream_end": data_start + packed_payload_bytes,
        "trailing_bytes": byte_size - (data_start + packed_payload_bytes),
        "zero_sized_chunk_count": zero_chunks,
    }
    return report, chunk_sizes


def inspect_indexed_filesystem(
    input_directory: str | Path, root: Path | None = None
) -> dict[str, object]:
    """Inspect a modern DriveClub index/DAT set without decompressing payloads."""

    root = root or repository_root()
    directory = validate_filesystem_input(input_directory, root)
    index_path = directory / "game.ndx"
    if not index_path.is_file():
        raise ValueError("Indexed-filesystem inspection requires game.ndx")

    with index_path.open("rb") as handle:
        magic = _read_exact(handle, 4, "index magic")
        (version,) = struct.unpack("<I", _read_exact(handle, 4, "index version"))
        timestamp, total_data_size = struct.unpack(
            "<qQ", _read_exact(handle, 16, "index timestamp/size")
        )
        hash_a, hash_b, compression, read_buffer_size = struct.unpack(
            "<IIiI", _read_exact(handle, 16, "index hashing/compression")
        )
        if magic not in {b"DATN", b"DATX"}:
            raise ValueError(f"Unexpected index magic {magic!r}")
        if version != 4300:
            raise ValueError(
                "Indexed-filesystem inspection currently supports version 4300, "
                f"got {version}"
            )
        if read_buffer_size == 0:
            raise ValueError("Index declares a zero-byte logical read buffer")
        unknown_1, unknown_2, data_file_count, unknown_4 = struct.unpack(
            "<IIiI", _read_exact(handle, 16, "index split-DAT fields")
        )
        (entry_count,) = struct.unpack("<i", _read_exact(handle, 4, "entry count"))
        dictionary_size = _read_exact(handle, 1, "dictionary size")[0]
        if entry_count < 0 or entry_count > 1_000_000:
            raise ValueError(f"Implausible index entry count {entry_count}")
        if dictionary_size > 0x80:
            raise ValueError(f"Implausible dictionary size {dictionary_size}")
        handle.seek(dictionary_size * 2, os.SEEK_CUR)
        (compressed_names_size,) = struct.unpack(
            "<i", _read_exact(handle, 4, "compressed-name size")
        )
        if compressed_names_size < 0:
            raise ValueError("Compressed-name size cannot be negative")
        handle.seek(compressed_names_size, os.SEEK_CUR)
        names_marker = _read_exact(handle, 4, "post-name marker")

        active_entries: list[dict[str, int]] = []
        use_16_bit_index = _filetime_datetime(timestamp) > DAT_INDEX_16BIT_CUTOFF
        for _ in range(entry_count):
            packed_index_offset, size, name_hash = struct.unpack(
                "<QiI", _read_exact(handle, 16, "index entry")
            )
            _read_exact(handle, 16, "index entry MD5")
            if size < 0:
                raise ValueError("Index contains a negative file size")
            if use_16_bit_index:
                dat_index = packed_index_offset & 0xFFFF
                file_offset = packed_index_offset >> 16
            else:
                dat_index = packed_index_offset & 0xFF
                file_offset = packed_index_offset >> 8
            if size > 0:
                active_entries.append(
                    {
                        "dat_index": dat_index,
                        "offset": file_offset,
                        "size": size,
                        "name_hash": name_hash,
                    }
                )
        entries_marker = _read_exact(handle, 4, "post-entry marker")

    dat_paths: dict[int, Path] = {}
    for path in directory.glob("game*.dat"):
        match = re.fullmatch(r"game(?P<index>\d{3})\.dat", path.name)
        if match:
            dat_paths[int(match.group("index"))] = path

    dat_reports: list[dict[str, object]] = []
    chunk_tables: dict[int, list[int]] = {}
    invalid_dat_files: list[dict[str, str]] = []
    for index, path in sorted(dat_paths.items()):
        try:
            report, chunk_sizes = _inspect_dat_header(path)
        except (OSError, ValueError, struct.error) as error:
            invalid_dat_files.append({"name": path.name, "error": str(error)})
            continue
        report["dat_index"] = index
        dat_reports.append(report)
        chunk_tables[index] = chunk_sizes

    referenced_indices = sorted({entry["dat_index"] for entry in active_entries})
    missing_dat_files = [
        f"game{index:03}.dat" for index in referenced_indices if index not in dat_paths
    ]
    mismatched_dat_buffer_sizes = [
        str(report["name"])
        for report in dat_reports
        if report["buffer_size"] != read_buffer_size
    ]
    entries_touching_zero_chunks = 0
    entries_outside_chunk_tables = 0
    for entry in active_entries:
        chunks = chunk_tables.get(entry["dat_index"])
        if chunks is None:
            continue
        first = entry["offset"] // read_buffer_size
        last = (entry["offset"] + entry["size"] - 1) // read_buffer_size
        if first >= len(chunks) or last >= len(chunks):
            entries_outside_chunk_tables += 1
            continue
        if any(size == 0 for size in chunks[first : last + 1]):
            entries_touching_zero_chunks += 1

    zero_data_markers = sum(
        report["data_marker_hex"] == "00000000" for report in dat_reports
    )
    index_markers = {
        "post_names": names_marker,
        "post_entries": entries_marker,
    }
    nonstandard_index_markers = [
        name
        for name, marker in index_markers.items()
        if marker not in {b"\x78\x56\x34\x12"}
    ]
    invalid_index_markers = [
        name
        for name, marker in index_markers.items()
        if marker not in {b"\x78\x56\x34\x12", bytes(4)}
    ]
    warnings: list[str] = []
    if missing_dat_files:
        warnings.append("one or more DAT files referenced by active entries are absent")
    if invalid_dat_files:
        warnings.append("one or more DAT headers could not be parsed")
    if mismatched_dat_buffer_sizes:
        warnings.append("one or more DAT logical chunk sizes disagree with the index")
    if entries_touching_zero_chunks:
        warnings.append(
            "active entries cross zero-sized chunks; a base/patch overlay or "
            "cleaner dump is required"
        )
    if entries_outside_chunk_tables:
        warnings.append("active entries extend beyond their DAT chunk tables")
    if zero_data_markers or nonstandard_index_markers:
        warnings.append(
            "zeroed format sentinels indicate a noncanonical repack or sparse overlay"
        )
    if invalid_index_markers:
        warnings.append("one or more index sentinels contain unsupported values")

    status = "complete_for_index"
    if (
        missing_dat_files
        or invalid_dat_files
        or mismatched_dat_buffer_sizes
        or entries_outside_chunk_tables
        or invalid_index_markers
    ):
        status = "invalid_or_incomplete"
    elif entries_touching_zero_chunks or zero_data_markers:
        status = "overlay_or_repack_requires_base"

    return {
        "schema_version": "1.0.0",
        "captured_at": datetime.now(UTC).isoformat(),
        "scope": "read-only structural inspection; no payload decompression",
        "status": status,
        "index": {
            "name": index_path.name,
            "byte_size": index_path.stat().st_size,
            "magic": magic.decode("ascii"),
            "version": version,
            "timestamp": _filetime_datetime(timestamp).isoformat(),
            "total_data_size": total_data_size,
            "hash_a": hash_a,
            "hash_b": hash_b,
            "compression": compression,
            "read_buffer_size": read_buffer_size,
            "declared_data_file_count": data_file_count,
            "entry_count": entry_count,
            "active_entry_count": len(active_entries),
            "dictionary_size": dictionary_size,
            "compressed_names_size": compressed_names_size,
            "post_names_marker_hex": names_marker.hex(),
            "post_entries_marker_hex": entries_marker.hex(),
            "unknown_fields": [unknown_1, unknown_2, unknown_4],
        },
        "present_dat_file_count": len(dat_paths),
        "parsed_dat_file_count": len(dat_reports),
        "referenced_dat_indices": referenced_indices,
        "missing_dat_files": missing_dat_files,
        "invalid_dat_files": invalid_dat_files,
        "mismatched_dat_buffer_sizes": mismatched_dat_buffer_sizes,
        "zero_data_marker_count": zero_data_markers,
        "active_entries_touching_zero_chunks": entries_touching_zero_chunks,
        "active_entries_outside_chunk_tables": entries_outside_chunk_tables,
        "nonstandard_index_markers": nonstandard_index_markers,
        "invalid_index_markers": invalid_index_markers,
        "dat_files": dat_reports,
        "warnings": warnings,
    }


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
