from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol

from engine.work_orchestrator import (
    ProviderSpec,
    WorkItem,
    default_worker_providers,
    eligible_providers,
    normalize_path_scope,
)

RUNTIME_SCHEMA_VERSION = 1
PROTECTED_PATHS = (".github", "infra/factory", "infra/validation")
HEALTH_STATES = frozenset({"healthy", "degraded", "unavailable", "unknown"})
TERMINAL_PROVIDER_STATES = frozenset({"success", "failed", "canceled", "interrupted"})
REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
BRANCH_PATTERN = re.compile(r"^[A-Za-z0-9._/-]+$")
REMOTE_PATTERN = re.compile(r"^[A-Za-z0-9._-]+$")
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SENSITIVE_PATTERN = re.compile(
    r"(?i)(token|secret|password|api[_-]?key|authorization)(\s*[:=]\s*)([^\s,;]+)"
)
URL_CREDENTIAL_PATTERN = re.compile(r"(?i)(https?://)([^/@\s:]+):([^/@\s]+)@")
TOKEN_PATTERNS = (
    re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{16,}\b", re.IGNORECASE),
)
SAFE_ENV_KEYS = frozenset({
    "PATH",
    "HOME",
    "USER",
    "USERNAME",
    "USERPROFILE",
    "LOCALAPPDATA",
    "APPDATA",
    "PROGRAMDATA",
    "SYSTEMROOT",
    "WINDIR",
    "COMSPEC",
    "PATHEXT",
    "TMP",
    "TEMP",
    "TMPDIR",
    "LANG",
    "LC_ALL",
    "TERM",
    "SHELL",
})
FORBIDDEN_COMMAND_PREFIXES = (
    "git ",
    "gh ",
    "curl ",
    "wget ",
    "ssh ",
    "scp ",
    "ftp ",
    "rm ",
    "rmdir ",
    "del ",
    "format ",
    "shutdown ",
    "bash ",
    "sh ",
    "zsh ",
    "fish ",
    "cmd ",
    "powershell ",
    "pwsh ",
    "python -c ",
    "python3 -c ",
    "node -e ",
    "node --eval ",
)
SENSITIVE_GIT_PATHS = (
    "HEAD",
    "commondir",
    "gitdir",
    "config",
    "config.worktree",
    "hooks",
    "info/attributes",
    "info/exclude",
    "objects/info/alternates",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def redact_text(value: Any, *, limit: int = 800) -> str:
    text = str(value or "")
    text = URL_CREDENTIAL_PATTERN.sub(r"\1<redacted>:<redacted>@", text)
    text = SENSITIVE_PATTERN.sub(lambda match: f"{match.group(1)}{match.group(2)}<redacted>", text)
    for pattern in TOKEN_PATTERNS:
        text = pattern.sub("<redacted>", text)
    return text[:limit]


def sanitize_value(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, Mapping):
        return {str(key): sanitize_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [sanitize_value(item) for item in value]
    return redact_text(value)


def normalize_runtime_path(value: str) -> str:
    raw = str(value or "").strip().replace("\\", "/")
    if raw.startswith("/") or re.match(r"^[A-Za-z]:/", raw):
        raise ValueError(f"automatic worker path must be repository-relative: {value}")
    normalized = normalize_path_scope(raw)
    parts = tuple(part for part in normalized.split("/") if part)
    if normalized == "*" or not parts:
        raise ValueError("automatic workers require explicit non-wildcard path scopes")
    if any(part in {".", ".."} for part in parts):
        raise ValueError(f"unsafe path scope: {value}")
    return "/".join(parts)


def path_scopes_overlap(left: str, right: str) -> bool:
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def validate_runtime_scopes(
    paths: Iterable[str], *, protected_paths: Iterable[str] = PROTECTED_PATHS
) -> tuple[str, ...]:
    normalized: list[str] = []
    protected = tuple(normalize_runtime_path(path) for path in protected_paths)
    for value in paths:
        path = normalize_runtime_path(value)
        if any(path_scopes_overlap(path, blocked) for blocked in protected):
            raise ValueError(f"automatic worker scope overlaps protected path: {path}")
        if path not in normalized:
            normalized.append(path)
    if not normalized:
        raise ValueError("automatic workers require at least one explicit path scope")
    return tuple(normalized)


def validate_changed_paths(
    changed_paths: Iterable[str],
    declared_paths: Iterable[str],
    *,
    protected_paths: Iterable[str] = PROTECTED_PATHS,
) -> tuple[str, ...]:
    scopes = validate_runtime_scopes(declared_paths, protected_paths=protected_paths)
    protected = tuple(normalize_runtime_path(path) for path in protected_paths)
    normalized: list[str] = []
    for value in changed_paths:
        path = normalize_runtime_path(value)
        if any(path_scopes_overlap(path, blocked) for blocked in protected):
            raise ValueError(f"provider changed protected path: {path}")
        if not any(path == scope or path.startswith(scope + "/") for scope in scopes):
            raise ValueError(f"provider changed path outside declared scope: {path}")
        if path not in normalized:
            normalized.append(path)
    if not normalized:
        raise ValueError("provider produced no tracked changes")
    return tuple(normalized)


def validate_branch_name(value: str, *, label: str) -> str:
    branch = str(value or "").strip()
    if (
        not branch
        or len(branch) > 200
        or not BRANCH_PATTERN.fullmatch(branch)
        or branch.startswith(("/", "-"))
        or branch.endswith(("/", "."))
        or ".." in branch
        or "@{" in branch
        or "//" in branch
    ):
        raise ValueError(f"invalid {label}: {value}")
    return branch


def validate_allowed_commands(values: Iterable[str]) -> tuple[str, ...]:
    result: list[str] = []
    for value in values:
        command = " ".join(str(value or "").strip().split())
        lowered = command.lower()
        if not command:
            continue
        if command in {"*", "**"} or lowered.startswith(FORBIDDEN_COMMAND_PREFIXES):
            raise ValueError(f"unsafe automatic worker command pattern: {command}")
        if any(token in command for token in ("\n", "\r", ";", "&", "|", "`", "$(", ">", "<")):
            raise ValueError(f"compound shell syntax is not allowed: {command}")
        if command not in result:
            result.append(command)
    return tuple(result)


@dataclass(frozen=True)
class ProviderHealth:
    provider_id: str
    status: str
    reason: str
    observed_at: str = field(default_factory=utc_now)
    details: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.status not in HEALTH_STATES:
            raise ValueError(f"invalid provider health status: {self.status}")

    @property
    def usable(self) -> bool:
        return self.status in {"healthy", "degraded"}

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider_id,
            "status": self.status,
            "reason": redact_text(self.reason),
            "observed_at": self.observed_at,
            "details": sanitize_value(self.details),
        }


@dataclass(frozen=True)
class ProviderSelection:
    provider_id: str | None
    status: str
    reason: str
    considered: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider_id,
            "status": self.status,
            "reason": self.reason,
            "considered": list(self.considered),
        }


