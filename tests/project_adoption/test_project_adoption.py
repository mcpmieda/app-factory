from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.project_adoption import audit_project, initialize_project, normalize_config


ROOT = Path(__file__).resolve().parents[2]


def base_config(**overrides):
    config = {
        "factoryBaseline": "v1.4.0",
        "adoption": {"mode": "existing"},
        "routing": {
            "scale": "L",
            "risk": "medium",
            "systemLevel": "production-system",
            "profile": "web-admin",
            "apiMode": "lightweight",
            "semanticVerification": "required",
            "semanticDepth": "domain",
            "independentVerification": "adversarial",
            "authoritativeData": "shared institutional store",
            "identity": "institutional identity",
            "authorization": "server-side capabilities",
            "recovery": "versioned rollback and restore procedure",
        },
        "ui": {
            "enabled": True,
            "designSystem": "shadcn/ui",
            "professionalUiProfile": "professional-default",
            "motionProfile": "ambient",
        },
    }
    for section, values in overrides.items():
        if isinstance(values, dict) and isinstance(config.get(section), dict):
            config[section].update(values)
        else:
            config[section] = values
    return config


def write_json(path: Path, value=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value or {}, indent=2) + "\n", encoding="utf-8")


class ProjectAdoptionGateTests(unittest.TestCase):
    def test_ready_web_admin_passes_preimplementation(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            initialize_project(project, ROOT, base_config())
            write_json(project / "specs/semantic-contract.json")
            write_json(project / "specs/semantic-assurance.json")
            write_json(project / "specs/verification-plan.json")
            self.assertEqual(audit_project(project, "pre-implementation"), [])

    def test_missing_agents_is_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            initialize_project(project, ROOT, base_config())
            write_json(project / "specs/semantic-contract.json")
            write_json(project / "specs/semantic-assurance.json")
            write_json(project / "specs/verification-plan.json")
            (project / "AGENTS.md").unlink()
            issues = audit_project(project)
            self.assertIn("missing AGENTS.md durable App Factory link", issues)

    def test_web_admin_ad_hoc_css_requires_deviation(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            initialize_project(project, ROOT, base_config(ui={"designSystem": "React + CSS"}))
            write_json(project / "specs/semantic-contract.json")
            write_json(project / "specs/semantic-assurance.json")
            write_json(project / "specs/verification-plan.json")
            issues = audit_project(project)
            self.assertTrue(any("ad-hoc/native CSS" in issue for issue in issues))

    def test_heroui_has_no_forced_environmental_profile(self):
        normalized = normalize_config(base_config(ui={"designSystem": "HeroUI"}))
        self.assertEqual(normalized["ui"]["designSystem"], "HeroUI")
        self.assertNotIn("ambientSurfaceProfile", normalized["ui"])
        self.assertNotIn("constellationIntensity", normalized["ui"])

    def test_domain_semantics_must_exist_before_code(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            initialize_project(project, ROOT, base_config())
            issues = audit_project(project)
            self.assertIn("Semantic Verification required before code: missing specs/semantic-contract.json", issues)
            self.assertIn("Semantic Verification required before code: missing specs/verification-plan.json", issues)
            self.assertIn("semantic depth domain requires specs/semantic-assurance.json before code", issues)

    def test_delivery_requires_review_and_independent_verification_record(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            initialize_project(project, ROOT, base_config())
            write_json(project / "specs/semantic-contract.json")
            write_json(project / "specs/semantic-assurance.json")
            write_json(project / "specs/verification-plan.json")
            issues = audit_project(project, "delivery")
            self.assertTrue(any("review-evidence.json" in issue for issue in issues))
            self.assertTrue(any("VERIFICATION.md" in issue for issue in issues))
            write_json(project / "specs/review-evidence.json")
            (project / "VERIFICATION.md").write_text("# Verification\n", encoding="utf-8")
            self.assertEqual(audit_project(project, "delivery"), [])

    def test_legacy_starter_manifest_must_be_upgraded(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            write_json(project / ".app-factory.json", {"profile": "web-admin", "factoryBaseline": "v1.4.0"})
            (project / "AGENTS.md").write_text("App Factory factory-router PROJECT_ADOPTION_GATE.md\n", encoding="utf-8")
            (project / "PROJECT_STATE.md").write_text("## App Factory Adoption\n", encoding="utf-8")
            issues = audit_project(project)
            self.assertTrue(any("schemaVersion must be 2" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
