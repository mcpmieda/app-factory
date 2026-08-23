from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "semantic_assurance.py"


class SemanticAssuranceCLITests(unittest.TestCase):
    def test_direct_cli_runs_without_pythonpath_or_repo_cwd(self) -> None:
        env = os.environ.copy()
        env.pop("PYTHONPATH", None)

        with tempfile.TemporaryDirectory() as cwd:
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "--help"],
                cwd=cwd,
                env=env,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("App Factory Semantic Assurance", completed.stdout)


if __name__ == "__main__":
    unittest.main()
