from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.context_engine import scan_repository


class ContextEngineTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        (root / "src").mkdir()
        (root / "node_modules/pkg").mkdir(parents=True)
        (root / "package.json").write_text(json.dumps({
            "dependencies": {"next": "16", "react": "19", "@heroui/react": "3"},
            "devDependencies": {"vitest": "4"},
            "scripts": {"build": "next build", "test": "vitest run"},
        }), encoding="utf-8")
        (root / "src/app.tsx").write_text(
            'import React from "react";\nexport function App() { return <main>Hello</main>; }\n',
            encoding="utf-8",
        )
        (root / "src/domain.py").write_text("import json\n\nclass Student:\n    pass\n", encoding="utf-8")
        (root / "README.md").write_text("# Demo\n", encoding="utf-8")
        (root / ".env").write_text("SECRET=do-not-read\n", encoding="utf-8")
        (root / "node_modules/pkg/index.js").write_text("module.exports = 1\n", encoding="utf-8")
        return temp, root

    def test_maps_stack_symbols_and_excludes_sensitive_generated_content(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        result = scan_repository(root)
        mapped = result.repo_map["files"]
        self.assertIn("src/app.tsx", mapped)
        self.assertIn("App", mapped["src/app.tsx"]["symbols"])
        self.assertIn("Student", mapped["src/domain.py"]["symbols"])
        self.assertNotIn(".env", mapped)
        self.assertNotIn("node_modules/pkg/index.js", mapped)
        self.assertEqual(result.repo_map["stack"]["package_manager"], None)
        self.assertIn("Next.js", result.repo_map["stack"]["frameworks"])
        self.assertIn("HeroUI", result.repo_map["stack"]["frameworks"])

    def test_incremental_cache_reuses_unchanged_metadata(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        first = scan_repository(root)
        second = scan_repository(root)
        self.assertEqual(second.repo_map["fingerprint"], first.repo_map["fingerprint"])
        self.assertEqual(second.repo_map["stats"]["reprocessed"], 0)
        self.assertEqual(second.repo_map["stats"]["cache_hits"], first.repo_map["stats"]["files"])
        self.assertEqual(second.repo_map["delta"], {"added": [], "changed": [], "removed": []})

    def test_delta_detects_added_changed_and_removed_files(self) -> None:
        temp, root = self.make_repo()
        self.addCleanup(temp.cleanup)
        scan_repository(root)
        (root / "src/app.tsx").write_text('export const App = () => "changed";\n', encoding="utf-8")
        (root / "src/domain.py").unlink()
        (root / "src/new.ts").write_text("export const value = 1;\n", encoding="utf-8")
        result = scan_repository(root)
        self.assertEqual(result.repo_map["delta"]["added"], ["src/new.ts"])
        self.assertEqual(result.repo_map["delta"]["changed"], ["src/app.tsx"])
        self.assertEqual(result.repo_map["delta"]["removed"], ["src/domain.py"])
        self.assertEqual(result.repo_map["stats"]["reprocessed"], 2)


if __name__ == "__main__":
    unittest.main()
