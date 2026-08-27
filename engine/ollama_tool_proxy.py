from __future__ import annotations

import json
import os
import tempfile
import threading
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Mapping

MAX_REQUEST_BYTES = 2 * 1024 * 1024
SENSITIVE_HEADERS = frozenset({"authorization", "proxy-authorization", "x-api-key"})


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
        raise ValueError("tool proxy upstream must be credential-free loopback HTTP with optional /v1 path")
    return raw


def rewrite_single_tool_request(payload: Mapping[str, Any], *, expected_tool: str) -> dict[str, Any]:
    if not isinstance(payload, Mapping):
        raise ValueError("chat request must be a JSON object")
    messages = payload.get("messages")
    if not isinstance(messages, list) or not messages:
        raise ValueError("chat request requires messages")
    tools = payload.get("tools")
    if not isinstance(tools, list) or len(tools) != 1:
        raise ValueError("required-tool proxy accepts exactly one tool")
    tool = tools[0]
    if not isinstance(tool, Mapping) or tool.get("type") != "function":
        raise ValueError("required-tool proxy accepts one function tool")
    function = tool.get("function")
    if not isinstance(function, Mapping) or function.get("name") != expected_tool:
        raise ValueError("required-tool proxy received an unexpected function tool")
    choice = payload.get("tool_choice", "auto")
    if choice not in {"auto", "required"}:
        raise ValueError("required-tool proxy rejects conflicting tool_choice")
    rewritten = dict(payload)
    rewritten["tool_choice"] = "required"
    return rewritten


@dataclass
class ProxyAudit:
    expected_tool: str
    accepted: int = 0
    rejected: int = 0
    rewritten: int = 0
    forwarded: int = 0
    upstream_errors: int = 0
    last_status: int | None = None
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return {
                "schema_version": 1,
                "expected_tool": self.expected_tool,
                "accepted": self.accepted,
                "rejected": self.rejected,
                "rewritten": self.rewritten,
                "forwarded": self.forwarded,
                "upstream_errors": self.upstream_errors,
                "last_status": self.last_status,
            }

    def mutate(self, **increments: int) -> None:
        with self._lock:
            for name, value in increments.items():
                if name == "last_status":
                    self.last_status = value
                else:
                    setattr(self, name, getattr(self, name) + value)


def write_audit(path: Path | None, audit: ProxyAudit) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(audit.snapshot(), sort_keys=True, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
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

    def _reject(self, status: int = 400) -> None:
        self.server.audit.mutate(rejected=1, last_status=status)
        write_audit(self.server.audit_file, self.server.audit)
        body = b'{"error":"required-tool proxy rejected request"}\n'
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)
        self.close_connection = True

    def do_GET(self) -> None:  # noqa: N802
        self._reject(405)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/chat/completions":
            self._reject(404)
            return
        if any(name.lower() in SENSITIVE_HEADERS for name in self.headers.keys()):
            self._reject(400)
            return
        content_type = self.headers.get_content_type()
        if content_type != "application/json":
            self._reject(415)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._reject(400)
            return
        if length <= 0 or length > MAX_REQUEST_BYTES:
            self._reject(413)
            return
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw)
            original_choice = payload.get("tool_choice", "auto") if isinstance(payload, dict) else None
            rewritten = rewrite_single_tool_request(
                payload, expected_tool=self.server.expected_tool
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            self._reject(400)
            return

        self.server.audit.mutate(
            accepted=1,
            rewritten=1 if original_choice != "required" else 0,
        )
        write_audit(self.server.audit_file, self.server.audit)
        upstream = f"{self.server.upstream_base_url}/chat/completions"
        request = urllib.request.Request(
            upstream,
            data=json.dumps(rewritten, separators=(",", ":")).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Accept": self.headers.get("Accept", "application/json"),
            },
        )
        try:
            response = urllib.request.urlopen(request, timeout=900)
        except urllib.error.HTTPError as error:
            self.server.audit.mutate(upstream_errors=1, last_status=error.code)
            write_audit(self.server.audit_file, self.server.audit)
            self._send_upstream_error(error.code)
            return
        except (urllib.error.URLError, TimeoutError, OSError):
            self.server.audit.mutate(upstream_errors=1, last_status=502)
            write_audit(self.server.audit_file, self.server.audit)
            self._send_upstream_error(502)
            return

        with response:
            status = int(response.status)
            self.server.audit.mutate(forwarded=1, last_status=status)
            write_audit(self.server.audit_file, self.server.audit)
            self.send_response(status)
            self.send_header("Content-Type", response.headers.get("Content-Type", "application/json"))
            self.send_header("Cache-Control", "no-store")
            self.send_header("Connection", "close")
            self.end_headers()
            while True:
                chunk = response.read(64 * 1024)
                if not chunk:
                    break
                self.wfile.write(chunk)
                self.wfile.flush()
            self.close_connection = True

    def _send_upstream_error(self, status: int) -> None:
        body = b'{"error":"local Ollama upstream failed"}\n'
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(body)
        self.close_connection = True
