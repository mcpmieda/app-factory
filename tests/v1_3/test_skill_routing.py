from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLI = ROOT / "scripts" / "skill_routing.py"

from engine.learning_engine import (  # noqa: E402
    empty_skill_routing_state,
    normalize_skill_name,
    read_skill_routing_state,
    record_skill_routing,
    skill_routing_path,
    skill_routing_report,
)


class SkillRoutingTests(unittest.TestCase):
    def test_record_deduplicates_skills_and_reports_never_selected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = record_skill_routing(
                root,
                skills=["factory-router", "ui-builder", "factory-router"],
                source="factory-router",
            )
            self.assertEqual(first["decisions"], 1)
            self.assertEqual(first["selected_total"], 2)
            self.assertEqual(first["skills"], {"factory-router": 1, "ui-builder": 1})
            self.assertTrue(first["local_only"])
            self.assertFalse(first["external_telemetry"])

            second = record_skill_routing(
                root,
                skills=["ui-builder"],
                source="app-planner",
            )
            self.assertEqual(second["decisions"], 2)
            self.assertEqual(second["selected_total"], 3)
            self.assertEqual(second["skills"]["ui-builder"], 2)
            self.assertEqual(second["sources"], {"app-planner": 1, "factory-router": 1})

            report = skill_routing_report(
                root,
                installed_skills=["factory-router", "ui-builder", "security-review"],
            )
            self.assertEqual(report["skills"]["security-review"], 0)
            self.assertEqual(report["never_selected"], ["security-review"])
            self.assertTrue(report["advisory_only"])
            self.assertFalse(report["used_for_backend_learning"])
            self.assertFalse(report["automatic_delete_recommendation"])

    def test_invalid_source_empty_selection_and_invalid_slugs_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(ValueError):
                record_skill_routing(root, skills=["factory-router"], source="unknown")
            with self.assertRaises(ValueError):
                record_skill_routing(root, skills=[], source="manual")
            for slug in ("-bad", "bad-", "bad_slug", "A" * 65):
                with self.assertRaises(ValueError, msg=slug):
                    normalize_skill_name(slug)

    def test_cardinality_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skills = [f"skill-{index:02d}" for index in range(65)]
            with self.assertRaisesRegex(ValueError, "cardinality"):
                record_skill_routing(root, skills=skills, source="manual")

    def test_untrusted_persisted_state_is_sanitized(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = skill_routing_path(root)
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    {
                        "schema_version": 999,
                        "decisions": 999999,
                        "skills": {
                            "factory-router": 3,
                            "bad_slug": 100,
                            "ui-builder": -1,
                            "security-review": "7",
                        },
                        "sources": {
                            "factory-router": 2,
                            "unknown": 100,
                            "manual": -1,
                        },
                        "updated_at": "not-a-date",
                        "prompt": "must never survive sanitization",
                    }
                ),
                encoding="utf-8",
            )
            state = read_skill_routing_state(root)
            self.assertEqual(state["schema_version"], 1)
            self.assertEqual(state["skills"], {"factory-router": 3})
            self.assertEqual(state["sources"], {"factory-router": 2})
            self.assertEqual(state["decisions"], 2)
            self.assertEqual(state["selected_total"], 3)
            self.assertNotIn("prompt", state)
            self.assertNotIn("updated_at", state)

    def test_missing_malformed_and_non_object_state_return_empty(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(read_skill_routing_state(root), empty_skill_routing_state())
            path = skill_routing_path(root)
            path.parent.mkdir(parents=True)
            path.write_text("{not json", encoding="utf-8")
            self.assertEqual(read_skill_routing_state(root), empty_skill_routing_state())
            path.write_text("[]", encoding="utf-8")
            self.assertEqual(read_skill_routing_state(root), empty_skill_routing_state())

    def test_cli_records_reports_and_rejects_unknown_installed_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            record = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "--root",
                    str(root),
                    "record",
                    "--skill",
                    "factory-router",
                    "--skill",
                    "app-planner",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(record.returncode, 0, msg=record.stderr or record.stdout)
            payload = json.loads(record.stdout)
            self.assertTrue(payload["recorded"])
            self.assertEqual(payload["state"]["selected_total"], 2)

            report = subprocess.run(
                [sys.executable, str(CLI), "--root", str(root), "report"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(report.returncode, 0, msg=report.stderr or report.stdout)
            report_payload = json.loads(report.stdout)
            self.assertEqual(report_payload["decisions"], 1)
            self.assertIn("security-review", report_payload["never_selected"])

            unknown = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "--root",
                    str(root),
                    "record",
                    "--skill",
                    "made-up-skill",
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(unknown.returncode, 1)
            self.assertIn("unknown installed Skill", unknown.stdout)


if __name__ == "__main__":
    unittest.main()
