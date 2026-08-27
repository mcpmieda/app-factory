#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import threading
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.ollama_tool_proxy import (  # noqa: E402
    rewrite_single_tool_request,
    validate_loopback_base_url,
)

MAX_REQUEST_BYTES = 2 * 1024 * 1024
SENSITIVE_HEADERS = frozenset({"authorization", "proxy-authorization", "x-api-key"})
REJECT_REASONS = frozenset({
    "method",
    "path",
    "sensitive_header",
    "content_type",
    "content_length",
    "tool_contract",
})


@dataclass
class ProxyAudit:
    expected_tool: str
    accepted: int = 0
    rejected: int = 0
    rewritten: int = 0
    forwarded: int = 0
    upstream_errors: int = 0
    last_status: int | None = None
    last_reject_reason: str | None = None
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
                "last_reject_reason": self.last_reject_reason,
            }

    def mutate(self, **updates: Any) -> None:
        with self._lock:
            for name, value in updates.items():
                if name in {"last_status", "last_reject_reason"}:
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
        try:
            payload = json.loads(self.rfile.read(length))
            original_choice = (
                payload.get("tool_choice", "auto") if isinstance(payload, dict) else None
            )
            rewritten = rewrite_single_tool_request(
                payload, expected_tool=self.server.expected_tool
            )
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
            self._reject(400, "tool_contract")
            return

        self.server.audit.mutate(
            accepted=1,
            rewritten=1 if original_choice != "required" else 0,
            last_reject_reason=None,
        )
        write_audit(self.server.audit_file, self.server.audit)
        request = urllib.request.Request(
            f"{self.server.upstream_base_url}/chat/completions",
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
            self.send_header(
                "Content-Type", response.headers.get("Content-Type", "application/json")
            )
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


def parser() -> argparse.ArgumentParser:
    item = argparse.ArgumentParser(
        description="Fail-closed loopback proxy that requires one OpenAI function tool"
    )
    item.add_argument("--listen-host", default="127.0.0.1")
    item.add_argument("--listen-port", type=int, default=11435)
    item.add_argument("--upstream", default="http://127.0.0.1:11434/v1")
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
            "upstream=loopback; payload logging=disabled",
            flush=True,
        )
        server.serve_forever(poll_interval=0.25)
        return 0
    except (OSError, ValueError) as error:
        print(f"required-tool proxy failed: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
