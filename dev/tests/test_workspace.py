from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from virtualauto.workspace import STAGES, initialise_workspace


class WorkspaceTests(unittest.TestCase):
    def test_creates_isolated_utility_boundaries(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            repository = temporary / "repo"
            repository.mkdir()
            workspace = temporary / "private"
            manifest = initialise_workspace(
                workspace,
                run_id="dc-f40-001",
                repository=repository,
            )
            run = workspace / "runs/dc-f40-001"
            self.assertEqual(manifest["run_root"], str(run))
            self.assertTrue((run / "workspace.json").is_file())
            for stage in STAGES:
                self.assertTrue((run / stage / "input").is_dir())
                self.assertTrue((run / stage / "output").is_dir())
            with self.assertRaisesRegex(ValueError, "already exists"):
                initialise_workspace(
                    workspace,
                    run_id="dc-f40-001",
                    repository=repository,
                )

    def test_rejects_workspace_inside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory).resolve()
            with self.assertRaisesRegex(ValueError, "outside"):
                initialise_workspace(
                    repository / "private",
                    run_id="dc-f40-001",
                    repository=repository,
                )


if __name__ == "__main__":
    unittest.main()
