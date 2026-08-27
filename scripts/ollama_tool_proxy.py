#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.ollama_tool_proxy import RequiredToolProxyServer  # noqa: E402


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