def select_runtime_provider(
    item: WorkItem,
    *,
    available_provider_ids: Iterable[str],
    health: Mapping[str, ProviderHealth],
    providers: Mapping[str, ProviderSpec] | None = None,
    allow_metered: bool = False,
) -> ProviderSelection:
    candidates = eligible_providers(
        item,
        available_provider_ids=available_provider_ids,
        providers=providers or default_worker_providers(),
        allow_metered=allow_metered,
    )
    considered = tuple(provider.provider_id for provider in candidates)
    for desired_health in ("healthy", "degraded"):
        for provider in candidates:
            observation = health.get(provider.provider_id)
            if observation and observation.status == desired_health:
                return ProviderSelection(
                    provider_id=provider.provider_id,
                    status="selected",
                    reason=(
                        f"Selected {provider.provider_id}: {desired_health} and eligible under "
                        "zero-first capability/cost policy."
                    ),
                    considered=considered,
                )
    return ProviderSelection(
        provider_id=None,
        status="no-healthy-provider",
        reason="No automatic eligible provider reported healthy or degraded runtime state.",
        considered=considered,
    )


@dataclass(frozen=True)
class ProviderTaskRequest:
    run_id: str
    task_id: str
    repository: str
    worktree: Path
    integration_branch: str
    target_branch: str
    working_branch: str
    paths: tuple[str, ...]
    instruction: str
    allowed_commands: tuple[str, ...] = ()
    timeout_seconds: int = 1800
    remote: str = "origin"

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "ProviderTaskRequest":
        raw_paths = raw.get("paths") or ()
        raw_commands = raw.get("allowed_commands") or ()
        if not isinstance(raw_paths, (list, tuple)):
            raise ValueError("paths must be an array of repository-relative strings")
        if not isinstance(raw_commands, (list, tuple)):
            raise ValueError("allowed_commands must be an array of command patterns")
        request = cls(
            run_id=str(raw.get("run_id") or "").strip(),
            task_id=str(raw.get("task_id") or "").strip(),
            repository=str(raw.get("repository") or "").strip(),
            worktree=Path(str(raw.get("worktree") or "")).expanduser().resolve(),
            integration_branch=str(raw.get("integration_branch") or "").strip(),
            target_branch=str(raw.get("target_branch") or "").strip(),
            working_branch=str(raw.get("working_branch") or "").strip(),
            paths=tuple(str(value) for value in raw_paths),
            instruction=str(raw.get("instruction") or "").strip(),
            allowed_commands=tuple(str(value) for value in raw_commands),
            timeout_seconds=int(raw.get("timeout_seconds") or 1800),
            remote=str(raw.get("remote") or "origin").strip(),
        )
        request.validate()
        return request

    def validate(self) -> None:
        if not self.run_id or len(self.run_id) > 120:
            raise ValueError("run_id is required and must be at most 120 characters")
        if not self.task_id or len(self.task_id) > 120:
            raise ValueError("task_id is required and must be at most 120 characters")
        if not REPOSITORY_PATTERN.fullmatch(self.repository):
            raise ValueError("repository must use owner/name form")
        if not self.worktree.is_absolute():
            raise ValueError("worktree must be an absolute path")
        if not self.instruction or len(self.instruction) > 50_000:
            raise ValueError("instruction is required and must be at most 50000 characters")
        integration = validate_branch_name(self.integration_branch, label="integration branch")
        target = validate_branch_name(self.target_branch, label="target branch")
        worker = validate_branch_name(self.working_branch, label="worker branch")
        if integration == target:
            raise ValueError("integration branch must differ from target branch")
        if worker in {integration, target}:
            raise ValueError("automatic worker branch must differ from integration and target branches")
        if not 1 <= int(self.timeout_seconds) <= 7200:
            raise ValueError("timeout_seconds must be between 1 and 7200")
        if not self.remote or not REMOTE_PATTERN.fullmatch(self.remote):
            raise ValueError("invalid git remote name")
        validate_runtime_scopes(self.paths)
        validate_allowed_commands(self.allowed_commands)

    @property
    def normalized_paths(self) -> tuple[str, ...]:
        return validate_runtime_scopes(self.paths)

    @property
    def normalized_commands(self) -> tuple[str, ...]:
        return validate_allowed_commands(self.allowed_commands)

    def worker_prompt(self) -> str:
        scopes = "\n".join(f"- {path}" for path in self.normalized_paths)
        commands = (
            "\n".join(f"- {command}" for command in self.normalized_commands)
            or "- none beyond built-in read/diff commands"
        )
        return (
            f"Factory Run: {self.run_id}\n"
            f"Task: {self.task_id}\n"
            f"Repository: {self.repository}\n"
            f"Worker branch: {self.working_branch}\n"
            f"Integration branch: {self.integration_branch}\n"
            f"Target branch: {self.target_branch}\n\n"
            "Complete the task inside the current worktree. Work only in the declared paths:\n"
            f"{scopes}\n\n"
            "Allowed deterministic command patterns supplied by the trusted control plane:\n"
            f"{commands}\n\n"
            "Mandatory guardrails:\n"
            "- Never write .github, infra/factory, or infra/validation.\n"
            "- Never merge, rebase, switch to, push to, or otherwise modify the integration or target branch.\n"
            "- Never activate production, change permissions, enable synchronization, or read unrelated credentials.\n"
            "- Do not modify Git config, refs, hooks, remotes, worktrees, or repository metadata.\n"
            "- Do not push. The trusted runtime publishes the worker branch after validating the diff.\n"
            "- Leave a clean, tested implementation in the worker branch/worktree.\n\n"
            "Task instruction:\n"
            f"{self.instruction}"
        )

    def to_dict(self, *, include_instruction: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "schema_version": RUNTIME_SCHEMA_VERSION,
            "run_id": self.run_id,
            "task_id": self.task_id,
            "repository": self.repository,
            "worktree": str(self.worktree),
            "integration_branch": self.integration_branch,
            "target_branch": self.target_branch,
            "working_branch": self.working_branch,
            "paths": list(self.normalized_paths),
            "allowed_commands": list(self.normalized_commands),
            "timeout_seconds": self.timeout_seconds,
            "remote": self.remote,
        }
        if include_instruction:
            payload["instruction"] = self.instruction
        return payload


