#!/usr/bin/env python3
from __future__ import annotations

import argparse
import http.client
import json
import os
import sys
import tempfile
import threading
import urllib.parse
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.ollama_tool_proxy import (  # noqa: E402
    TOOL_GENERATION_MAX_TOKENS,
    TOOL_GENERATION_SEED,
    TOOL_GENERATION_TEMPERATURE,
    canonical_native_tool_sse,
    canonical_stop_sse,
    native_chat_url,
    native_single_tool_request,
    validate_loopback_base_url,
)

MAX_REQUEST_BYTES = 2 * 1024 * 1024
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
SENSITIVE_HEADERS = frozenset({"authorization", "proxy-authorization", "x-api-key"})
TOOL_CONTRACT_REASON_BY_MESSAGE = {
    "chat request must be a JSON object": "tool_payload",
    "chat request requires messages": "tool_messages",
    "required-tool proxy requires a non-empty tool list": "tool_count",
    "required-tool proxy accepts only function tools": "tool_type",
    "required-tool proxy requires exactly one expected function tool": "tool_name",
    "required-tool proxy rejects conflicting tool_choice": "tool_choice",
    "native chat request requires a model": "tool_model",
    "native chat request requires messages": "tool_messages",
    "native chat request messages must be objects": "tool_messages",
    "native chat request contains an unsupported message role": "tool_messages",
    "native chat request message content must be text": "tool_messages",
}
RESPONSE_CONTRACT_STAGE_BY_MESSAGE = {
    "native response must be a JSON object": "payload",
    "native response requires a model": "model",
    "native response must be complete": "done",
    "native response requires an assistant message": "assistant_message",
    "native response message role must be assistant": "assistant_role",
    "native response requires exactly one tool call": "tool_call_count",
    "native response tool call must be an object": "tool_type",
    "native response returned an unexpected function tool": "tool_name",
    "native response tool arguments must be an object": "arguments",
}
RESPONSE_CONTRACT_STAGES = frozenset({
    "encoding",
    "json",
    "payload",
    "model",
    "done",
    "assistant_message",
    "assistant_role",
    "tool_call_count",
    "tool_type",
    "tool_name",
    "arguments",
    "unknown",
})
REJECT_REASONS = frozenset({
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
    *TOOL_CONTRACT_REASON_BY_MESSAGE.values(),
    "tool_contract",
})


def safe_response_contract_stage(error: ValueError) -> str:
    """Return a bounded diagnostic code without exposing upstream response content."""
    return RESPONSE_CONTRACT_STAGE_BY_MESSAGE.get(str(error), "unknown")


@dataclass
class ProxyAudit:
    expected_tool: str
    accepted: int = 0
    rejected: int = 0
    rewritten: int = 0
    forwarded: int = 0
    upstream_errors: int = 0
    tools_received: int = 0
    tools_discarded: int = 0
    upstream_tool_calls: int = 0
    responses_normalized: int = 0
    post_tool_requests: int = 0
    post_tool_completions: int = 0
    last_status: int | None = None
    last_reject_reason: str | None = None
    last_response_contract_stage: str | None = None
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "schema_version": 3,
                "expected_tool": self.expected_tool,
                "upstream_protocol": "ollama_native_chat",
                "accepted": self.accepted,
                "rejected": self.rejected,
                "rewritten": self.rewritten,
                "forwarded": self.forwarded,
                "upstream_errors": self.upstream_errors,
                "tools_received": self.tools_received,
                "tools_discarded": self.tools_discarded,
                "upstream_tool_calls": self.upstream_tool_calls,
                "responses_normalized": self.responses_normalized,
                "post_tool_requests": self.post_tool_requests,
                "post_tool_completions": self.post_tool_completions,
                "last_status": self.last_status,
                "last_reject_reason": self.last_reject_reason,
                "last_response_contract_stage": self.last_response_contract_stage,
                "generation_temperature": TOOL_GENERATION_TEMPERATURE,
                "generation_seed": TOOL_GENERATION_SEED,
                "generation_max_tokens": TOOL_GENERATION_MAX_TOKENS,
            }

    def mutate(self, **updates: Any) -> None:
        with self._lock:
            for name, value in updates.items():
                if name in {
                    "last_status",
                    "last_reject_reason",
                    "last_response_contract_stage",
                }:
                    setattr(self, name, value)
                else:
                    setattr(self, name, getattr(self, name) + value)


