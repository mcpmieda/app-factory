from __future__ import annotations

import unittest

from engine.work_orchestrator import (
    build_execution_plan,
    default_worker_providers,
    path_scopes_conflict,
)


class WorkOrchestratorTests(unittest.TestCase):
    def test_independent_tasks_share_first_wave(self) -> None:
        spec = {
            "schema_version": 1,
            "run_id": "parallel",
            "goal": "parallel work",
            "tasks": [
                {
                    "id": "a",
                    "title": "A",
                    "paths": ["src/a"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                },
                {
                    "id": "b",
                    "title": "B",
                    "paths": ["src/b"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                },
            ],
        }
        plan = build_execution_plan(spec, available_provider_ids=["jules"], max_parallel=4)
        self.assertEqual(len(plan.waves), 1)
        self.assertEqual({item.task_id for item in plan.waves[0].assignments}, {"a", "b"})

    def test_overlapping_paths_are_serialized(self) -> None:
        spec = {
            "schema_version": 1,
            "run_id": "paths",
            "goal": "avoid collisions",
            "tasks": [
                {
                    "id": "a",
                    "title": "A",
                    "paths": ["src/banco"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                },
                {
                    "id": "b",
                    "title": "B",
                    "paths": ["src/banco/conselho"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                },
            ],
        }
        plan = build_execution_plan(spec, available_provider_ids=["jules"], max_parallel=4)
        self.assertEqual(len(plan.waves), 2)

    def test_dependencies_create_followup_wave(self) -> None:
        spec = {
            "schema_version": 1,
            "run_id": "deps",
            "goal": "respect dependencies",
            "tasks": [
                {
                    "id": "implement",
                    "title": "Implement",
                    "paths": ["src/feature"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                },
                {
                    "id": "verify",
                    "title": "Verify",
                    "depends_on": ["implement"],
                    "paths": ["tests/feature"],
                    "required_capabilities": ["repo_read", "repo_write", "test"],
                },
            ],
        }
        plan = build_execution_plan(spec, available_provider_ids=["jules"], max_parallel=4)
        self.assertEqual([wave.assignments[0].task_id for wave in plan.waves], ["implement", "verify"])

    def test_human_gate_blocks_task_and_dependents(self) -> None:
        spec = {
            "schema_version": 1,
            "run_id": "human",
            "goal": "protect production",
            "tasks": [
                {
                    "id": "activate",
                    "title": "Activate production",
                    "paths": ["infra"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                    "human_gates": ["production_activation"],
                },
                {
                    "id": "after",
                    "title": "After activation",
                    "depends_on": ["activate"],
                    "paths": ["src"],
                    "required_capabilities": ["reasoning", "repo_read"],
                },
            ],
        }
        plan = build_execution_plan(spec, available_provider_ids=["jules"])
        blocked = {item.task_id: item.status for item in plan.blocked}
        self.assertEqual(blocked["activate"], "human-required")
        self.assertEqual(blocked["after"], "blocked")
        self.assertFalse(plan.waves)

    def test_codex_is_never_automatic(self) -> None:
        spec = {
            "schema_version": 1,
            "run_id": "codex",
            "goal": "no premium automatic fallback",
            "tasks": [
                {
                    "id": "task",
                    "title": "Task",
                    "paths": ["src"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                    "preferred_providers": ["codex"],
                }
            ],
        }
        plan = build_execution_plan(
            spec,
            available_provider_ids=["codex"],
            allow_metered=True,
        )
        self.assertFalse(plan.waves)
        self.assertEqual(plan.blocked[0].status, "no-provider")
        self.assertFalse(default_worker_providers()["codex"].automatic)

    def test_zero_cost_local_provider_wins_when_available(self) -> None:
        spec = {
            "schema_version": 1,
            "run_id": "zero",
            "goal": "zero-first",
            "tasks": [
                {
                    "id": "task",
                    "title": "Task",
                    "paths": ["src"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                    "preferred_providers": ["jules"],
                }
            ],
        }
        plan = build_execution_plan(
            spec,
            available_provider_ids=["jules", "opencode_ollama"],
        )
        self.assertEqual(plan.waves[0].assignments[0].provider_id, "opencode_ollama")

    def test_path_conflict_is_conservative_when_scope_missing(self) -> None:
        self.assertTrue(path_scopes_conflict([], ["src/a"]))
        self.assertFalse(path_scopes_conflict(["src/a"], ["src/b"]))

    def test_cycle_is_rejected(self) -> None:
        spec = {
            "schema_version": 1,
            "run_id": "cycle",
            "goal": "cycle",
            "tasks": [
                {"id": "a", "title": "A", "depends_on": ["b"]},
                {"id": "b", "title": "B", "depends_on": ["a"]},
            ],
        }
        with self.assertRaisesRegex(ValueError, "cycle"):
            build_execution_plan(spec, available_provider_ids=["jules"])


if __name__ == "__main__":
    unittest.main()
