from __future__ import annotations

import unittest

from scripts.ollama_tool_proxy import (
    ProxyAudit,
    REJECT_REASONS,
    RESPONSE_CONTRACT_STAGE_BY_MESSAGE,
    RESPONSE_CONTRACT_STAGES,
    TOOL_CONTRACT_REASON_BY_MESSAGE,
    safe_response_contract_stage,
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
                "tool_sequence",
                "response_size",
                "response_contract",
                "tool_payload",
                "tool_messages",
                "tool_count",
                "tool_type",
                "tool_name",
                "tool_choice",
                "tool_model",
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
                "tool_model",
            },
        )
        audit = ProxyAudit(expected_tool="write")
        audit.mutate(rejected=1, last_status=400, last_reject_reason="tool_count")
        snapshot = audit.snapshot()

        self.assertEqual(snapshot["schema_version"], 3)
        self.assertEqual(snapshot["upstream_protocol"], "ollama_native_chat")
        self.assertEqual(snapshot["last_reject_reason"], "tool_count")
        self.assertIsNone(snapshot["last_response_contract_stage"])
        self.assertEqual(snapshot["generation_temperature"], 0)
        self.assertEqual(snapshot["generation_seed"], 0)
        self.assertEqual(snapshot["generation_max_tokens"], 512)
        self.assertEqual(snapshot["rejected"], 1)
        self.assertEqual(snapshot["upstream_tool_calls"], 0)
        self.assertEqual(snapshot["responses_normalized"], 0)
        self.assertEqual(snapshot["post_tool_requests"], 0)
        self.assertEqual(snapshot["post_tool_completions"], 0)
        self.assertNotIn("prompt", snapshot)
        self.assertNotIn("headers", snapshot)
        self.assertNotIn("arguments", snapshot)
        self.assertNotIn("response", snapshot)
        self.assertNotIn("tool_result", snapshot)
        self.assertNotIn("messages", snapshot)

    def test_response_contract_stage_is_bounded_and_sanitized(self) -> None:
        expected = {
            "payload",
            "model",
            "done",
            "assistant_message",
            "assistant_role",
            "tool_call_count",
            "tool_type",
            "tool_name",
            "arguments",
        }
        self.assertEqual(set(RESPONSE_CONTRACT_STAGE_BY_MESSAGE.values()), expected)
        self.assertTrue(expected.issubset(RESPONSE_CONTRACT_STAGES))
        self.assertIn("encoding", RESPONSE_CONTRACT_STAGES)
        self.assertIn("json", RESPONSE_CONTRACT_STAGES)
        self.assertIn("unknown", RESPONSE_CONTRACT_STAGES)

        for message, stage in RESPONSE_CONTRACT_STAGE_BY_MESSAGE.items():
            with self.subTest(stage=stage):
                self.assertEqual(safe_response_contract_stage(ValueError(message)), stage)

        secretish = "native response leaked content SECRET-123"
        self.assertEqual(safe_response_contract_stage(ValueError(secretish)), "unknown")
        audit = ProxyAudit(expected_tool="write")
        audit.mutate(
            upstream_errors=1,
            last_status=502,
            last_reject_reason="response_contract",
            last_response_contract_stage="tool_call_count",
        )
        snapshot = audit.snapshot()
        self.assertEqual(snapshot["last_response_contract_stage"], "tool_call_count")
        self.assertNotIn(secretish, str(snapshot))

    def test_acceptance_tracks_one_native_tool_then_one_terminal_post_tool_turn(self) -> None:
        audit = ProxyAudit(expected_tool="write")
        audit.mutate(
            accepted=1,
            rewritten=1,
            tools_received=2,
            tools_discarded=1,
            forwarded=1,
            upstream_tool_calls=1,
            responses_normalized=1,
            last_status=200,
            last_reject_reason=None,
            last_response_contract_stage=None,
        )
        audit.mutate(
            post_tool_requests=1,
            post_tool_completions=1,
            last_status=200,
            last_reject_reason=None,
            last_response_contract_stage=None,
        )
        snapshot = audit.snapshot()

        self.assertEqual(snapshot["schema_version"], 3)
        self.assertEqual(snapshot["upstream_protocol"], "ollama_native_chat")
        self.assertEqual(snapshot["accepted"], 1)
        self.assertEqual(snapshot["rewritten"], 1)
        self.assertEqual(snapshot["rejected"], 0)
        self.assertEqual(snapshot["tools_received"], 2)
        self.assertEqual(snapshot["tools_discarded"], 1)
        self.assertEqual(snapshot["forwarded"], 1)
        self.assertEqual(snapshot["upstream_tool_calls"], 1)
        self.assertEqual(snapshot["responses_normalized"], 1)
        self.assertEqual(snapshot["post_tool_requests"], 1)
        self.assertEqual(snapshot["post_tool_completions"], 1)
        self.assertEqual(snapshot["last_status"], 200)
        self.assertIsNone(snapshot["last_reject_reason"])
        self.assertIsNone(snapshot["last_response_contract_stage"])
        self.assertNotIn("tool_names", snapshot)


if __name__ == "__main__":
    unittest.main()
