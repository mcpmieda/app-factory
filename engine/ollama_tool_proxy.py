from __future__ import annotations

import urllib.parse
from typing import Any, Mapping


def validate_loopback_base_url(value: str) -> str:
    raw = str(value or "").strip().rstrip("/")
    parsed = urllib.parse.urlparse(raw)
    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"127.0.0.1", "localhost", "::1"}
        or parsed.username
        or parsed.password
        or parsed.params
        or parsed.query
        or parsed.fragment
        or parsed.path not in {"", "/v1"}
    ):
        raise ValueError(
            "tool proxy upstream must be credential-free loopback HTTP with optional /v1 path"
        )
    return raw


def rewrite_single_tool_request(
    payload: Mapping[str, Any], *, expected_tool: str
) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ValueError("chat request must be a JSON object")
    messages = payload.get("messages")
    if not isinstance(messages, list) or not messages:
        raise ValueError("chat request requires messages")
    tools = payload.get("tools")
    if not isinstance(tools, list) or not tools:
        raise ValueError("required-tool proxy requires a non-empty tool list")

    expected_matches: list[Mapping[str, Any]] = []
    for tool in tools:
        if not isinstance(tool, Mapping) or tool.get("type") != "function":
            raise ValueError("required-tool proxy accepts only function tools")
        function = tool.get("function")
        if not isinstance(function, Mapping):
            raise ValueError("required-tool proxy accepts only function tools")
        if function.get("name") == expected_tool:
            expected_matches.append(tool)

    if len(expected_matches) != 1:
        raise ValueError("required-tool proxy requires exactly one expected function tool")

    choice = payload.get("tool_choice", "auto")
    if choice not in {"auto", "required"}:
        raise ValueError("required-tool proxy rejects conflicting tool_choice")

    rewritten = dict(payload)
    rewritten["tools"] = [dict(expected_matches[0])]
    rewritten["tool_choice"] = "required"
    return rewritten