@dataclass(frozen=True)
class ProviderInvocation:
    provider_id: str
    argv: tuple[str, ...]
    cwd: Path
    timeout_seconds: int
    env: Mapping[str, str] = field(default_factory=dict)
    sensitive_argument_indexes: frozenset[int] = frozenset()

    def display_argv(self) -> list[str]:
        return [
            "<task-instruction>" if index in self.sensitive_argument_indexes else value
            for index, value in enumerate(self.argv)
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider_id,
            "argv": self.display_argv(),
            "cwd": str(self.cwd),
            "timeout_seconds": self.timeout_seconds,
            "environment_keys": sorted(self.env),
        }


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str = ""
    stderr: str = ""


class CommandRunner(Protocol):
    def run(self, invocation: ProviderInvocation) -> CommandResult: ...


class SubprocessRunner:
    def run(self, invocation: ProviderInvocation) -> CommandResult:
        environment = {
            key: value for key, value in os.environ.items() if key.upper() in SAFE_ENV_KEYS
        }
        environment.update({str(key): str(value) for key, value in invocation.env.items()})
        environment["GIT_TERMINAL_PROMPT"] = "0"
        completed = subprocess.run(
            list(invocation.argv),
            cwd=invocation.cwd,
            env=environment,
            capture_output=True,
            text=True,
            timeout=invocation.timeout_seconds,
            check=False,
            shell=False,
        )
        return CommandResult(
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )


