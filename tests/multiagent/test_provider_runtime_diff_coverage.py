from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine.provider_runtime import ProviderTaskRequest
from engine.providers.antigravity import AntigravityAdapter, _last_json_object
from engine.providers.opencode_ollama import OpenCodeOllamaAdapter, _json_objects


class ProviderRuntimeDiffCoverageTests(unittest.TestCase):
    @staticmethod
    def request(worktree: Path) -> ProviderTaskRequest:
        return ProviderTaskRequest.from_mapping({
            "run_id": "diff-coverage",
            "task_id": "worker",
            "repository": "owner/repo",
            "worktree": str(worktree),
            "integration_branch": "factory/diff-coverage",
            "target_branch": "main",
            "working_branch": "factory/diff-coverage/worker",
            "paths": ["docs/worker"],
            "instruction": "Exercise defensive validation branches.",
        })

    def test_direct_request_rejects_relative_worktree(self) -> None:
        request = ProviderTaskRequest(
            run_id="diff-coverage",
            task_id="relative-worktree",
            repository="owner/repo",
            worktree=Path("relative-worktree"),
            integration_branch="factory/diff-coverage",
            target_branch="main",
            working_branch="factory/diff-coverage/relative-worktree",
            paths=("docs/worker",),
            instruction="Exercise the direct dataclass validation path.",
        )
        with self.assertRaisesRegex(ValueError, "absolute path"):
            request.validate()

    def test_workspace_validation_requires_isolated_profiles(self) -> None:
        with tempfile.TemporaryDirectory(prefix="provider-profile-coverage-") as raw:
            request = self.request(Path(raw).resolve())
            with self.assertRaisesRegex(ValueError, "ANTIGRAVITY_PROFILE_HOME"):
                AntigravityAdapter().validate_workspace(request)
            with self.assertRaisesRegex(ValueError, "OPENCODE_PROFILE_HOME"):
                OpenCodeOllamaAdapter(model="qwen").validate_workspace(request)

    def test_machine_readable_parsers_ignore_blank_lines(self) -> None:
        self.assertEqual(_last_json_object("\n"), {})
        self.assertEqual(_json_objects("\n"), [])


if __name__ == "__main__":
    unittest.main()
