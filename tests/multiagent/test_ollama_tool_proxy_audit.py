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
                "stream_mode",
                "response_size",
                "response_contract",
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
        self.assertEqual(snapshot["upstream_tool_calls"], 0)
        self.assertEqual(snapshot["responses_normalized"], 0)
        self.assertNotIn("prompt", snapshot)
        self.assertNotIn("headers", snapshot)
        self.assertNotIn("arguments", snapshot)
        self.assertNotIn("response", snapshot)

    def test_acceptance_tracks_only_counts_and_response_normalization(self) -> None:
        audit = ProxyAudit(expected_tool="write", rejected=1, last_reject_reason="path")
        audit.mutate(
            accepted=1,
            rewritten=1,
            tools_received=7,
            tools_discarded=6,
            forwarded=1,
            upstream_tool_calls=1,
            responses_normalized=1,
            last_status=200,
            last_reject_reason=None,
        )
        snapshot = audit.snapshot()

        self.assertEqual(snapshot["accepted"], 1)
        self.assertEqual(snapshot["rewritten"], 1)
        self.assertEqual(snapshot["rejected"], 1)
        self.assertEqual(snapshot["tools_received"], 7)
        self.assertEqual(snapshot["tools_discarded"], 6)
        self.assertEqual(snapshot["forwarded"], 1)
        self.assertEqual(snapshot["upstream_tool_calls"], 1)
        self.assertEqual(snapshot["responses_normalized"], 1)
        self.assertEqual(snapshot["last_status"], 200)
        self.assertIsNone(snapshot["last_reject_reason"])
        self.assertNotIn("tool_names", snapshot)


if __name__ == "__main__":
    unittest.main()