@dataclass(frozen=True)
class ProviderRunOutput:
    provider_id: str
    status: str
    response: str = ""
    session_id: str | None = None
    usage: Mapping[str, Any] = field(default_factory=dict)
    error: str | None = None

    def __post_init__(self) -> None:
        if self.status not in TERMINAL_PROVIDER_STATES:
            raise ValueError(f"invalid provider run status: {self.status}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider_id,
            "status": self.status,
            "session_id": redact_text(self.session_id) if self.session_id else None,
            "response": redact_text(self.response),
            "usage": sanitize_value(self.usage),
            "error": redact_text(self.error) if self.error else None,
        }


@dataclass(frozen=True)
class DurableEvidence:
    branch: str
    commit_sha: str
    changed_paths: tuple[str, ...]
    pushed: bool
    start_sha: str | None = None
    pull_request_url: str | None = None

    @property
    def complete(self) -> bool:
        return bool(
            self.pushed
            and SHA_PATTERN.fullmatch(self.commit_sha)
            and self.branch
            and self.changed_paths
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "branch": self.branch,
            "commit_sha": self.commit_sha,
            "start_sha": self.start_sha,
            "changed_paths": list(self.changed_paths),
            "pushed": self.pushed,
            "pull_request_url": self.pull_request_url,
            "durable": self.complete,
        }


@dataclass(frozen=True)
class TelemetryEvent:
    run_id: str
    task_id: str
    provider_id: str
    phase: str
    outcome: str
    detail: str = ""
    observed_at: str = field(default_factory=utc_now)
    metrics: Mapping[str, int | float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": RUNTIME_SCHEMA_VERSION,
            "run_id": self.run_id,
            "task_id": self.task_id,
            "provider": self.provider_id,
            "phase": self.phase,
            "outcome": self.outcome,
            "detail": redact_text(self.detail),
            "observed_at": self.observed_at,
            "metrics": dict(self.metrics),
        }

    def to_json_line(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, sort_keys=True)


@dataclass(frozen=True)
class ProviderExecutionResult:
    output: ProviderRunOutput
    evidence: DurableEvidence | None
    telemetry: tuple[TelemetryEvent, ...]

    @property
    def completed(self) -> bool:
        return self.output.status == "success" and bool(self.evidence and self.evidence.complete)

    def to_dict(self) -> dict[str, Any]:
        return {
            "completed": self.completed,
            "output": self.output.to_dict(),
            "evidence": self.evidence.to_dict() if self.evidence else None,
            "telemetry": [event.to_dict() for event in self.telemetry],
        }


