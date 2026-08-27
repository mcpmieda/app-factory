from __future__ import annotations

import json
import urllib.parse
from typing import Any, Mapping

TOOL_GENERATION_TEMPERATURE = 0
TOOL_GENERATION_SEED = 0
TOOL_GENERATION_MAX_TOKENS = 512


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
    # Ollama's OpenAI-compatible endpoint does not guarantee enforcement of
    # tool_choice. Keep it as a compatibility hint, but completion is accepted only
    # after a real structured tool call passes canonical_single_tool_sse().
    rewritten["tool_choice"] = "required"
    # FunctionGemma can otherwise wander for thousands of tokens on a malformed
    # tool turn. Make local inference reproducible and tightly bounded without ever
    # fabricating a tool call or its arguments.
    rewritten["temperature"] = TOOL_GENERATION_TEMPERATURE
    rewritten["seed"] = TOOL_GENERATION_SEED
    rewritten["max_tokens"] = TOOL_GENERATION_MAX_TOKENS
    rewritten.pop("max_completion_tokens", None)
    return rewritten


def canonical_single_tool_sse(
    payload: Mapping[str, Any], *, expected_tool: str
) -> bytes:
    """Validate one complete Ollama/OpenAI tool call and emit one canonical SSE event.

    The function changes only transport shape. It never invents a tool name, tool-call
    id, or arguments. Object-valued arguments are serialized losslessly as JSON for
    the OpenAI-compatible streaming schema expected by the client.
    """
    if not isinstance(payload, Mapping):
        raise ValueError("completion response must be a JSON object")
    completion_id = payload.get("id")
    model = payload.get("model")
    if not isinstance(completion_id, str) or not completion_id.strip():
        raise ValueError("completion response requires an id")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("completion response requires a model")

    choices = payload.get("choices")
    if not isinstance(choices, list) or len(choices) != 1:
        raise ValueError("completion response requires exactly one choice")
    choice = choices[0]
    if not isinstance(choice, Mapping) or choice.get("finish_reason") != "tool_calls":
        raise ValueError("completion response must finish with tool_calls")
    message = choice.get("message")
    if not isinstance(message, Mapping):
        raise ValueError("completion response requires an assistant message")
    tool_calls = message.get("tool_calls")
    if not isinstance(tool_calls, list) or len(tool_calls) != 1:
        raise ValueError("completion response requires exactly one tool call")

    tool_call = tool_calls[0]
    if not isinstance(tool_call, Mapping) or tool_call.get("type") != "function":
        raise ValueError("completion response tool call must be a function")
    call_id = tool_call.get("id")
    function = tool_call.get("function")
    if not isinstance(call_id, str) or not call_id.strip():
        raise ValueError("completion response tool call requires an id")
    if not isinstance(function, Mapping) or function.get("name") != expected_tool:
        raise ValueError("completion response returned an unexpected function tool")

    arguments = function.get("arguments")
    if isinstance(arguments, Mapping):
        argument_text = json.dumps(arguments, ensure_ascii=False, separators=(",", ":"))
    elif isinstance(arguments, str):
        try:
            decoded_arguments = json.loads(arguments)
        except json.JSONDecodeError as error:
            raise ValueError("completion response tool arguments must be valid JSON") from error
        if not isinstance(decoded_arguments, Mapping):
            raise ValueError("completion response tool arguments must be a JSON object")
        argument_text = arguments
    else:
        raise ValueError("completion response tool arguments must be an object or JSON string")

    chunk: dict[str, Any] = {
        "id": completion_id,
        "object": "chat.completion.chunk",
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "index": 0,
                            "id": call_id,
                            "type": "function",
                            "function": {
                                "name": expected_tool,
                                "arguments": argument_text,
                            },
                        }
                    ],
                },
                "finish_reason": "tool_calls",
            }
        ],
    }
    created = payload.get("created")
    if isinstance(created, int) and not isinstance(created, bool):
        chunk["created"] = created
    usage = payload.get("usage")
    if isinstance(usage, Mapping):
        chunk["usage"] = dict(usage)

    event = json.dumps(chunk, ensure_ascii=False, separators=(",", ":"))
    return f"data: {event}\n\ndata: [DONE]\n\n".encode("utf-8")


def canonical_stop_sse(model: str) -> bytes:
    """Return a content-free terminal SSE after a verified tool result.

    This acknowledgement carries no task content and no tool call. It exists only to
    terminate the OpenCode agent loop after the proxy has already verified one real
    expected tool call and observed the client's corresponding tool-result turn.
    """
    clean_model = str(model or "").strip()
    if not clean_model:
        raise ValueError("post-tool stop requires a model")
    chunk = {
        "id": "chatcmpl-factory-tool-complete",
        "object": "chat.completion.chunk",
        "model": clean_model,
        "choices": [
            {
                "index": 0,
                "delta": {"role": "assistant", "content": ""},
                "finish_reason": "stop",
            }
        ],
    }
    event = json.dumps(chunk, ensure_ascii=False, separators=(",", ":"))
    return f"data: {event}\n\ndata: [DONE]\n\n".encode("utf-8")
