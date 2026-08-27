from __future__ import annotations

import json
import unittest

from engine.ollama_tool_proxy import (
    canonical_single_tool_sse,
    rewrite_single_tool_request,
    validate_loopback_base_url,
)


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

    def completion_payload(self, *, arguments=None):
        if arguments is None:
            arguments = '{"filePath":"pilots/live/result.md","content":"ok\\n"}'
        return {
            "id": "chatcmpl-local-1",
            "object": "chat.completion",
            "created": 123456,
            "model": "functiongemma:270m",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "",
                        "tool_calls": [
                            {
                                "id": "call_write_1",
                                "type": "function",
                                "function": {
                                    "name": "write",
                                    "arguments": arguments,
                                },
                            }
                        ],
                    },
                    "finish_reason": "tool_calls",
                }
            ],
            "usage": {"prompt_tokens": 100, "completion_tokens": 20, "total_tokens": 120},
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

    def test_canonical_sse_preserves_one_complete_tool_call(self) -> None:
        original_arguments = '{"filePath":"pilots/live/result.md","content":"ok\\n"}'
        wire = canonical_single_tool_sse(
            self.completion_payload(arguments=original_arguments), expected_tool="write"
        ).decode("utf-8")
        events = [line.removeprefix("data: ") for line in wire.splitlines() if line.startswith("data: ")]

        self.assertEqual(events[-1], "[DONE]")
        chunk = json.loads(events[0])
        self.assertEqual(chunk["object"], "chat.completion.chunk")
        self.assertEqual(chunk["created"], 123456)
        self.assertEqual(chunk["usage"]["total_tokens"], 120)
        choice = chunk["choices"][0]
        self.assertEqual(choice["finish_reason"], "tool_calls")
        call = choice["delta"]["tool_calls"][0]
        self.assertEqual(call["id"], "call_write_1")
        self.assertEqual(call["function"]["name"], "write")
        self.assertEqual(call["function"]["arguments"], original_arguments)

    def test_canonical_sse_serializes_object_arguments_without_changing_values(self) -> None:
        arguments = {
            "filePath": "pilots/live/result.md",
            "content": "olá\n",
        }
        wire = canonical_single_tool_sse(
            self.completion_payload(arguments=arguments), expected_tool="write"
        ).decode("utf-8")
        first_event = next(
            line.removeprefix("data: ") for line in wire.splitlines() if line.startswith("data: ")
        )
        call = json.loads(first_event)["choices"][0]["delta"]["tool_calls"][0]
        self.assertEqual(json.loads(call["function"]["arguments"]), arguments)

    def test_canonical_sse_rejects_invalid_completion_shapes(self) -> None:
        cases = []
        cases.append([])
        no_id = self.completion_payload()
        no_id["id"] = ""
        cases.append(no_id)
        no_model = self.completion_payload()
        no_model["model"] = None
        cases.append(no_model)
        no_choices = self.completion_payload()
        no_choices["choices"] = []
        cases.append(no_choices)
        bad_finish = self.completion_payload()
        bad_finish["choices"][0]["finish_reason"] = "stop"
        cases.append(bad_finish)
        no_message = self.completion_payload()
        no_message["choices"][0]["message"] = None
        cases.append(no_message)
        no_calls = self.completion_payload()
        no_calls["choices"][0]["message"]["tool_calls"] = []
        cases.append(no_calls)
        bad_call_type = self.completion_payload()
        bad_call_type["choices"][0]["message"]["tool_calls"][0]["type"] = "custom"
        cases.append(bad_call_type)
        no_call_id = self.completion_payload()
        no_call_id["choices"][0]["message"]["tool_calls"][0]["id"] = ""
        cases.append(no_call_id)
        wrong_tool = self.completion_payload()
        wrong_tool["choices"][0]["message"]["tool_calls"][0]["function"]["name"] = "bash"
        cases.append(wrong_tool)
        invalid_json_args = self.completion_payload(arguments="{broken")
        cases.append(invalid_json_args)
        array_args = self.completion_payload(arguments='["not","object"]')
        cases.append(array_args)
        scalar_args = self.completion_payload(arguments=7)
        cases.append(scalar_args)

        for payload in cases:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                canonical_single_tool_sse(payload, expected_tool="write")

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
