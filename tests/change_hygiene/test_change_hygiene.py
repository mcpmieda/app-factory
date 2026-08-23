from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.change_hygiene import (
    build_report,
    detect_tooling,
    scan_added_risks,
)


class ChangeHygieneTests(unittest.TestCase):
    def test_clean_small_project_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "app.py").write_text("def main():\n    return 1\n", encoding="utf-8")
            report = build_report(root)
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["blockers"], [])

    def test_tracked_style_backup_is_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "app.py.bak").write_text("old = True\n", encoding="utf-8")
            report = build_report(root)
            self.assertEqual(report["status"], "fail")
            self.assertEqual(report["blockers"][0]["kind"], "tracked-temporary-artifact")

    def test_conflict_marker_is_blocker(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "app.ts").write_text(
                "<<<<<<< HEAD\nconst value = 1;\n>>>>>>> branch\n",
                encoding="utf-8",
            )
            report = build_report(root)
            kinds = {item["kind"] for item in report["blockers"]}
            self.assertIn("merge-conflict-marker", kinds)

    def test_shadow_copy_is_advisory_not_automatic_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "service.ts").write_text("export const service = 1;\n", encoding="utf-8")
            (root / "service-v2.ts").write_text("export const service = 2;\n", encoding="utf-8")
            report = build_report(root)
            self.assertEqual(report["status"], "review")
            finding = next(item for item in report["advisories"] if item["kind"] == "possible-shadow-copy")
            self.assertEqual(finding["sibling"], "service.ts")

    def test_added_suppression_and_important_are_advisory(self) -> None:
        advisories: list[dict[str, object]] = []
        scan_added_risks(
            "styles.css",
            [".button { color: red !important; }", "/* stylelint-disable no-descending-specificity */"],
            advisories,
        )
        kinds = {item["kind"] for item in advisories}
        self.assertIn("css-important-added", kinds)
        self.assertIn("new-suppression", kinds)

    def test_language_specific_suppressions_are_detected_in_comments(self) -> None:
        advisories: list[dict[str, object]] = []
        scan_added_risks(
            "service.ts",
            ["const value = call(); // eslint-disable-line no-warning-comments", "// @ts-ignore"],
            advisories,
        )
        scan_added_risks("worker.py", ["import legacy  # noqa"], advisories)
        markers = [item["message"] for item in advisories if item["kind"] == "new-suppression"]
        self.assertTrue(any("eslint-disable" in message for message in markers))
        self.assertTrue(any("@ts-ignore" in message for message in markers))
        self.assertTrue(any("# noqa" in message for message in markers))

    def test_documentation_and_string_literals_do_not_fake_suppressions(self) -> None:
        advisories: list[dict[str, object]] = []
        scan_added_risks(
            "README.md",
            ["Avoid `eslint-disable`, `@ts-ignore`, `# noqa` and temporary workarounds."],
            advisories,
        )
        scan_added_risks(
            "scanner.py",
            [
                'MARKERS = ("# noqa", "# type: ignore")',
                'example = "# TODO: remove temporary workaround"',
            ],
            advisories,
        )
        self.assertEqual(advisories, [])

    def test_temporary_debt_marker_is_visible(self) -> None:
        advisories: list[dict[str, object]] = []
        scan_added_risks(
            "service.py",
            ["# TODO: remove temporary workaround after legacy migration"],
            advisories,
        )
        self.assertIn("temporary-debt-marker", {item["kind"] for item in advisories})

    def test_detects_existing_hygiene_tooling_without_installing_it(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "package.json").write_text(
                json.dumps(
                    {
                        "scripts": {"lint": "eslint ."},
                        "devDependencies": {
                            "eslint": "1",
                            "knip": "1",
                            "stylelint": "1",
                            "jscpd": "1",
                        },
                    }
                ),
                encoding="utf-8",
            )
            (root / "pyproject.toml").write_text(
                "[tool.ruff]\nline-length = 100\n[tool.vulture]\nmin_confidence = 100\n",
                encoding="utf-8",
            )
            tooling = detect_tooling(root)
            self.assertTrue(tooling["lint"])
            self.assertTrue(tooling["knip"])
            self.assertTrue(tooling["stylelint"])
            self.assertTrue(tooling["jscpd"])
            self.assertTrue(tooling["ruff"])
            self.assertTrue(tooling["vulture"])


if __name__ == "__main__":
    unittest.main()
