from __future__ import annotations

import unittest

from scripts.ollama_tool_proxy import (
    ProxyAudit,
    REJECT_REASONS,
    TOOL_CONTRACT_REASON_BY_MESSAGE,
)


class OllamaToolProxyAuditTests(unittest.TestCase):
    def test_reject_reason_is_bounded_and_contains_no_request_content(self) -> None:
        self.assertEqual(
            REJECT_REASONS,
            {
                "method",
                "path",
                "sensitive_header",
                "content_type",
                "content_length",
                "json_payload",
                "tool_payload",
                "tool_messages",
                "tool_count",
                "tool_type",
                "tool_name",
                "tool_choice",
                "tool_contract",
            },
        )
        self.assertEqual(
            set(TOOL_CONTRACT_REASON_BY_MESSAGE.values()),
            {
                "tool_payload",
                "tool_messages",
                "tool_count",
                "tool_type",
                "tool_name",
                "tool_choice",
            },
        )
        audit = ProxyAudit(expected_tool="write")
        audit.mutate(rejected=1, last_status=400, last_reject_reason="tool_count")
        snapshot = audit.snapshot()

        self.assertEqual(snapshot["last_reject_reason"], "tool_count")
        self.assertEqual(snapshot["rejected"], 1)
        self.assertNotIn("prompt", snapshot)
        self.assertNotIn("headers", snapshot)
        self.assertNotIn("arguments", snapshot)

    def test_acceptance_can_clear_only_the_last_reason(self) -> None:
        audit = ProxyAudit(expected_tool="write", rejected=1, last_reject_reason="path")
        audit.mutate(accepted=1, rewritten=1, last_reject_reason=None)
        snapshot = audit.snapshot()

        self.assertEqual(snapshot["accepted"], 1)
        self.assertEqual(snapshot["rewritten"], 1)
        self.assertEqual(snapshot["rejected"], 1)
        self.assertIsNone(snapshot["last_reject_reason"])


if __name__ == "__main__":
    unittest.main()
