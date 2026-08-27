from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.provider_worker import (
    DEFAULT_OPENCODE_AGENT,
    DEFAULT_OPENCODE_AGENT_PROMPT,
    _agent_tool_frontmatter,
    _prepare_default_opencode_agent,
)


class ProviderWorkerAgentTests(unittest.TestCase):
    def test_default_agent_mirrors_request_tool_surface_inside_isolated_profile(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            profile = Path(raw) / "profile"
            profile.mkdir()
            agent = _prepare_default_opencode_agent(
                profile,
                None,
                tool_surface={
                    "write": True,
                    "read": False,
                    "edit": False,
                    "bash": False,
                },
            )
            agent_file = (
                profile
                / "factory-config"
                / "agents"
                / f"{DEFAULT_OPENCODE_AGENT}.md"
            )
            content = agent_file.read_text(encoding="utf-8")

        self.assertEqual(agent, DEFAULT_OPENCODE_AGENT)
        self.assertIn("mode: primary", content)
        self.assertIn(DEFAULT_OPENCODE_AGENT_PROMPT, content)
        self.assertIn("tools:", content)
        self.assertIn("  write: true", content)
        self.assertIn("  read: false", content)
        self.assertIn("  edit: false", content)
        self.assertIn("  bash: false", content)
        self.assertNotIn("permission:", content)

    def test_agent_tool_frontmatter_is_deterministic_and_validated(self) -> None:
        rendered = _agent_tool_frontmatter(
            {"write": True, "read": False, "bash": False}
        )
        self.assertEqual(
            rendered,
            "tools:\n  bash: false\n  read: false\n  write: true",
        )
        with self.assertRaises(ValueError):
            _agent_tool_frontmatter({})
        with self.assertRaises(ValueError):
            _agent_tool_frontmatter({"../write": True})
        with self.assertRaises(ValueError):
            _agent_tool_frontmatter({"write": 1})

    def test_explicit_trusted_agent_is_preserved_without_writing_profile_file(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            profile = Path(raw) / "profile"
            profile.mkdir()
            agent = _prepare_default_opencode_agent(profile, "operator-agent")

            self.assertEqual(agent, "operator-agent")
            self.assertFalse((profile / "factory-config").exists())

    def test_automatic_agent_requires_request_specific_tools(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            profile = Path(raw) / "profile"
            profile.mkdir()
            with self.assertRaisesRegex(ValueError, "request-specific tools"):
                _prepare_default_opencode_agent(profile, None)

    def test_invalid_explicit_agent_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            profile = Path(raw) / "profile"
            profile.mkdir()
            for value in ("../agent", " agent", "-agent", "agent name", "/agent"):
                with self.subTest(value=value), self.assertRaises(ValueError):
                    _prepare_default_opencode_agent(profile, value)


if __name__ == "__main__":
    unittest.main()
