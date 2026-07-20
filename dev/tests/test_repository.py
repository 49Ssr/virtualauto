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
