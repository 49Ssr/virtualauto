from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from virtualauto.driveclub import (
    parse_listing,
    require_separate_trees,
    safe_internal_name,
    validate_filesystem_input,
    validate_required_dat_files,
    verify_extracted_files,
)


class DriveClubPathTests(unittest.TestCase):
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
