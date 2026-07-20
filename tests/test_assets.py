from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from virtualauto.assets import register_source_asset


class SourceAssetTests(unittest.TestCase):
    def test_registers_hash_without_leaking_private_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "private-source.bin"
            source.write_bytes(b"virtualauto-private-fixture")
            output = root / "records/source.json"
            record = register_source_asset(
                input_path=source,
                output_path=output,
                asset_id="AST-TEST-PRIVATE-001",
                title="Synthetic private fixture",
                source_kind="other",
                format_name="binary-fixture",
                provenance="Created by a unit test; contains no third-party data.",
                rights_status="original",
                storage_reference="TEST-PRIVATE-001",
                root=root,
            )
            self.assertEqual(
                record["sha256"], hashlib.sha256(source.read_bytes()).hexdigest()
            )
            self.assertNotIn(str(source), output.read_text(encoding="utf-8"))

    def test_rejects_path_like_storage_reference(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "fixture.bin"
            source.write_bytes(b"x")
            with self.assertRaisesRegex(ValueError, "opaque label"):
                register_source_asset(
                    input_path=source,
                    output_path="record.json",
                    asset_id="AST-TEST-PRIVATE-002",
                    title="Synthetic private fixture",
                    source_kind="other",
                    format_name="binary-fixture",
                    provenance="Created by a unit test only.",
                    rights_status="original",
                    storage_reference="C:/private/fixture.bin",
                    root=root,
                )


if __name__ == "__main__":
    unittest.main()
