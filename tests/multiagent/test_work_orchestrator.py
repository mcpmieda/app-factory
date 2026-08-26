from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from engine.work_orchestrator import (
    ProviderSpec,
    WorkItem,
    build_execution_plan,
    default_worker_providers,
    eligible_providers,
    factory_run_template,
    load_factory_run,
    normalize_path_scope,
    path_scopes_conflict,
)


class WorkOrchestratorTests(unittest.TestCase):
    @staticmethod
    def task(task_id: str = "task", **overrides: object) -> dict[str, object]:
        value: dict[str, object] = {
            "id": task_id,
            "title": task_id.title(),
            "paths": [f"src/{task_id}"],
            "required_capabilities": ["reasoning", "repo_read", "repo_write"],
        }
        value.update(overrides)
        return value

    @classmethod
    def spec(cls, *tasks: dict[str, object], **overrides: object) -> dict[str, object]:
        value: dict[str, object] = {
            "schema_version": 1,
            "run_id": "test-run",
            "goal": "exercise orchestration",
            "tasks": list(tasks) or [cls.task()],
        }
        value.update(overrides)
        return value

    def test_independent_tasks_share_first_wave(self) -> None:
        plan = build_execution_plan(
            self.spec(self.task("a"), self.task("b")),
            available_provider_ids=["jules"],
            max_parallel=4,
        )
        self.assertEqual(len(plan.waves), 1)
        self.assertEqual({item.task_id for item in plan.waves[0].assignments}, {"a", "b"})

    def test_plan_serialization_includes_nested_assignments_and_blocked_tasks(self) -> None:
        plan = build_execution_plan(
            self.spec(
                self.task("a"),
                self.task(
                    "activate",
                    depends_on=["a"],
                    human_gates=["production_activation"],
                ),
            ),
            available_provider_ids=["jules"],
        )
        payload = plan.to_dict()
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["waves"][0]["assignments"][0]["task_id"], "a")
        self.assertEqual(payload["blocked"][0]["task_id"], "activate")

    def test_overlapping_paths_are_serialized(self) -> None:
        plan = build_execution_plan(
            self.spec(
                self.task("a", paths=["src/banco"]),
                self.task("b", paths=["src/banco/conselho"]),
            ),
            available_provider_ids=["jules"],
            max_parallel=4,
        )
        self.assertEqual(len(plan.waves), 2)

    def test_global_parallel_limit_creates_multiple_waves(self) -> None:
        plan = build_execution_plan(
            self.spec(self.task("a"), self.task("b")),
            available_provider_ids=["jules"],
            max_parallel=1,
        )
        self.assertEqual(len(plan.waves), 2)

    def test_provider_parallel_limit_creates_multiple_waves(self) -> None:
        providers = {
            "tiny": ProviderSpec(
                provider_id="tiny",
                cost_class="zero",
                execution_mode="test",
                capabilities=frozenset({"reasoning", "repo_read", "repo_write"}),
                max_parallel=1,
            )
        }
        plan = build_execution_plan(
            self.spec(self.task("a"), self.task("b")),
            available_provider_ids=["tiny"],
            providers=providers,
            max_parallel=4,
        )
        self.assertEqual(len(plan.waves), 2)
        self.assertTrue(all(wave.assignments[0].provider_id == "tiny" for wave in plan.waves))

    def test_dependencies_create_followup_wave(self) -> None:
        plan = build_execution_plan(
            self.spec(
                self.task("implement"),
                self.task("verify", depends_on=["implement"], paths=["tests/feature"]),
            ),
            available_provider_ids=["jules"],
            max_parallel=4,
        )
        self.assertEqual([wave.assignments[0].task_id for wave in plan.waves], ["implement", "verify"])

    def test_human_gate_blocks_task_and_dependents(self) -> None:
        plan = build_execution_plan(
            self.spec(
                self.task("activate", human_gates=["production_activation"]),
                self.task("after", depends_on=["activate"]),
            ),
            available_provider_ids=["jules"],
        )
        blocked = {item.task_id: item.status for item in plan.blocked}
        self.assertEqual(blocked["activate"], "human-required")
        self.assertEqual(blocked["after"], "blocked")
        self.assertFalse(plan.waves)

    def test_codex_is_never_automatic(self) -> None:
        plan = build_execution_plan(
            self.spec(self.task("codex-task", preferred_providers=["codex"])),
            available_provider_ids=["codex"],
            allow_metered=True,
        )
        self.assertFalse(plan.waves)
        self.assertEqual(plan.blocked[0].status, "no-provider")
        self.assertFalse(default_worker_providers()["codex"].automatic)

    def test_zero_cost_local_provider_wins_when_available(self) -> None:
        plan = build_execution_plan(
            self.spec(self.task("zero", preferred_providers=["jules"])),
            available_provider_ids=["jules", "opencode_ollama"],
        )
        self.assertEqual(plan.waves[0].assignments[0].provider_id, "opencode_ollama")

    def test_provider_filter_rejects_unknown_metered_and_incapable_options(self) -> None:
        item = WorkItem(
            task_id="x",
            title="X",
            role="verification",
            required_capabilities=frozenset({"headless_browser"}),
        )
        metered = ProviderSpec(
            provider_id="metered-auto",
            cost_class="metered",
            execution_mode="test",
            capabilities=frozenset({"headless_browser"}),
            max_parallel=1,
            automatic=True,
        )
        providers = {**default_worker_providers(), "metered-auto": metered}
        result = eligible_providers(
            item,
            available_provider_ids=["missing", "codex", "metered-auto", "jules"],
            providers=providers,
            allow_metered=False,
        )
        self.assertEqual(result, [])
        allowed = eligible_providers(
            item,
            available_provider_ids=["metered-auto"],
            providers=providers,
            allow_metered=True,
        )
        self.assertEqual([provider.provider_id for provider in allowed], ["metered-auto"])

    def test_path_normalization_and_conflicts_cover_wildcards(self) -> None:
        self.assertEqual(normalize_path_scope(" ././src\\feature/ "), "src/feature")
        self.assertEqual(normalize_path_scope("/"), "*")
        self.assertTrue(path_scopes_conflict([], ["src/a"]))
        self.assertTrue(path_scopes_conflict(["/"], ["src/a"]))
        self.assertTrue(path_scopes_conflict(["src/a"], ["src/a"]))
        self.assertFalse(path_scopes_conflict(["src/a"], ["src/b"]))

    def test_missing_and_oversized_identifiers_are_rejected(self) -> None:
        missing = self.spec(self.task("task"))
        missing["tasks"] = [{"title": "Missing ID"}]
        with self.assertRaisesRegex(ValueError, "task id is required"):
            load_factory_run(missing)

        oversized = self.spec(self.task("x" * 121))
        with self.assertRaisesRegex(ValueError, "task id is too long"):
            load_factory_run(oversized)

    def test_non_array_task_fields_are_rejected(self) -> None:
        spec = self.spec(self.task("bad", depends_on="not-an-array"))
        with self.assertRaisesRegex(ValueError, "expected an array"):
            load_factory_run(spec)

    def test_unknown_human_gate_and_invalid_metadata_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown human gates"):
            load_factory_run(self.spec(self.task("gate", human_gates=["unknown_gate"])))
        with self.assertRaisesRegex(ValueError, "metadata .* must be an object"):
            load_factory_run(self.spec(self.task("metadata", metadata="invalid")))

    def test_factory_run_can_load_from_a_json_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="factory-run-unit-") as raw:
            path = Path(raw) / "run.json"
            path.write_text(json.dumps(self.spec(self.task("file"))), encoding="utf-8")
            run_id, goal, items = load_factory_run(path)
        self.assertEqual(run_id, "test-run")
        self.assertEqual(goal, "exercise orchestration")
        self.assertEqual(items[0].task_id, "file")

    def test_non_object_file_unsupported_schema_empty_tasks_and_non_object_tasks_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="factory-run-errors-") as raw:
            path = Path(raw) / "run.json"
            path.write_text("[]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "JSON object"):
                load_factory_run(path)

        with self.assertRaisesRegex(ValueError, "Unsupported Factory Run schema_version"):
            load_factory_run(self.spec(self.task(), schema_version=999))
        with self.assertRaisesRegex(ValueError, "non-empty tasks array"):
            load_factory_run(self.spec(tasks=[]))
        with self.assertRaisesRegex(ValueError, "Every task must be an object"):
            load_factory_run(self.spec(tasks=[self.task("a"), "invalid"]))

    def test_duplicate_unknown_and_self_dependencies_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "ids must be unique"):
            load_factory_run(self.spec(self.task("dup"), self.task("dup")))
        with self.assertRaisesRegex(ValueError, "depends on unknown tasks"):
            load_factory_run(self.spec(self.task("a", depends_on=["missing"])))
        with self.assertRaisesRegex(ValueError, "cannot depend on itself"):
            load_factory_run(self.spec(self.task("a", depends_on=["a"])))

    def test_cycle_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "cycle"):
            build_execution_plan(
                self.spec(
                    self.task("a", depends_on=["b"]),
                    self.task("b", depends_on=["a"]),
                ),
                available_provider_ids=["jules"],
            )

    def test_template_is_directly_plannable(self) -> None:
        template = factory_run_template()
        plan = build_execution_plan(template, available_provider_ids=["jules"])
        self.assertEqual(plan.run_id, "project-phase-001")
        self.assertEqual(len(plan.waves), 2)


if __name__ == "__main__":
    unittest.main()
