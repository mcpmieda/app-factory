from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from scripts.provider_worker import _assert_safe_staged_files


class ProviderWorkerStageSafetyTests(unittest.TestCase):
    def test_staged_symlink_is_rejected_before_resolution(self) -> None:
        with tempfile.TemporaryDirectory(prefix="provider-stage-symlink-") as raw:
            root = Path(raw)
            docs = root / "docs"
            docs.mkdir()
            target = root / "target.txt"
            target.write_text("safe target\n", encoding="utf-8")
            symlink = docs / "stage.txt"
            try:
                symlink.symlink_to(target)
            except OSError as error:
                self.skipTest(f"symlink unavailable on this platform: {error}")

            request = SimpleNamespace(worktree=root)
            with self.assertRaisesRegex(ValueError, "regular file"):
                _assert_safe_staged_files(request, ("docs/stage.txt",))


if __name__ == "__main__":
    unittest.main()
