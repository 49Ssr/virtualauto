from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "generated/automotive_master.index.json"


class RepositoryTests(unittest.TestCase):
    def test_master_index_generation_is_deterministic(self) -> None:
        before = hashlib.sha256(INDEX.read_bytes()).hexdigest()
        result = subprocess.run(
            [sys.executable, "scripts/build_master_index.py"],
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
            [sys.executable, "scripts/validate_repository.py"],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
