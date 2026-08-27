from __future__ import annotations

import unittest

from engine.work_orchestrator import (
    MAX_AUTOMATIC_PARALLEL,
    build_execution_plan,
    default_worker_providers,
)


class ParallelGuardrailTests(unittest.TestCase):
    @staticmethod
    def spec() -> dict[str, object]:
        return {
            "schema_version": 1,
            "run_id": "parallel-guard",
            "goal": "validate hard parallel ceiling",
            "tasks": [
                {
                    "id": "a",
                    "title": "A",
                    "paths": ["src/a"],
                    "required_capabilities": ["reasoning", "repo_read", "repo_write"],
                }
            ],
        }

    def test_global_parallel_limit_is_strictly_one_to_three(self) -> None:
        self.assertEqual(MAX_AUTOMATIC_PARALLEL, 3)
        for value in (0, 4, 99):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "between 1 and 3"):
                build_execution_plan(self.spec(), available_provider_ids=["jules"], max_parallel=value)

    def test_no_builtin_automatic_provider_exceeds_three_workers(self) -> None:
        automatic = [provider for provider in default_worker_providers().values() if provider.automatic]
        self.assertTrue(automatic)
        self.assertTrue(all(1 <= provider.max_parallel <= 3 for provider in automatic))


if __name__ == "__main__":
    unittest.main()
