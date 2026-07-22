from __future__ import annotations

import hashlib
import json
import struct
import tempfile
import unittest
from pathlib import Path

from virtualauto.pkg import assemble_fragments, inspect_fragments


def build_sfo(values: dict[str, object]) -> bytes:
    keys = bytearray()
    data = bytearray()
    pending: list[tuple[int, int, int, int]] = []
    for key, value in values.items():
        key_delta = len(keys)
        keys.extend(key.encode("utf-8") + b"\0")
        while len(data) % 4:
            data.append(0)
        value_delta = len(data)
        if isinstance(value, int):
            raw = struct.pack("<I", value)
            value_format = 0x0404
        else:
            raw = str(value).encode("utf-8") + b"\0"
            value_format = 0x0204
        data.extend(raw)
        pending.append((key_delta, value_format, len(raw), value_delta))
    key_offset = 20 + len(pending) * 16
    data_offset = key_offset + len(keys)
    entries = b"".join(
        struct.pack("<HHIII", key_delta, value_format, length, length, value_delta)
        for key_delta, value_format, length, value_delta in pending
    )
    return (
        struct.pack("<4sIIII", b"\x00PSF", 0x101, key_offset, data_offset, len(pending))
        + entries
        + keys
        + data
    )


def create_fragment_set(directory: Path) -> tuple[bytes, list[Path]]:
    package = bytearray(index % 251 for index in range(6144))
    package[:4] = b"\x7fCNT"
    struct.pack_into(">I", package, 0x04, 0x83000001)
    struct.pack_into(">I", package, 0x0C, 15)
    struct.pack_into(">I", package, 0x10, 1)
    struct.pack_into(">I", package, 0x18, 0x500)
    package[0x40:0x64] = b"EP9000-CUSA00003_00-TESTPACKAGE000".ljust(0x24, b"\0")
    struct.pack_into(">I", package, 0x70, 0x0F)
    struct.pack_into(">I", package, 0x74, 0x1A)
    struct.pack_into(">I", package, 0x78, 0x42000000)
    struct.pack_into(">Q", package, 0x410, 0x1000)
    struct.pack_into(">Q", package, 0x418, 0x800)
    struct.pack_into(">Q", package, 0x430, len(package))
    sfo = build_sfo(
        {
            "APP_VER": "01.28",
            "CATEGORY": "gp",
            "TITLE_ID": "CUSA00003",
            "VERSION": "01.00",
        }
    )
    struct.pack_into(">IIIIIIQ", package, 0x500, 0x1000, 0, 0, 0, 0x600, len(sfo), 0)
    package[0x600 : 0x600 + len(sfo)] = sfo
    parts = [directory / "driveclub_0.pkg", directory / "driveclub_1.pkg"]
    parts[0].write_bytes(package[:4096])
    parts[1].write_bytes(package[4096:])
    return bytes(package), parts


class PackageFragmentTests(unittest.TestCase):
    def test_inspects_consecutive_fragment_set_and_sfo(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_fragment_set(root)
            report = inspect_fragments(root)
            self.assertEqual(report["status"], "structurally-valid")
            self.assertEqual(report["combined_byte_size"], 6144)
            self.assertEqual(report["package"]["param_sfo"]["APP_VER"], "01.28")
            self.assertEqual(report["package"]["param_sfo"]["CATEGORY"], "gp")

    def test_rejects_missing_fragment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _package, parts = create_fragment_set(root)
            parts[1].rename(root / "driveclub_2.pkg")
            with self.assertRaisesRegex(ValueError, "Missing"):
                inspect_fragments(root)

    def test_rejects_declared_size_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _package, parts = create_fragment_set(root)
            with parts[0].open("r+b") as handle:
                handle.seek(0x430)
                handle.write(struct.pack(">Q", 7000))
            with self.assertRaisesRegex(ValueError, "does not match"):
                inspect_fragments(root)

    def test_assembles_outside_input_and_records_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            inputs = root / "input"
            inputs.mkdir()
            package, _parts = create_fragment_set(inputs)
            output = root / "output/driveclub.pkg"
            manifest = assemble_fragments(inputs, output)
            self.assertEqual(output.read_bytes(), package)
            self.assertEqual(
                manifest["output"]["sha256"], hashlib.sha256(package).hexdigest()
            )
            manifest_path = output.with_suffix(".pkg.manifest.json")
            self.assertTrue(manifest_path.is_file())
            retained = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(len(retained["source_fragments"]), 2)
            with self.assertRaisesRegex(ValueError, "overwrite"):
                assemble_fragments(inputs, output)

    def test_rejects_output_inside_input_tree(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_fragment_set(root)
            with self.assertRaisesRegex(ValueError, "outside"):
                assemble_fragments(root, root / "assembled.pkg")


if __name__ == "__main__":
    unittest.main()
