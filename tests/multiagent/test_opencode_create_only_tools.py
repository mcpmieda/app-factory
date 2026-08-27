from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from engine.provider_runtime import ProviderTaskRequest
from engine.providers.opencode_ollama import OpenCodeOllamaAdapter


class OpenCodeCreateOnlyToolTests(unittest.TestCase):
    def test_new_file_without_commands_exposes_only_write_capability(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            worktree.mkdir()
            profile.mkdir()
            request = ProviderTaskRequest.from_mapping({
                "run_id": "create-only",
                "task_id": "evidence",
                "repository": "owner/repo",
                "worktree": str(worktree),
                "integration_branch": "factory/create-only",
                "target_branch": "main",
                "working_branch": "factory/create-only/evidence",
                "paths": ["pilots/live/result.md"],
                "instruction": "Create exactly the requested evidence file.",
                "allowed_commands": [],
            })
            config = OpenCodeOllamaAdapter(
                model="functiongemma", profile_home=profile
            ).opencode_config(request)

        visible = {name for name, enabled in config["tools"].items() if enabled}
        self.assertEqual(visible, {"write"})
        self.assertEqual(config["permission"]["edit"]["pilots/live/result.md"], "allow")
        self.assertEqual(config["permission"]["edit"][".github/**"], "deny")

    def test_existing_file_keeps_read_edit_and_search_tools_visible(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            worktree = root / "worktree"
            profile = root / "profile"
            worktree.mkdir()
            profile.mkdir()
            existing = worktree / "docs" / "result.md"
            existing.parent.mkdir()
            existing.write_text("existing\n", encoding="utf-8")
            request = ProviderTaskRequest.from_mapping({
                "run_id": "edit-existing",
                "task_id": "evidence",
                "repository": "owner/repo",
                "worktree": str(worktree),
                "integration_branch": "factory/edit-existing",
                "target_branch": "main",
                "working_branch": "factory/edit-existing/evidence",
                "paths": ["docs/result.md"],
                "instruction": "Update the requested evidence file.",
                "allowed_commands": [],
            })
            tools = OpenCodeOllamaAdapter(
                model="functiongemma", profile_home=profile
            ).tool_config(request)

        self.assertTrue(tools["write"])
        self.assertTrue(tools["edit"])
        self.assertTrue(tools["read"])
        self.assertTrue(tools["grep"])
        self.assertTrue(tools["glob"])
        self.assertTrue(tools["patch"])
        self.assertFalse(tools["bash"])


if __name__ == "__main__":
    unittest.main()
