from __future__ import annotations

import struct
import tempfile
import unittest
from pathlib import Path

from virtualauto.driveclub import (
    inspect_indexed_filesystem,
    parse_listing,
    require_separate_trees,
    safe_internal_name,
    validate_filesystem_input,
    validate_required_dat_files,
    verify_extracted_files,
)


def write_indexed_fixture(root: Path, *, sparse: bool) -> None:
    timestamp = 133_000_000_000_000_000
    marker = 0 if sparse else 0x12345678
    packed_entry = 0
    index = b"".join(
        (
            b"DATX",
            struct.pack("<I", 4300),
            struct.pack("<qQ", timestamp, 65536),
            struct.pack("<IIiI", 13, 1, 7, 65536),
            struct.pack("<IIiI", 0, 0, 1, 0),
            struct.pack("<iB", 1, 0),
            struct.pack("<iI", 0, marker),
            struct.pack("<QiI", packed_entry, 32, 0x1234),
            bytes(16),
            struct.pack("<I", marker),
        )
    )
    (root / "game.ndx").write_bytes(index)
    chunk_size = 0 if sparse else 64
    data_marker = bytes(4) if sparse else b"DATA"
    data = b"".join(
        (
            b"DATF",
            struct.pack("<I", 4300),
            struct.pack("<qQ", timestamp, 0),
            struct.pack("<iI", 1, 65536),
            b"CHNK",
            struct.pack("<I", chunk_size),
            data_marker,
            bytes(chunk_size),
        )
    )
    (root / "game000.dat").write_bytes(data)


class DriveClubPathTests(unittest.TestCase):
    def test_inspects_complete_indexed_filesystem(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_indexed_fixture(root, sparse=False)
            report = inspect_indexed_filesystem(root, root)
            self.assertEqual(report["status"], "complete_for_index")
            self.assertEqual(report["index"]["active_entry_count"], 1)
            self.assertEqual(report["active_entries_touching_zero_chunks"], 0)

    def test_identifies_sparse_overlay_that_requires_base(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_indexed_fixture(root, sparse=True)
            report = inspect_indexed_filesystem(root, root)
            self.assertEqual(report["status"], "overlay_or_repack_requires_base")
            self.assertEqual(report["zero_data_marker_count"], 1)
            self.assertEqual(report["active_entries_touching_zero_chunks"], 1)

    def test_parses_safe_listing(self) -> None:
        entries = parse_listing(
            "vehicles/ferrari_f40/body.rpk (4096 bytes, Dat Index: 2, "
            "Offset: 0x00001000)\n"
        )
        self.assertEqual(
            entries,
            [
                {
                    "path": "vehicles/ferrari_f40/body.rpk",
                    "size": 4096,
                    "dat_index": 2,
                    "offset": 4096,
                }
            ],
        )

    def test_rejects_traversal_and_absolute_paths(self) -> None:
        for value in (
            "../escape.bin",
            "/absolute.bin",
            "C:/escape.bin",
            "cars\\ambiguous.bin",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_internal_name(value)

    def test_rejects_windows_reserved_and_invalid_names(self) -> None:
        for value in ("cars/CON.bin", "cars/bad:name.bin", "cars/trailing. "):
            with self.subTest(value=value), self.assertRaises(ValueError):
                safe_internal_name(value)

    def test_rejects_case_insensitive_collision(self) -> None:
        listing = (
            "cars/F40.rpk (1 bytes, Dat Index: 0, Offset: 0x0)\n"
            "cars/f40.rpk (1 bytes, Dat Index: 0, Offset: 0x1)\n"
        )
        with self.assertRaisesRegex(ValueError, "collision"):
            parse_listing(listing)

    def test_input_requires_index_or_embedded_index_data(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "game.ndx"):
                validate_filesystem_input(root, root)
            (root / "game.dat").write_bytes(b"fixture")
            self.assertTrue(validate_filesystem_input(root, root).samefile(root))

    def test_missing_indexed_data_file_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "game.ndx").write_bytes(b"fixture")
            entries = [{"path": "a", "size": 1, "dat_index": 3, "offset": 0}]
            with self.assertRaisesRegex(ValueError, "game003.dat"):
                validate_required_dat_files(root, entries)

    def test_extracted_size_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory).resolve()
            target = output / "cars/f40.bin"
            target.parent.mkdir()
            target.write_bytes(b"1234")
            entries = [{"path": "cars/f40.bin", "size": 4, "dat_index": 0, "offset": 0}]
            self.assertEqual(verify_extracted_files(output, entries), [])
            entries[0]["size"] = 5
            self.assertRegex(verify_extracted_files(output, entries)[0], "^size:")

    def test_unexpected_output_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory).resolve()
            (output / "extra.bin").write_bytes(b"extra")
            self.assertEqual(
                verify_extracted_files(output, []), ["unexpected:extra.bin"]
            )

    def test_input_and_output_must_not_overlap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with self.assertRaisesRegex(ValueError, "must not overlap"):
                require_separate_trees(root / "input", root / "input/output")
            with self.assertRaisesRegex(ValueError, "must not overlap"):
                require_separate_trees(root / "output/input", root / "output")


if __name__ == "__main__":
    unittest.main()