class ProviderAdapter(Protocol):
    provider_id: str

    def probe(self, runner: CommandRunner) -> ProviderHealth: ...

    def build_invocation(self, request: ProviderTaskRequest) -> ProviderInvocation: ...

    def parse_output(self, result: CommandResult) -> ProviderRunOutput: ...


class GitClient:
    def __init__(self, runner: CommandRunner, hooks_path: Path) -> None:
        self.runner = runner
        self.hooks_path = hooks_path

    def run(self, worktree: Path, *args: str, timeout_seconds: int = 120) -> CommandResult:
        result = self.runner.run(ProviderInvocation(
            provider_id="git-runtime",
            argv=(
                "git",
                "-c",
                f"core.hooksPath={self.hooks_path}",
                "-c",
                "commit.gpgSign=false",
                *args,
            ),
            cwd=worktree,
            timeout_seconds=timeout_seconds,
        ))
        if result.returncode != 0:
            raise RuntimeError(
                redact_text(result.stderr or result.stdout or f"git {' '.join(args)} failed")
            )
        return result

    def text(self, worktree: Path, *args: str) -> str:
        return self.run(worktree, *args).stdout.strip()


@dataclass(frozen=True)
class GitSecuritySnapshot:
    top_level: Path
    git_marker: str
    git_dir: Path
    common_dir: Path
    sensitive_metadata: Mapping[str, str]
    refs: Mapping[str, str]
    remote_url: str


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    if path.is_symlink():
        digest.update(b"symlink\0")
        digest.update(os.readlink(path).encode("utf-8", errors="surrogateescape"))
        return digest.hexdigest()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def _snapshot_path(path: Path) -> str:
    if not path.exists() and not path.is_symlink():
        return "missing"
    if path.is_file() or path.is_symlink():
        return f"file:{_hash_file(path)}"
    entries: list[str] = []
    for child in sorted(path.rglob("*"), key=lambda item: item.as_posix()):
        relative = child.relative_to(path).as_posix()
        if child.is_dir() and not child.is_symlink():
            entries.append(f"dir:{relative}")
        else:
            entries.append(f"file:{relative}:{_hash_file(child)}")
    return "tree:" + hashlib.sha256("\n".join(entries).encode("utf-8")).hexdigest()


def _resolve_git_path(base: Path, raw: str) -> Path:
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = base / candidate
    return candidate.resolve()


def _git_marker(worktree: Path) -> str:
    marker = worktree / ".git"
    if marker.is_symlink():
        return f"symlink:{os.readlink(marker)}"
    if marker.is_file():
        return f"file:{_hash_file(marker)}"
    if marker.is_dir():
        stat = marker.stat()
        return f"directory:{stat.st_dev}:{stat.st_ino}"
    return "missing"


