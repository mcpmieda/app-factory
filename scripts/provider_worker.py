#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.provider_runtime import (  # noqa: E402
    ProviderInvocation,
    ProviderTaskRequest,
    SubprocessRunner,
    execute_provider_task,
    redact_text,
    utc_now,
)
from engine.providers import AntigravityAdapter, OpenCodeOllamaAdapter  # noqa: E402

DEFAULT_OPENCODE_AGENT = "factory-worker"
AGENT_NAME_PATTERN = re.compile(r"^[A-Za-z0-9._/-]+$")
TOOL_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
MAX_STAGED_FILE_BYTES = 64 * 1024
DEFAULT_OPENCODE_AGENT_PROMPT = """You are a bounded App Factory worker.
Follow the user task literally and make only the requested scoped change.
Use only tools currently exposed by the runtime. Do not inspect unrelated files.
Do not plan aloud. If a file change is requested, call the appropriate file tool immediately.
Never use shell or Git unless that capability is explicitly exposed.
Stop as soon as the requested scoped change succeeds.
"""


def emit(value: object) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def load_request(path: Path) -> ProviderTaskRequest:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("provider request must be a JSON object")
    return ProviderTaskRequest.from_mapping(raw)


def _validated_agent_name(requested_agent: str) -> str:
    raw_agent = requested_agent
    agent = raw_agent.strip()
    parts = agent.split("/")
    if (
        raw_agent != agent
        or not AGENT_NAME_PATTERN.fullmatch(agent)
        or agent.startswith(("/", "-"))
        or agent.endswith(("/", "."))
        or "//" in agent
        or any(part in {"", ".", ".."} for part in parts)
    ):
        raise ValueError("invalid OpenCode agent identifier")
    return agent


def _agent_tool_frontmatter(tool_surface: Mapping[str, bool]) -> str:
    if not tool_surface:
        raise ValueError("automatic OpenCode agent requires an explicit tool surface")
    lines = ["tools:"]
    for name, enabled in sorted(tool_surface.items()):
        if not TOOL_NAME_PATTERN.fullmatch(name) or not isinstance(enabled, bool):
            raise ValueError("invalid automatic OpenCode agent tool surface")
        lines.append(f"  {name}: {'true' if enabled else 'false'}")
    return "\n".join(lines)


def _prepare_default_opencode_agent(
    profile: Path,
    requested_agent: str | None,
    *,
    tool_surface: Mapping[str, bool] | None = None,
) -> str:
    """Create a trusted request-specific OpenCode agent in the isolated profile.

    Explicit operator agent IDs remain supported after validation. Automatic workers
    get a fixed profile-local primary agent whose agent-level tool map exactly mirrors
    the production adapter's per-request tool visibility. The adapter permission map
    remains the authoritative path/command security boundary.
    """
    if requested_agent:
        return _validated_agent_name(requested_agent)
    if tool_surface is None:
        raise ValueError("automatic OpenCode agent requires request-specific tools")

    profile = profile.expanduser().resolve()
    agent_dir = profile / "factory-config" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    agent_file = agent_dir / f"{DEFAULT_OPENCODE_AGENT}.md"
    agent_file.write_text(
        "---\n"
        "description: Bounded App Factory automatic worker\n"
        "mode: primary\n"
        f"{_agent_tool_frontmatter(tool_surface)}\n"
        "---\n"
        f"{DEFAULT_OPENCODE_AGENT_PROMPT}",
        encoding="utf-8",
    )
    return DEFAULT_OPENCODE_AGENT


def _outside_worktree(path: Path, worktree: Path, *, label: str) -> Path:
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(worktree.resolve())
    except ValueError:
        return resolved
    raise ValueError(f"{label} must be outside the provider worktree")


