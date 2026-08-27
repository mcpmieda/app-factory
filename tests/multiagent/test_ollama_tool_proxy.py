from __future__ import annotations

import unittest

from engine.ollama_tool_proxy import rewrite_single_tool_request, validate_loopback_base_url


class OllamaToolProxyTests(unittest.TestCase):
    def base_payload(self):
        return {
            "model": "functiongemma:270m",
            "messages": [{"role": "user", "content": "create the file"}],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "write",
                        "description": "Write a file",
                        "parameters": {"type": "object"},
                    },
                }
            ],
            "tool_choice": "auto",
            "stream": True,
        }

    def test_filters_extra_function_tools_and_forces_expected_tool_required(self) -> None:
        payload = self.base_payload()
        payload["tools"].extend(
            [
                {
                    "type": "function",
                    "function": {
                        "name": "read",
                        "description": "Read a file",
                        "parameters": {"type": "object"},
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "bash",
                        "description": "Run a command",
                        "parameters": {"type": "object"},
                    },
                },
            ]
        )

        rewritten = rewrite_single_tool_request(payload, expected_tool="write")

        self.assertEqual(rewritten["tool_choice"], "required")
        self.assertEqual(len(rewritten["tools"]), 1)
        self.assertEqual(rewritten["tools"][0]["function"]["name"], "write")
        self.assertEqual(len(payload["tools"]), 3)
        self.assertEqual(payload["tool_choice"], "auto")

    def test_rewrites_missing_or_required_choice_without_expanding_authority(self) -> None:
        missing = self.base_payload()
        missing.pop("tool_choice")
        self.assertEqual(
            rewrite_single_tool_request(missing, expected_tool="write")["tool_choice"],
            "required",
        )

        already = self.base_payload()
        already["tool_choice"] = "required"
        self.assertEqual(
            rewrite_single_tool_request(already, expected_tool="write")["tool_choice"],
            "required",
        )

    def test_rejects_missing_duplicate_non_function_or_conflicting_expected_tool(self) -> None:
        cases = []
        zero = self.base_payload()
        zero["tools"] = []
        cases.append(zero)
        missing_expected = self.base_payload()
        missing_expected["tools"][0]["function"]["name"] = "read"
        cases.append(missing_expected)
        duplicate_expected = self.base_payload()
        duplicate_expected["tools"] = duplicate_expected["tools"] * 2
        cases.append(duplicate_expected)
        wrong_type = self.base_payload()
        wrong_type["tools"].append({"type": "web_search"})
        cases.append(wrong_type)
        missing_function = self.base_payload()
        missing_function["tools"].append({"type": "function", "function": None})
        cases.append(missing_function)
        conflicting = self.base_payload()
        conflicting["tool_choice"] = "none"
        cases.append(conflicting)
        no_messages = self.base_payload()
        no_messages["messages"] = []
        cases.append(no_messages)

        for payload in cases:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                rewrite_single_tool_request(payload, expected_tool="write")

    def test_upstream_is_strictly_credential_free_loopback_http(self) -> None:
        self.assertEqual(
            validate_loopback_base_url("http://127.0.0.1:11434/v1/"),
            "http://127.0.0.1:11434/v1",
        )
        self.assertEqual(
            validate_loopback_base_url("http://localhost:11434"),
            "http://localhost:11434",
        )
        for value in (
            "",
            "https://127.0.0.1:11434/v1",
            "http://ollama.example.com:11434/v1",
            "http://user:pass@127.0.0.1:11434/v1",
            "http://127.0.0.1:11434/api",
            "http://127.0.0.1:11434/v1?token=x",
        ):
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_loopback_base_url(value)


if __name__ == "__main__":
    unittest.main()