def _parse_refs(raw: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in raw.splitlines():
        if "\t" not in line:
            continue
        ref, sha = line.split("\t", 1)
        if SHA_PATTERN.fullmatch(sha):
            result[ref] = sha
    return result


def take_git_security_snapshot(
    git: GitClient, request: ProviderTaskRequest
) -> GitSecuritySnapshot:
    top_level = Path(git.text(request.worktree, "rev-parse", "--show-toplevel")).resolve()
    if top_level != request.worktree.resolve():
        raise ValueError("worktree must be the repository root")
    git_dir = _resolve_git_path(request.worktree, git.text(request.worktree, "rev-parse", "--git-dir"))
    common_dir = _resolve_git_path(
        request.worktree, git.text(request.worktree, "rev-parse", "--git-common-dir")
    )
    metadata: dict[str, str] = {}
    for relative in SENSITIVE_GIT_PATHS:
        for label, root in (("git", git_dir), ("common", common_dir)):
            key = f"{label}:{relative}"
            metadata[key] = _snapshot_path(root / relative)
    refs = _parse_refs(
        git.text(
            request.worktree,
            "for-each-ref",
            "--format=%(refname)%09%(objectname)",
        )
    )
    remote_url = git.text(request.worktree, "remote", "get-url", request.remote)
    if not remote_url:
        raise ValueError(f"git remote has no URL: {request.remote}")
    return GitSecuritySnapshot(
        top_level=top_level,
        git_marker=_git_marker(request.worktree),
        git_dir=git_dir,
        common_dir=common_dir,
        sensitive_metadata=metadata,
        refs=refs,
        remote_url=remote_url,
    )


def assert_git_security_unchanged(
    snapshot: GitSecuritySnapshot,
    request: ProviderTaskRequest,
) -> None:
    if _git_marker(request.worktree) != snapshot.git_marker:
        raise ValueError("provider modified the worktree Git control entry")
    metadata: dict[str, str] = {}
    for relative in SENSITIVE_GIT_PATHS:
        for label, root in (("git", snapshot.git_dir), ("common", snapshot.common_dir)):
            metadata[f"{label}:{relative}"] = _snapshot_path(root / relative)
    if metadata != dict(snapshot.sensitive_metadata):
        raise ValueError("provider modified protected Git configuration, hooks, or metadata")


def assert_only_worker_ref_changed(
    before: Mapping[str, str], after: Mapping[str, str], working_branch: str
) -> None:
    allowed_ref = f"refs/heads/{working_branch}"
    all_refs = set(before) | set(after)
    changed = {ref for ref in all_refs if before.get(ref) != after.get(ref)}
    unexpected = changed - {allowed_ref}
    if unexpected:
        raise ValueError(
            "provider modified Git refs outside the worker branch: " + ", ".join(sorted(unexpected))
        )


def _status_paths(raw: str) -> tuple[str, ...]:
    tokens = raw.split("\0")
    paths: list[str] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        index += 1
        if not token:
            continue
        if len(token) < 4:
            raise ValueError("unable to parse provider worktree status")
        status = token[:2]
        path = token[3:]
        if path and path not in paths:
            paths.append(path)
        if "R" in status or "C" in status:
            if index >= len(tokens):
                raise ValueError("unable to parse provider rename/copy status")
            original = tokens[index]
            index += 1
            if original and original not in paths:
                paths.append(original)
    return tuple(paths)


def _nul_paths(raw: str) -> tuple[str, ...]:
    return tuple(path for path in raw.split("\0") if path)


def execute_provider_task(
    adapter: ProviderAdapter,
    request: ProviderTaskRequest,
    *,
    runner: CommandRunner | None = None,
    publish: bool = True,
) -> ProviderExecutionResult:
    request.validate()
    active_runner = runner or SubprocessRunner()
    events: list[TelemetryEvent] = []

    if not request.worktree.is_dir():
        raise ValueError(f"worktree does not exist: {request.worktree}")

    with tempfile.TemporaryDirectory(prefix="app-factory-empty-hooks-") as hooks_raw:
        git = GitClient(active_runner, Path(hooks_raw))
        branch = git.text(request.worktree, "branch", "--show-current")
        if branch != request.working_branch:
            raise ValueError(
                f"worktree branch mismatch: expected {request.working_branch}, found {branch}"
            )
        if git.text(
            request.worktree, "status", "--porcelain=v1", "-z", "--untracked-files=all"
        ):
            raise ValueError("provider worktree must be clean before execution")
        start_sha = git.text(request.worktree, "rev-parse", "HEAD")
        if not SHA_PATTERN.fullmatch(start_sha):
            raise ValueError("unable to establish starting commit SHA")
        security = take_git_security_snapshot(git, request)

        events.append(TelemetryEvent(
            run_id=request.run_id,
            task_id=request.task_id,
            provider_id=adapter.provider_id,
            phase="dispatch",
            outcome="started",
            detail=f"worker branch {request.working_branch}",
        ))
        invocation = adapter.build_invocation(request)
        command_result = active_runner.run(invocation)
        output = adapter.parse_output(command_result)
        events.append(TelemetryEvent(
            run_id=request.run_id,
            task_id=request.task_id,
            provider_id=adapter.provider_id,
            phase="provider",
            outcome=output.status,
            detail=output.error or output.response,
        ))
        if output.status != "success":
            return ProviderExecutionResult(output=output, evidence=None, telemetry=tuple(events))

        # Check control files directly before trusting the repository with another Git command.
        assert_git_security_unchanged(security, request)
        current_branch = git.text(request.worktree, "branch", "--show-current")
        if current_branch != request.working_branch:
            raise ValueError("provider changed the active branch")
        current_head = git.text(request.worktree, "rev-parse", "HEAD")
        ancestry = active_runner.run(ProviderInvocation(
            provider_id="git-runtime",
            argv=(
                "git",
                "-c",
                f"core.hooksPath={hooks_raw}",
                "merge-base",
                "--is-ancestor",
                start_sha,
                current_head,
            ),
            cwd=request.worktree,
            timeout_seconds=120,
        ))
        if ancestry.returncode != 0:
            raise ValueError("provider rewrote or detached the worker branch history")
        merge_commits = git.text(
            request.worktree, "rev-list", "--merges", f"{start_sha}..{current_head}"
        )
        if merge_commits:
            raise ValueError("provider introduced merge commits into the worker branch")

        refs_after_provider = _parse_refs(
            git.text(
                request.worktree,
                "for-each-ref",
                "--format=%(refname)%09%(objectname)",
            )
        )
        assert_only_worker_ref_changed(security.refs, refs_after_provider, request.working_branch)
        remote_url_after = git.text(request.worktree, "remote", "get-url", request.remote)
        if remote_url_after != security.remote_url:
            raise ValueError("provider modified the configured Git remote")

        status = git.text(
            request.worktree, "status", "--porcelain=v1", "-z", "--untracked-files=all"
        )
        status_paths = _status_paths(status)
        committed_paths = (
            _nul_paths(
                git.run(
                    request.worktree,
                    "diff",
                    "--name-only",
                    "-z",
                    start_sha,
                    current_head,
                ).stdout
            )
            if current_head != start_sha
            else ()
        )
        validate_changed_paths((*committed_paths, *status_paths), request.normalized_paths)

        if status:
            git.run(request.worktree, "add", "--all", "--", *request.normalized_paths)
            staged_paths = _nul_paths(
                git.run(request.worktree, "diff", "--cached", "--name-only", "-z").stdout
            )
            validate_changed_paths((*committed_paths, *staged_paths), request.normalized_paths)
            git.run(
                request.worktree,
                "commit",
                "-m",
                f"[Factory:{request.run_id}] {request.task_id}",
            )
            current_head = git.text(request.worktree, "rev-parse", "HEAD")

        changed_paths = _nul_paths(
            git.run(
                request.worktree,
                "diff",
                "--name-only",
                "-z",
                start_sha,
                current_head,
            ).stdout
        )
        changed_paths = validate_changed_paths(changed_paths, request.normalized_paths)
        if git.text(
            request.worktree, "status", "--porcelain=v1", "-z", "--untracked-files=all"
        ):
            raise ValueError("provider worktree is not clean after controlled commit")
        assert_git_security_unchanged(security, request)

        refs_before_publish = _parse_refs(
            git.text(
                request.worktree,
                "for-each-ref",
                "--format=%(refname)%09%(objectname)",
            )
        )
        assert_only_worker_ref_changed(security.refs, refs_before_publish, request.working_branch)

        pushed = False
        if publish:
            git.run(
                request.worktree,
                "push",
                security.remote_url,
                f"HEAD:refs/heads/{request.working_branch}",
                timeout_seconds=600,
            )
            remote_line = git.text(
                request.worktree,
                "ls-remote",
                security.remote_url,
                f"refs/heads/{request.working_branch}",
            )
            remote_sha = remote_line.split()[0] if remote_line else ""
            if remote_sha != current_head:
                raise ValueError("published worker branch does not match the validated commit SHA")
            pushed = True

        evidence = DurableEvidence(
            branch=request.working_branch,
            commit_sha=current_head,
            changed_paths=changed_paths,
            pushed=pushed,
            start_sha=start_sha,
        )
        events.append(TelemetryEvent(
            run_id=request.run_id,
            task_id=request.task_id,
            provider_id=adapter.provider_id,
            phase="publish",
            outcome="success" if evidence.complete else "local-only",
            detail=f"commit {current_head}; changed {len(changed_paths)} path(s)",
            metrics={"changed_paths": len(changed_paths)},
        ))
        return ProviderExecutionResult(
            output=output,
            evidence=evidence,
            telemetry=tuple(events),
        )