def write_audit(path: Path | None, audit: ProxyAudit) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(audit.snapshot(), sort_keys=True, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(payload)
        temporary = Path(handle.name)
    os.replace(temporary, path)


class RequiredToolProxyServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        server_address: tuple[str, int],
        *,
        upstream_base_url: str,
        expected_tool: str,
        audit_file: Path | None = None,
    ) -> None:
        host, _ = server_address
        if host not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("tool proxy must bind to loopback")
        self.upstream_base_url = validate_loopback_base_url(upstream_base_url)
        self.upstream_native_chat_url = native_chat_url(self.upstream_base_url)
        parsed_upstream = urllib.parse.urlparse(self.upstream_native_chat_url)
        if parsed_upstream.hostname not in {"127.0.0.1", "localhost", "::1"}:
            raise ValueError("validated tool proxy upstream stopped being loopback")
        self.upstream_host = parsed_upstream.hostname
        self.upstream_port = parsed_upstream.port or 80
        self.upstream_path = parsed_upstream.path
        self.expected_tool = expected_tool
        if not expected_tool or any(char.isspace() for char in expected_tool):
            raise ValueError("expected tool name is invalid")
        self.audit = ProxyAudit(expected_tool=expected_tool)
        self.audit_file = audit_file
        super().__init__(server_address, RequiredToolProxyHandler)
        write_audit(self.audit_file, self.audit)


class RequiredToolProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server: RequiredToolProxyServer

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        return

    def _reject(self, status: int, reason: str) -> None:
        if reason not in REJECT_REASONS:
            reason = "tool_contract"
        self.server.audit.mutate(
            rejected=1,
            last_status=status,
            last_reject_reason=reason,
            last_response_contract_stage=None,
        )
        write_audit(self.server.audit_file, self.server.audit)
        body = b'{"error":"required-tool proxy rejected request"}\n'
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)
        self.close_connection = True

    def _send_sse(self, event_stream: bytes) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(event_stream)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(event_stream)
        self.wfile.flush()
        self.close_connection = True

    def do_GET(self) -> None:  # noqa: N802
        self._reject(405, "method")

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/chat/completions":
            self._reject(404, "path")
            return
        if any(name.lower() in SENSITIVE_HEADERS for name in self.headers.keys()):
            self._reject(400, "sensitive_header")
            return
        if self.headers.get_content_type() != "application/json":
            self._reject(415, "content_type")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._reject(400, "content_length")
            return
        if length <= 0 or length > MAX_REQUEST_BYTES:
            self._reject(413, "content_length")
            return
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._reject(400, "json_payload")
            return
        if not isinstance(payload, dict) or payload.get("stream") is not True:
            self._reject(400, "stream_mode")
            return

        messages = payload.get("messages")
        last_message = messages[-1] if isinstance(messages, list) and messages else None
        if isinstance(last_message, dict) and last_message.get("role") == "tool":
            before = self.server.audit.snapshot()
            self.server.audit.mutate(post_tool_requests=1)
            if (
                before["responses_normalized"] != 1
                or before["upstream_tool_calls"] != 1
                or before["post_tool_completions"] != 0
                or before["rejected"] != 0
            ):
                self._reject(409, "tool_sequence")
                return
            try:
                event_stream = canonical_stop_sse(payload.get("model"))
            except ValueError:
                self._reject(400, "tool_sequence")
                return
            self.server.audit.mutate(
                post_tool_completions=1,
                last_status=200,
                last_reject_reason=None,
                last_response_contract_stage=None,
            )
            write_audit(self.server.audit_file, self.server.audit)
            self._send_sse(event_stream)
            return

        tools = payload.get("tools")
        received_tool_count = len(tools) if isinstance(tools, list) else 0
        try:
            native_request = native_single_tool_request(
                payload, expected_tool=self.server.expected_tool
            )
        except ValueError as error:
            self._reject(
                400,
                TOOL_CONTRACT_REASON_BY_MESSAGE.get(str(error), "tool_contract"),
            )
            return

        retained_tool_count = len(native_request.get("tools", []))
        self.server.audit.mutate(
            accepted=1,
            rewritten=1,
            tools_received=received_tool_count,
            tools_discarded=max(received_tool_count - retained_tool_count, 0),
            last_reject_reason=None,
            last_response_contract_stage=None,
        )
        write_audit(self.server.audit_file, self.server.audit)
        body = json.dumps(native_request, separators=(",", ":")).encode("utf-8")
        connection = http.client.HTTPConnection(
            self.server.upstream_host,
            self.server.upstream_port,
            timeout=900,
        )
        try:
            connection.request(
                "POST",
                self.server.upstream_path,
                body=body,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
            )
            response = connection.getresponse()
            status = int(response.status)
            if status < 200 or status >= 300:
                self.server.audit.mutate(
                    upstream_errors=1,
                    last_status=status,
                    last_response_contract_stage=None,
                )
                write_audit(self.server.audit_file, self.server.audit)
                self._send_upstream_error(status)
                return
            self.server.audit.mutate(forwarded=1, last_status=status)
            raw_response = response.read(MAX_RESPONSE_BYTES + 1)
        except (http.client.HTTPException, TimeoutError, OSError):
            self.server.audit.mutate(
                upstream_errors=1,
                last_status=502,
                last_response_contract_stage=None,
            )
            write_audit(self.server.audit_file, self.server.audit)
            self._send_upstream_error(502)
            return
        finally:
            connection.close()

        if len(raw_response) > MAX_RESPONSE_BYTES:
            self.server.audit.mutate(
                upstream_errors=1,
                last_status=502,
                last_reject_reason="response_size",
                last_response_contract_stage=None,
            )
            write_audit(self.server.audit_file, self.server.audit)
            self._send_upstream_error(502)
            return
        try:
            completion = json.loads(raw_response)
        except UnicodeDecodeError:
            response_stage = "encoding"
        except json.JSONDecodeError:
            response_stage = "json"
        else:
            try:
                event_stream = canonical_native_tool_sse(
                    completion, expected_tool=self.server.expected_tool
                )
            except ValueError as error:
                response_stage = safe_response_contract_stage(error)
            else:
                response_stage = None

        if response_stage is not None:
            self.server.audit.mutate(
                upstream_errors=1,
                last_status=502,
                last_reject_reason="response_contract",
                last_response_contract_stage=response_stage,
            )
            write_audit(self.server.audit_file, self.server.audit)
            self._send_upstream_error(502)
            return

        self.server.audit.mutate(
            upstream_tool_calls=1,
            responses_normalized=1,
            last_status=200,
            last_reject_reason=None,
            last_response_contract_stage=None,
        )
        write_audit(self.server.audit_file, self.server.audit)
        self._send_sse(event_stream)

    def _send_upstream_error(self, status: int) -> None:
        body = b'{"error":"local Ollama upstream failed"}\n'
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)
        self.close_connection = True


def parser() -> argparse.ArgumentParser:
    item = argparse.ArgumentParser(
        description="Fail-closed loopback bridge for one native Ollama tool call and terminal result"
    )
    item.add_argument("--listen-host", default="127.0.0.1")
    item.add_argument("--listen-port", type=int, default=11435)
    item.add_argument("--upstream", default="http://127.0.0.1:11434")
    item.add_argument("--expected-tool", required=True)
    item.add_argument("--audit-file", type=Path)
    return item


def main() -> int:
    args = parser().parse_args()
    try:
        if not 1 <= args.listen_port <= 65535:
            raise ValueError("listen port must be from 1 through 65535")
        server = RequiredToolProxyServer(
            (args.listen_host, args.listen_port),
            upstream_base_url=args.upstream,
            expected_tool=args.expected_tool,
            audit_file=args.audit_file,
        )
        print(
            f"required-tool proxy listening on {args.listen_host}:{server.server_port}; "
            "upstream=ollama-native-chat/loopback; response=canonical-sse; post-tool=single-stop; "
            f"generation=deterministic/{TOOL_GENERATION_MAX_TOKENS}; payload logging=disabled",
            flush=True,
        )
        server.serve_forever(poll_interval=0.25)
        return 0
    except (OSError, ValueError) as error:
        print(f"required-tool proxy failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