def _assert_safe_staged_files(request: ProviderTaskRequest, changed_paths: tuple[str, ...]) -> None:
    root = request.worktree.resolve()
    for relative in changed_paths:
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as error:
            raise ValueError(f"staged path escaped provider worktree: {relative}") from error
        if candidate.is_symlink() or not candidate.is_file():
            raise ValueError(f"staged provider output must be a regular file: {relative}")
        size = candidate.stat().st_size
        if size <= 0 or size > MAX_STAGED_FILE_BYTES:
            raise ValueError(
                f"staged provider output must be 1..{MAX_STAGED_FILE_BYTES} bytes: {relative}"
            )
        try:
            text = candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(f"staged provider output must be UTF-8 text: {relative}") from error
        if "\x00" in text:
            raise ValueError(f"staged provider output contains NUL bytes: {relative}")
        if redact_text(text, limit=len(text) + 1) != text:
            raise ValueError(f"staged provider output matches a credential pattern: {relative}")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _stage_provider_result(
    *,
    request: ProviderTaskRequest,
    result: object,
    runner: SubprocessRunner,
    bundle_path: Path,
    record_path: Path,
) -> dict[str, object]:
    output = getattr(result, "output", None)
    evidence = getattr(result, "evidence", None)
    if output is None or output.status != "success" or evidence is None:
        detail = getattr(output, "error", None) if output is not None else None
        raise RuntimeError(detail or "provider did not produce a validated staged commit")
    if evidence.pushed:
        raise ValueError("stage-only execution must not publish the worker branch")
    if not evidence.start_sha or not evidence.commit_sha or not evidence.changed_paths:
        raise ValueError("stage-only execution did not produce complete local evidence")

    _assert_safe_staged_files(request, tuple(evidence.changed_paths))
    bundle = _outside_worktree(bundle_path, request.worktree, label="provider bundle")
    record = _outside_worktree(record_path, request.worktree, label="stage record")
    if bundle.exists() or record.exists():
        raise ValueError("stage outputs must not overwrite existing files")
    bundle.parent.mkdir(parents=True, exist_ok=True)
    record.parent.mkdir(parents=True, exist_ok=True)

    bundled = runner.run(
        ProviderInvocation(
            provider_id="git-runtime",
            argv=("git", "bundle", "create", str(bundle), request.working_branch),
            cwd=request.worktree,
            timeout_seconds=300,
        )
    )
    if bundled.returncode != 0 or not bundle.is_file() or bundle.stat().st_size <= 0:
        raise RuntimeError(redact_text(bundled.stderr or bundled.stdout or "git bundle failed"))

    payload: dict[str, object] = {
        "schema_version": 1,
        "provider": output.provider_id,
        "run_id": request.run_id,
        "task_id": request.task_id,
        "repository": request.repository,
        "integration_branch": request.integration_branch,
        "target_branch": request.target_branch,
        "working_branch": request.working_branch,
        "declared_paths": list(request.normalized_paths),
        "start_sha": evidence.start_sha,
        "commit_sha": evidence.commit_sha,
        "changed_paths": list(evidence.changed_paths),
        "bundle_sha256": _sha256_file(bundle),
        "staged_at": utc_now(),
        "github_run_id": str(os.environ.get("GITHUB_RUN_ID") or ""),
        "github_run_attempt": str(os.environ.get("GITHUB_RUN_ATTEMPT") or ""),
        "github_sha": str(os.environ.get("GITHUB_SHA") or ""),
    }
    record.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(
        description="Safe App Factory local/headless provider worker runtime"
    )
    sub = root.add_subparsers(dest="command", required=True)

    validate = sub.add_parser(
        "validate", help="Validate a provider task request without executing it"
    )
    validate.add_argument("spec", type=Path)

    for command in ("probe", "command", "run", "stage"):
        item = sub.add_parser(
            command,
            help={
                "probe": "Probe provider health without running a task",
                "command": "Show the redacted fixed-argv invocation for a task",
                "run": "Execute, validate, commit, and publish a worker branch",
                "stage": "Execute, validate, commit, and export a credential-free Git bundle",
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
        if command in {"command", "run", "stage"}:
            item.add_argument("spec", type=Path)
        if command == "run":
            item.add_argument(
                "--publish",
                action="store_true",
                help="Required: push the validated worker branch so completion is durable in GitHub",
            )
        if command == "stage":
            item.add_argument(
                "--bundle",
                type=Path,
                required=True,
                help="Output Git bundle path outside the provider worktree",
            )
            item.add_argument(
                "--record",
                type=Path,
                required=True,
                help="Output sanitized stage-record JSON path outside the provider worktree",
            )
    return root


def build_adapter(
    args: argparse.Namespace, request: ProviderTaskRequest | None = None
):
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
    requested_agent = args.agent or os.environ.get("OPENCODE_AGENT") or None
    common = {
        "model": args.model or os.environ.get("OPENCODE_OLLAMA_MODEL", ""),
        "binary": args.binary or os.environ.get("OPENCODE_BIN", "opencode"),
        "ollama_binary": args.ollama_binary or os.environ.get("OLLAMA_BIN", "ollama"),
        "ollama_base_url": (
            args.ollama_base_url
            or os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        ),
        "profile_home": profile,
    }
    if requested_agent:
        return OpenCodeOllamaAdapter(
            **common,
            agent=(
                _prepare_default_opencode_agent(profile, requested_agent)
                if profile is not None
                else _validated_agent_name(requested_agent)
            ),
        )
    if request is None:
        return OpenCodeOllamaAdapter(**common, agent=None)
    if profile is None:
        raise ValueError("automatic OpenCode execution requires an isolated profile")

    provisional = OpenCodeOllamaAdapter(**common, agent=None)
    agent = _prepare_default_opencode_agent(
        profile,
        None,
        tool_surface=provisional.tool_config(request),
    )
    return OpenCodeOllamaAdapter(**common, agent=agent)


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "validate":
            request = load_request(args.spec)
            emit({"valid": True, "request": request.to_dict()})
            return 0

        runner = SubprocessRunner()
        if args.command == "probe":
            adapter = build_adapter(args)
            health = adapter.probe(runner)
            emit(health.to_dict())
            return 0 if health.status == "healthy" else 2

        request = load_request(args.spec)
        adapter = build_adapter(args, request)
        if args.command == "command":
            emit({
                "request": request.to_dict(),
                "invocation": adapter.build_invocation(request).to_dict(),
            })
            return 0
        if args.command == "stage":
            result = execute_provider_task(adapter, request, runner=runner, publish=False)
            payload = _stage_provider_result(
                request=request,
                result=result,
                runner=runner,
                bundle_path=args.bundle,
                record_path=args.record,
            )
            emit({"staged": True, "record": payload})
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
