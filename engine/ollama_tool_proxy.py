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


def native_chat_url(value: str) -> str:
    raw = validate_loopback_base_url(value)
    parsed = urllib.parse.urlparse(raw)
    return urllib.parse.urlunparse(parsed._replace(path="/api/chat"))


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
    rewritten["temperature"] = TOOL_GENERATION_TEMPERATURE
    rewritten["seed"] = TOOL_GENERATION_SEED
    rewritten["max_tokens"] = TOOL_GENERATION_MAX_TOKENS
    rewritten.pop("max_completion_tokens", None)
    return rewritten


def native_single_tool_request(
    payload: Mapping[str, Any], *, expected_tool: str
) -> dict[str, Any]:
    """Translate one validated OpenAI-compatible request to Ollama native chat.

    Only protocol shape and deterministic generation options change. Messages and the
    retained tool schema come from the real OpenCode request; no task content or tool
    arguments are invented by the shim.
    """
    filtered = rewrite_single_tool_request(payload, expected_tool=expected_tool)
    model = filtered.get("model")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("native chat request requires a model")

    source_messages = filtered.get("messages")
    if not isinstance(source_messages, list) or not source_messages:
        raise ValueError("native chat request requires messages")
    native_messages: list[dict[str, str]] = []
    for message in source_messages:
        if not isinstance(message, Mapping):
            raise ValueError("native chat request messages must be objects")
        role = message.get("role")
        content = message.get("content")
        if role not in {"system", "user", "assistant"}:
            raise ValueError("native chat request contains an unsupported message role")
        if not isinstance(content, str):
            raise ValueError("native chat request message content must be text")
        native_messages.append({"role": role, "content": content})

    return {
        "model": model,
        "messages": native_messages,
        "tools": filtered["tools"],
        "stream": False,
        "options": {
            "temperature": TOOL_GENERATION_TEMPERATURE,
            "seed": TOOL_GENERATION_SEED,
            "num_predict": TOOL_GENERATION_MAX_TOKENS,
        },
    }


def _tool_sse(
    *,
    model: str,
    completion_id: str,
    call_id: str,
    expected_tool: str,
    argument_text: str,
    usage: Mapping[str, Any] | None = None,
    created: int | None = None,
) -> bytes:
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
    if created is not None:
        chunk["created"] = created
    if usage:
        chunk["usage"] = dict(usage)
    event = json.dumps(chunk, ensure_ascii=False, separators=(",", ":"))
    return f"data: {event}\n\ndata: [DONE]\n\n".encode("utf-8")


def canonical_single_tool_sse(
    payload: Mapping[str, Any], *, expected_tool: str
) -> bytes:
    """Validate one complete OpenAI-shaped tool call and emit canonical SSE."""
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

    created = payload.get("created")
    safe_created = created if isinstance(created, int) and not isinstance(created, bool) else None
    usage = payload.get("usage")
    safe_usage = usage if isinstance(usage, Mapping) else None
    return _tool_sse(
        model=model,
        completion_id=completion_id,
        call_id=call_id,
        expected_tool=expected_tool,
        argument_text=argument_text,
        usage=safe_usage,
        created=safe_created,
    )


def canonical_native_tool_sse(
    payload: Mapping[str, Any], *, expected_tool: str
) -> bytes:
    """Validate one real native Ollama tool call and translate only transport metadata."""
    if not isinstance(payload, Mapping):
        raise ValueError("native response must be a JSON object")
    model = payload.get("model")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("native response requires a model")
    if payload.get("done") is not True:
        raise ValueError("native response must be complete")
    message = payload.get("message")
    if not isinstance(message, Mapping):
        raise ValueError("native response requires an assistant message")
    if message.get("role") != "assistant":
        raise ValueError("native response message role must be assistant")
    tool_calls = message.get("tool_calls")
    if not isinstance(tool_calls, list) or len(tool_calls) != 1:
        raise ValueError("native response requires exactly one tool call")
    tool_call = tool_calls[0]
    if not isinstance(tool_call, Mapping):
        raise ValueError("native response tool call must be an object")
    function = tool_call.get("function")
    if not isinstance(function, Mapping) or function.get("name") != expected_tool:
        raise ValueError("native response returned an unexpected function tool")
    arguments = function.get("arguments")
    if not isinstance(arguments, Mapping):
        raise ValueError("native response tool arguments must be an object")
    argument_text = json.dumps(arguments, ensure_ascii=False, separators=(",", ":"))

    prompt_tokens = payload.get("prompt_eval_count")
    completion_tokens = payload.get("eval_count")
    usage: dict[str, int] = {}
    if isinstance(prompt_tokens, int) and not isinstance(prompt_tokens, bool):
        usage["prompt_tokens"] = prompt_tokens
    if isinstance(completion_tokens, int) and not isinstance(completion_tokens, bool):
        usage["completion_tokens"] = completion_tokens
    if "prompt_tokens" in usage and "completion_tokens" in usage:
        usage["total_tokens"] = usage["prompt_tokens"] + usage["completion_tokens"]

    return _tool_sse(
        model=model,
        completion_id="chatcmpl-factory-native-tool",
        call_id="call_factory_native_tool_0",
        expected_tool=expected_tool,
        argument_text=argument_text,
        usage=usage or None,
    )


def canonical_stop_sse(model: str) -> bytes:
    """Return a content-free terminal SSE after a verified tool result."""
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
