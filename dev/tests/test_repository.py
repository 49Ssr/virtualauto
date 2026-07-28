from __future__ import annotations

import ast
import hashlib
import importlib
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "research/indexes/automotive_master.index.json"


class RepositoryTests(unittest.TestCase):
    def test_core_cli_import_does_not_require_bpy(self) -> None:
        sys.modules.pop("bpy", None)
        importlib.import_module("virtualauto.cli")
        self.assertNotIn("bpy", sys.modules)

    def test_portable_core_has_no_bpy_imports(self) -> None:
        for source in (ROOT / "src/virtualauto").glob("*.py"):
            tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported = {alias.name.split(".", 1)[0] for alias in node.names}
                    self.assertNotIn("bpy", imported, source)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    self.assertNotEqual("bpy", node.module.split(".", 1)[0], source)

    def test_procedural_node_input_requires_coordinate_contract(self) -> None:
        schema = json.loads(
            (ROOT / "lab/schemas/node-contract.schema.json").read_text(
                encoding="utf-8"
            )
        )
        example = json.loads(
            (ROOT / "lab/examples/node_contract.json").read_text(encoding="utf-8")
        )
        jsonschema.Draft202012Validator(schema).validate(example)
        del example["inputs"][0]["coordinate_contract"]
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.Draft202012Validator(schema).validate(example)

    def test_f40_camera_contract_is_schema_valid(self) -> None:
        schema = json.loads(
            (ROOT / "lab/schemas/camera-pipeline.schema.json").read_text(
                encoding="utf-8"
            )
        )
        contract = json.loads(
            (
                ROOT
                / "research/projects/driveclub_f40/camera_pipeline.json"
            ).read_text(encoding="utf-8")
        )
        jsonschema.Draft202012Validator(schema).validate(contract)
        self.assertEqual(contract["status"], "qualified")
        self.assertGreater(len(contract["explicitly_unset"]), 0)
        image_checks = contract["compositor"]["image_checks"]
        self.assertEqual(len(image_checks), 4)
        self.assertTrue(
            all(
                len(check["float32_sha256_native_little_endian"]) == 64
                for check in image_checks
            )
        )

    def test_camera_audit_is_declared_read_only(self) -> None:
        source = (
            ROOT / "workflows/blender/scripts/audit_camera_pipeline.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("bpy.ops.wm.save", source)
        self.assertNotIn("bpy.ops.render", source)
        self.assertNotIn(".new(", source)
        self.assertNotIn(".remove(", source)

    def test_lensfun_builder_reloads_portable_equations(self) -> None:
        source = (
            ROOT / "workflows/blender/scripts/build_lensfun_maps.py"
        ).read_text(encoding="utf-8")
        self.assertIn("importlib.reload(lensfun_models)", source)

    def test_master_index_generation_is_deterministic(self) -> None:
        before = hashlib.sha256(INDEX.read_bytes()).hexdigest()
        result = subprocess.run(
            [sys.executable, "dev/scripts/build_master_index.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        after = hashlib.sha256(INDEX.read_bytes()).hexdigest()
        self.assertEqual(before, after)

    def test_strict_repository_validation(self) -> None:
        environment = os.environ.copy()
        environment["VIRTUALAUTO_STRICT_VALIDATION"] = "1"
        result = subprocess.run(
            [sys.executable, "dev/scripts/validate_repository.py"],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
