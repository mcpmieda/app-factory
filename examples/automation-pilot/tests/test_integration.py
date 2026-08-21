import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class CliIntegrationTests(unittest.TestCase):
    def test_dry_run_never_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "roster_report",
                    str(ROOT / "fixtures/roster.csv"),
                    str(output),
                    "--dry-run",
                ],
                cwd=ROOT,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(output.exists())
            self.assertIn('"rejected": 1', result.stdout)
            self.assertIn("no file written", result.stderr)

    def test_repeated_execution_is_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            command = [
                sys.executable,
                "-m",
                "roster_report",
                str(ROOT / "fixtures/roster.csv"),
                str(output),
            ]
            first = subprocess.run(command, cwd=ROOT, check=False, capture_output=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            first_bytes = output.read_bytes()
            second = subprocess.run(command, cwd=ROOT, check=False, capture_output=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(first_bytes, output.read_bytes())


if __name__ == "__main__":
    unittest.main()
