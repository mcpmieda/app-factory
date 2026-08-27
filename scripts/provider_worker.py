#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.provider_runtime import (  # noqa: E402
    ProviderTaskRequest,
    SubprocessRunner,
    execute_provider_task,
    redact_text,
)
from engine.providers import AntigravityAdapter, OpenCodeOllamaAdapter  # noqa: E402


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def load_request(path: Path) -> ProviderTaskRequest:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("provider request must be a JSON object")
    return ProviderTaskRequest.from_mapping(raw)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Safe App Factory local/headless provider worker runtime"
    )
    sub = root.add_subparsers(dest="command", required=True)

    validate = sub.add_parser(
        "validate", help="Validate a provider task request without executing it"
    )
    validate.add_argument("spec", type=Path)

    for command in ("probe", "command", "run"):
        item = sub.add_parser(
            command,
            help={
                "probe": "Probe provider health without running a task",
                "command": "Show the redacted fixed-argv invocation for a task",
                "run": "Execute, validate, commit, and publish a worker branch",
            }[command],
        )
        item.add_argument(
            "--provider", choices=("antigravity", "opencode_ollama"), required=True
        )
        item.add_argument("--binary")
        item.add_argument("--model")
        item.add_argument("--agent")
        item.add_argument("--effort", choices=("low", "medium", "high"))
        item.add_argument("--ollama-binary")
        item.add_argument("--ollama-base-url")
        item.add_argument(
            "--profile-home",
            type=Path,
            help="Dedicated provider profile directory; never use the normal user profile",
        )
        if command in {"command", "run"}:
            item.add_argument("spec", type=Path)
        if command == "run":
            item.add_argument(
                "--publish",
                action="store_true",
                help="Required: push the validated worker branch so completion is durable in GitHub",
            )
    return root


def build_adapter(args: argparse.Namespace):
    if args.provider == "antigravity":
        profile = args.profile_home or (
            Path(os.environ["ANTIGRAVITY_PROFILE_HOME"])
            if os.environ.get("ANTIGRAVITY_PROFILE_HOME")
            else None
        )
        return AntigravityAdapter(
            binary=args.binary or os.environ.get("ANTIGRAVITY_BIN", "agy"),
            model=args.model or os.environ.get("ANTIGRAVITY_MODEL") or None,
            effort=args.effort or os.environ.get("ANTIGRAVITY_EFFORT") or None,
            agent=args.agent or os.environ.get("ANTIGRAVITY_AGENT") or None,
            profile_home=profile,
        )
    profile = args.profile_home or (
        Path(os.environ["OPENCODE_PROFILE_HOME"])
        if os.environ.get("OPENCODE_PROFILE_HOME")
        else None
    )
    return OpenCodeOllamaAdapter(
        model=args.model or os.environ.get("OPENCODE_OLLAMA_MODEL", ""),
        binary=args.binary or os.environ.get("OPENCODE_BIN", "opencode"),
        ollama_binary=args.ollama_binary or os.environ.get("OLLAMA_BIN", "ollama"),
        agent=args.agent or os.environ.get("OPENCODE_AGENT") or None,
        ollama_base_url=(
            args.ollama_base_url
            or os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        ),
        profile_home=profile,
    )


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "validate":
            request = load_request(args.spec)
            emit({"valid": True, "request": request.to_dict()})
            return 0
        adapter = build_adapter(args)
        runner = SubprocessRunner()
        if args.command == "probe":
            health = adapter.probe(runner)
            emit(health.to_dict())
            return 0 if health.status == "healthy" else 2
        request = load_request(args.spec)
        if args.command == "command":
            emit({
                "request": request.to_dict(),
                "invocation": adapter.build_invocation(request).to_dict(),
            })
            return 0
        if args.command == "run":
            if not args.publish:
                raise ValueError("run requires --publish; local-only completion is forbidden")
            result = execute_provider_task(
                adapter, request, runner=runner, publish=True
            )
            emit(result.to_dict())
            return 0 if result.completed else 2
    except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as error:
        emit({"valid": False, "error": redact_text(error)})
        return 1
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
