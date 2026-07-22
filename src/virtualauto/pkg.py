"""Inspect and assemble byte-split PS4 PKG containers without altering inputs."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import struct
from datetime import UTC, datetime
from pathlib import Path

PKG_MAGIC = b"\x7fCNT"
PKG_SIZE_OFFSET = 0x430
MINIMUM_HEADER_SIZE = PKG_SIZE_OFFSET + 8
COPY_BLOCK_SIZE = 16 * 1024 * 1024
FRAGMENT_NAME = re.compile(r"^(?P<stem>.+)_(?P<index>\d+)\.pkg$", re.IGNORECASE)


def _read_exact(path: Path, offset: int, size: int) -> bytes:
    with path.open("rb") as handle:
        handle.seek(offset)
        value = handle.read(size)
    if len(value) != size:
        raise ValueError(
            f"{path.name} is too short for offset 0x{offset:X} and {size} bytes"
        )
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(COPY_BLOCK_SIZE), b""):
            digest.update(block)
    return digest.hexdigest()


def _parse_sfo(data: bytes) -> dict[str, object]:
    if len(data) < 20 or data[:4] != b"\x00PSF":
        raise ValueError("param.sfo does not have a valid PSF header")
    _magic, _version, key_offset, data_offset, count = struct.unpack_from(
        "<4sIIII", data, 0
    )
    table_end = 20 + count * 16
    if table_end > len(data) or key_offset > len(data) or data_offset > len(data):
        raise ValueError("param.sfo table offsets exceed the retained metadata")

    values: dict[str, object] = {}
    for index in range(count):
        key_delta, value_format, length, _maximum, value_delta = struct.unpack_from(
            "<HHIII", data, 20 + index * 16
        )
        key_start = key_offset + key_delta
        key_end = data.find(b"\0", key_start)
        value_start = data_offset + value_delta
        value_end = value_start + length
        if key_start >= len(data) or key_end < 0 or value_end > len(data):
            raise ValueError("param.sfo entry points outside the retained metadata")
        key = data[key_start:key_end].decode("utf-8", "replace")
        raw = data[value_start:value_end]
        if value_format in {0x0204, 0x2044}:
            encoded = raw.rstrip(b"\0")
            try:
                value: object = encoded.decode("utf-8")
            except UnicodeDecodeError:
                value = encoded.decode("cp1252", "replace")
        elif value_format == 0x0404 and len(raw) >= 4:
            value = struct.unpack_from("<I", raw)[0]
        else:
            value = {"format": f"0x{value_format:04X}", "hex": raw.hex()}
        values[key] = value
    return values


def _read_pkg_metadata(first_fragment: Path) -> dict[str, object]:
    header = _read_exact(first_fragment, 0, 0x440)
    if header[:4] != PKG_MAGIC:
        raise ValueError(f"First fragment has no PS4 PKG header: {first_fragment.name}")

    entry_count = struct.unpack_from(">I", header, 0x10)[0]
    table_offset = struct.unpack_from(">I", header, 0x18)[0]
    metadata: dict[str, object] = {
        "magic": "0x7F434E54",
        "package_type": f"0x{struct.unpack_from('>I', header, 0x04)[0]:08X}",
        "file_count": struct.unpack_from(">I", header, 0x0C)[0],
        "entry_count": entry_count,
        "content_id": header[0x40:0x64]
        .split(b"\0", 1)[0]
        .decode("ascii", "replace"),
        "drm_type": f"0x{struct.unpack_from('>I', header, 0x70)[0]:08X}",
        "content_type": f"0x{struct.unpack_from('>I', header, 0x74)[0]:08X}",
        "content_flags": f"0x{struct.unpack_from('>I', header, 0x78)[0]:08X}",
        "pfs_image_offset": struct.unpack_from(">Q", header, 0x410)[0],
        "pfs_image_size": struct.unpack_from(">Q", header, 0x418)[0],
        "declared_pkg_size": struct.unpack_from(">Q", header, PKG_SIZE_OFFSET)[0],
    }

    table_size = entry_count * 32
    if entry_count > 1_000_000:
        raise ValueError(f"Implausible PKG entry count: {entry_count}")
    entries = _read_exact(first_fragment, table_offset, table_size)
    param_entry: tuple[int, int] | None = None
    for index in range(entry_count):
        entry_id, _name, _flags1, _flags2, offset, size, _padding = (
            struct.unpack_from(">IIIIIIQ", entries, index * 32)
        )
        if entry_id == 0x1000:
            param_entry = (offset, size)
            break
    if param_entry is not None:
        offset, size = param_entry
        metadata["param_sfo"] = _parse_sfo(_read_exact(first_fragment, offset, size))
    else:
        metadata["param_sfo"] = None
    return metadata


def _discover_fragments(input_path: str | Path) -> tuple[Path, str, list[Path]]:
    source = Path(input_path).expanduser().resolve()
    selected_stem: str | None = None
    if source.is_file():
        match = FRAGMENT_NAME.fullmatch(source.name)
        if match is None:
            raise ValueError(f"Input file is not a numbered PKG fragment: {source}")
        selected_stem = match.group("stem")
        directory = source.parent
    elif source.is_dir():
        directory = source
    else:
        raise ValueError(f"PKG fragment input does not exist: {source}")

    groups: dict[str, dict[int, Path]] = {}
    display_stems: dict[str, str] = {}
    for candidate in directory.iterdir():
        if not candidate.is_file():
            continue
        match = FRAGMENT_NAME.fullmatch(candidate.name)
        if match is None:
            continue
        stem = match.group("stem")
        if selected_stem is not None and stem.casefold() != selected_stem.casefold():
            continue
        key = stem.casefold()
        index = int(match.group("index"))
        if index in groups.setdefault(key, {}):
            raise ValueError(f"Duplicate PKG fragment index {index} for {stem}")
        groups[key][index] = candidate.resolve()
        display_stems.setdefault(key, stem)

    if not groups:
        raise ValueError(f"No numbered *_N.pkg fragment set found in {directory}")
    if len(groups) != 1:
        names = ", ".join(sorted(display_stems.values(), key=str.casefold))
        raise ValueError(
            f"Multiple PKG fragment sets found ({names}); pass one fragment path"
        )
    key, indexed = next(iter(groups.items()))
    maximum = max(indexed)
    missing = sorted(set(range(maximum + 1)).difference(indexed))
    if missing:
        raise ValueError(f"Missing PKG fragment indices: {missing}")
    fragments = [indexed[index] for index in range(maximum + 1)]
    return directory, display_stems[key], fragments


def inspect_fragments(
    input_path: str | Path, *, hash_fragments: bool = False
) -> dict[str, object]:
    """Validate a numbered PKG set and return observed package metadata."""
    directory, stem, fragments = _discover_fragments(input_path)
    if len(fragments) < 2:
        raise ValueError("A split PKG set must contain at least two fragments")

    sizes = [path.stat().st_size for path in fragments]
    if any(size <= 0 for size in sizes):
        raise ValueError("PKG fragments must not be empty")
    if sizes[0] < MINIMUM_HEADER_SIZE:
        raise ValueError("First PKG fragment is too small to retain the package header")
    if any(size != sizes[0] for size in sizes[:-1]):
        raise ValueError("All non-final PKG fragments must have an identical byte size")
    if sizes[-1] > sizes[0]:
        raise ValueError("Final PKG fragment is larger than the preceding fragments")
    if _read_exact(fragments[0], 0, 4) != PKG_MAGIC:
        raise ValueError("Fragment zero does not start with the PS4 PKG magic")
    for fragment in fragments[1:]:
        if _read_exact(fragment, 0, 4) == PKG_MAGIC:
            raise ValueError(
                "Continuation fragment unexpectedly contains a PKG header: "
                f"{fragment.name}"
            )

    metadata = _read_pkg_metadata(fragments[0])
    combined_size = sum(sizes)
    if metadata["declared_pkg_size"] != combined_size:
        raise ValueError(
            "Combined fragment size does not match the package header: "
            f"{combined_size} != {metadata['declared_pkg_size']}"
        )

    records: list[dict[str, object]] = []
    for index, (path, size) in enumerate(zip(fragments, sizes, strict=True)):
        record: dict[str, object] = {
            "index": index,
            "name": path.name,
            "byte_size": size,
        }
        if hash_fragments:
            record["sha256"] = _sha256(path)
        records.append(record)
    return {
        "report_version": "1.0.0",
        "status": "structurally-valid",
        "input_directory": str(directory),
        "fragment_stem": stem,
        "fragment_count": len(fragments),
        "fragment_byte_size": sizes[0],
        "combined_byte_size": combined_size,
        "fragments": records,
        "package": metadata,
        "limits": [
            "Structural validation does not prove source authenticity.",
            "Fragment hashes are local provenance unless compared with an "
            "upstream manifest.",
            "Package metadata access does not imply payload decryption or extraction.",
        ],
    }


def _write_json_atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    os.replace(temporary, path)


def assemble_fragments(
    input_path: str | Path,
    output_path: str | Path,
) -> dict[str, object]:
    """Stream a validated fragment set into a new, checksum-recorded PKG."""
    report = inspect_fragments(input_path, hash_fragments=False)
    input_directory, _stem, fragments = _discover_fragments(input_path)
    output = Path(output_path).expanduser().resolve()
    if output.suffix.casefold() != ".pkg":
        raise ValueError("Assembled output must use the .pkg extension")
    try:
        output.relative_to(input_directory)
    except ValueError:
        pass
    else:
        raise ValueError("Assembled output must remain outside the fragment input tree")

    output.parent.mkdir(parents=True, exist_ok=True)
    partial = output.with_suffix(output.suffix + ".partial")
    manifest = output.with_suffix(output.suffix + ".manifest.json")
    for candidate in (output, partial, manifest):
        if candidate.exists():
            raise ValueError(f"Refusing to overwrite existing output: {candidate}")

    required = int(report["combined_byte_size"]) + COPY_BLOCK_SIZE
    free = shutil.disk_usage(output.parent).free
    if free < required:
        raise ValueError(
            f"Insufficient free space: require at least {required} bytes, have {free}"
        )

    source_state = {
        path: (path.stat().st_size, path.stat().st_mtime_ns) for path in fragments
    }
    combined_digest = hashlib.sha256()
    fragment_records: list[dict[str, object]] = []
    try:
        with partial.open("xb") as destination:
            for index, fragment in enumerate(fragments):
                fragment_digest = hashlib.sha256()
                copied = 0
                with fragment.open("rb") as source:
                    for block in iter(lambda: source.read(COPY_BLOCK_SIZE), b""):
                        destination.write(block)
                        fragment_digest.update(block)
                        combined_digest.update(block)
                        copied += len(block)
                if copied != source_state[fragment][0]:
                    raise ValueError(f"Fragment size changed while reading: {fragment}")
                fragment_records.append(
                    {
                        "index": index,
                        "name": fragment.name,
                        "byte_size": copied,
                        "sha256": fragment_digest.hexdigest(),
                    }
                )
            destination.flush()
            os.fsync(destination.fileno())

        for fragment, before in source_state.items():
            after = (fragment.stat().st_size, fragment.stat().st_mtime_ns)
            if after != before:
                raise ValueError(f"Fragment changed during assembly: {fragment}")
        if partial.stat().st_size != report["combined_byte_size"]:
            raise ValueError("Assembled temporary file has an unexpected byte size")
        output_metadata = _read_pkg_metadata(partial)
        if output_metadata["declared_pkg_size"] != partial.stat().st_size:
            raise ValueError("Assembled package does not match its declared byte size")
        os.replace(partial, output)
    except Exception:
        if partial.exists():
            partial.unlink()
        raise

    result: dict[str, object] = {
        "manifest_version": "1.0.0",
        "operation": "byte-exact-split-pkg-assembly",
        "created_at": datetime.now(UTC).isoformat(),
        "source_inputs_immutable": True,
        "input_directory": str(input_directory),
        "source_fragments": fragment_records,
        "output": {
            "path": str(output),
            "byte_size": output.stat().st_size,
            "sha256": combined_digest.hexdigest(),
        },
        "package": output_metadata,
        "validation": {
            "consecutive_indices": True,
            "single_leading_header": True,
            "uniform_nonfinal_fragment_size": True,
            "declared_size_matches": True,
            "source_state_unchanged": True,
        },
        "limits": report["limits"],
    }
    _write_json_atomic(manifest, result)
    result["manifest_path"] = str(manifest)
    return result
