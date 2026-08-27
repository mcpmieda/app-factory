from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from engine.provider_runtime import (
    CommandResult,
    CommandRunner,
    ProviderHealth,
    ProviderInvocation,
    ProviderRunOutput,
    ProviderTaskRequest,
    redact_text,
)

SAFE_GIT_COMMANDS = (
    "git status*",
    "git diff*",
    "git log*",
    "git show*",
    "git rev-parse*",
)
DENIED_GIT_COMMANDS = (
    "git add*",
    "git commit*",
    "git push*",
    "git merge*",
    "git rebase*",
    "git checkout*",
    "git switch*",
    "git reset*",
    "git clean*",
    "git branch*",
    "git tag*",
    "git update-ref*",
    "git remote*",
    "git config*",
    "git fetch*",
    "git pull*",
    "git clone*",
    "git worktree*",
    "git submodule*",
)
PROJECT_CONFIG_PATHS = (
    "opencode.json",
    "opencode.jsonc",
    ".opencode",
)


class OpenCodeOllamaAdapter:
    provider_id = "opencode_ollama"

    def __init__(
        self,
        *,
        model: str,
        binary: str = "opencode",
        ollama_binary: str = "ollama",
        agent: str | None = None,
        ollama_base_url: str = "http://localhost:11434/v1",
        profile_home: Path | None = None,
    ) -> None:
        clean_model = str(model or "").strip()
        if not clean_model:
            raise ValueError("OpenCode/Ollama requires an explicit local model")
        self.model = clean_model if "/" in clean_model else f"ollama/{clean_model}"
        if not self.model.startswith("ollama/"):
            raise ValueError("OpenCode/Ollama automatic worker accepts only the ollama provider")
        self.binary = binary
        self.ollama_binary = ollama_binary
        self.agent = agent
        self.profile_home = profile_home.expanduser().resolve() if profile_home else None
        parsed = urlparse(ollama_base_url)
        if (
            parsed.scheme not in {"http", "https"}
            or parsed.hostname not in {"localhost", "127.0.0.1", "::1"}
            or parsed.username
            or parsed.password
        ):
            raise ValueError(
                "OpenCode/Ollama automatic worker requires a credential-free loopback-only Ollama base URL"
            )
        self.ollama_base_url = ollama_base_url.rstrip("/")

    @classmethod
    def from_environment(cls) -> "OpenCodeOllamaAdapter":
        return cls(
            model=os.environ.get("OPENCODE_OLLAMA_MODEL", ""),
            binary=os.environ.get("OPENCODE_BIN", "opencode"),
            ollama_binary=os.environ.get("OLLAMA_BIN", "ollama"),
            agent=os.environ.get("OPENCODE_AGENT") or None,
            ollama_base_url=os.environ.get(
                "OLLAMA_BASE_URL", "http://localhost:11434/v1"
            ),
            profile_home=(
                Path(os.environ["OPENCODE_PROFILE_HOME"])
                if os.environ.get("OPENCODE_PROFILE_HOME")
                else None
            ),
        )

    def profile_environment(self) -> dict[str, str]:
        if self.profile_home is None:
            raise ValueError(
                "OpenCode/Ollama automatic execution requires OPENCODE_PROFILE_HOME"
            )
        if not self.profile_home.is_dir():
            raise ValueError(f"OpenCode profile home does not exist: {self.profile_home}")
        config_home = self.profile_home / "xdg" / "config"
        data_home = self.profile_home / "xdg" / "data"
        cache_home = self.profile_home / "xdg" / "cache"
        state_home = self.profile_home / "xdg" / "state"
        factory_config = self.profile_home / "factory-config"
        for directory in (config_home, data_home, cache_home, state_home, factory_config):
            directory.mkdir(parents=True, exist_ok=True)
        return {
            "HOME": str(self.profile_home),
            "USERPROFILE": str(self.profile_home),
            "APPDATA": str(self.profile_home / "AppData" / "Roaming"),
            "LOCALAPPDATA": str(self.profile_home / "AppData" / "Local"),
            "XDG_CONFIG_HOME": str(config_home),
            "XDG_DATA_HOME": str(data_home),
            "XDG_CACHE_HOME": str(cache_home),
            "XDG_STATE_HOME": str(state_home),
            "OPENCODE_CONFIG_DIR": str(factory_config),
        }

    def validate_workspace(self, request: ProviderTaskRequest) -> None:
        request.validate()
        if self.profile_home is None:
            raise ValueError(
                "OpenCode/Ollama automatic execution requires OPENCODE_PROFILE_HOME"
            )
        try:
            self.profile_home.relative_to(request.worktree.resolve())
        except ValueError:
            pass
        else:
            raise ValueError("OpenCode profile home must be outside the provider worktree")
        present = [
            relative for relative in PROJECT_CONFIG_PATHS if (request.worktree / relative).exists()
        ]
        if present:
            raise ValueError(
                "OpenCode automatic worker rejects repository-provided runtime config: "
                + ", ".join(present)
            )

    def probe(self, runner: CommandRunner) -> ProviderHealth:
        try:
            profile_environment = self.profile_environment()
        except ValueError as error:
            return ProviderHealth(
                provider_id=self.provider_id,
                status="unavailable",
                reason=str(error),
            )
        missing = [
            binary
            for binary in (self.binary, self.ollama_binary)
            if shutil.which(binary) is None
        ]
        if missing:
            return ProviderHealth(
                provider_id=self.provider_id,
                status="unavailable",
                reason="Missing local binaries: " + ", ".join(missing),
            )
        ollama = runner.run(ProviderInvocation(
            provider_id=self.provider_id,
            argv=(self.ollama_binary, "list"),
            cwd=Path.cwd(),
            timeout_seconds=60,
            env=profile_environment,
        ))
        if ollama.returncode != 0:
            return ProviderHealth(
                provider_id=self.provider_id,
                status="unavailable",
                reason=ollama.stderr or ollama.stdout or "Ollama service/model listing failed",
            )
        model_id = self.model.split("/", 1)[1]
        installed_models = {
            line.split()[0]
            for line in ollama.stdout.splitlines()
            if line.strip() and not line.lower().startswith("name ")
        }
        accepted_names = {model_id, f"{model_id}:latest"}
        if not installed_models.intersection(accepted_names):
            return ProviderHealth(
                provider_id=self.provider_id,
                status="unavailable",
                reason=f"Configured Ollama model is not installed: {model_id}",
            )
        probe_config = self._base_config(permission="deny")
        opencode = runner.run(ProviderInvocation(
            provider_id=self.provider_id,
            argv=(self.binary, "models", "ollama"),
            cwd=Path.cwd(),
            timeout_seconds=60,
            env={
                **profile_environment,
                "OPENCODE_CONFIG_CONTENT": json.dumps(
                    probe_config, separators=(",", ":")
                ),
                **self._disable_environment(),
            },
        ))
        if opencode.returncode != 0:
            return ProviderHealth(
                provider_id=self.provider_id,
                status="degraded",
                reason=(
                    opencode.stderr
                    or opencode.stdout
                    or "OpenCode could not enumerate the Ollama provider"
                ),
            )
        return ProviderHealth(
            provider_id=self.provider_id,
            status="healthy",
            reason="OpenCode, Ollama, and the configured local model are available in an isolated profile.",
            details={"model": self.model},
        )

    def permission_config(self, request: ProviderTaskRequest) -> dict[str, Any]:
        edit_rules: dict[str, str] = {"*": "deny"}
        for scope in request.normalized_paths:
            edit_rules[scope] = "allow"
            edit_rules[f"{scope}/**"] = "allow"
        # Last matching rule wins. Protected paths remain denied even if future scope logic regresses.
        for protected in (".github", "infra/factory", "infra/validation", ".git"):
            edit_rules[protected] = "deny"
            edit_rules[f"{protected}/**"] = "deny"

        bash_rules: dict[str, str] = {"*": "deny"}
        for command in (*SAFE_GIT_COMMANDS, *request.normalized_commands):
            bash_rules[command] = "allow"
        for command in DENIED_GIT_COMMANDS:
            bash_rules[command] = "deny"
        return {
            "*": "deny",
            "read": {
                "*": "allow",
                ".git": "deny",
                ".git/**": "deny",
                ".env": "deny",
                ".env.*": "deny",
                "**/.env": "deny",
                "**/.env.*": "deny",
                ".env.example": "allow",
                "**/.env.example": "allow",
            },
            "glob": "allow",
            "grep": "allow",
            "lsp": "deny",
            "edit": edit_rules,
            "bash": bash_rules,
            "external_directory": "deny",
            "webfetch": "deny",
            "websearch": "deny",
            "task": "deny",
            "skill": "deny",
            "question": "deny",
            "doom_loop": "deny",
        }

    def tool_config(self, request: ProviderTaskRequest) -> dict[str, bool]:
        """Expose only capabilities the bounded task can actually need.

        Permission remains the authoritative security boundary. For a task with no
        control-plane commands whose declared paths do not yet exist, the worker is
        creation-only: advertising a single write schema reduces local-model prompt
        cost and removes ambiguous tool choices without granting any new authority.
        """
        create_only = (
            not request.normalized_commands
            and bool(request.normalized_paths)
            and all(
                "*" not in scope and not (request.worktree / scope).exists()
                for scope in request.normalized_paths
            )
        )
        if create_only:
            return {
                "bash": False,
                "edit": False,
                "write": True,
                "read": False,
                "grep": False,
                "glob": False,
                "patch": False,
                "lsp": False,
                "skill": False,
                "todowrite": False,
                "webfetch": False,
                "websearch": False,
                "question": False,
                "task": False,
            }
        return {
            "bash": bool(request.normalized_commands),
            "edit": True,
            "write": True,
            "read": True,
            "grep": True,
            "glob": True,
            "patch": True,
            "lsp": False,
            "skill": False,
            "todowrite": False,
            "webfetch": False,
            "websearch": False,
            "question": False,
            "task": False,
        }

    def _base_config(self, *, permission: Any) -> dict[str, Any]:
        model_id = self.model.split("/", 1)[1]
        return {
            "$schema": "https://opencode.ai/config.json",
            "model": self.model,
            "enabled_providers": ["ollama"],
            "permission": permission,
            "share": "disabled",
            "autoupdate": False,
            "mcp": {},
            "plugin": [],
            "instructions": [],
            "command": {},
            "provider": {
                "ollama": {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": "Ollama (local)",
                    "options": {"baseURL": self.ollama_base_url},
                    "models": {model_id: {"name": model_id}},
                }
            },
        }

    def opencode_config(self, request: ProviderTaskRequest) -> dict[str, Any]:
        config = self._base_config(permission=self.permission_config(request))
        # OpenCode still supports its tool-visibility map. Keep permission rules as
        # the security boundary and use this map only to avoid advertising denied
        # tool schemas to bounded local models.
        config["tools"] = self.tool_config(request)
        return config

    @staticmethod
    def _disable_environment() -> dict[str, str]:
        return {
            "OPENCODE_DISABLE_AUTOUPDATE": "true",
            "OPENCODE_DISABLE_DEFAULT_PLUGINS": "true",
            "OPENCODE_DISABLE_CLAUDE_CODE": "true",
            "OPENCODE_DISABLE_MODELS_FETCH": "true",
            "OPENCODE_AUTO_SHARE": "false",
        }

    def build_invocation(self, request: ProviderTaskRequest) -> ProviderInvocation:
        self.validate_workspace(request)
        prompt = request.worker_prompt()
        argv: list[str] = [
            self.binary,
            "run",
            "--auto",
            "--format",
            "json",
            "--dir",
            str(request.worktree),
            "--model",
            self.model,
            "--title",
            f"Factory {request.run_id}/{request.task_id}",
        ]
        if self.agent:
            argv.extend(("--agent", self.agent))
        argv.append(prompt)
        return ProviderInvocation(
            provider_id=self.provider_id,
            argv=tuple(argv),
            cwd=request.worktree,
            timeout_seconds=request.timeout_seconds,
            env={
                **self.profile_environment(),
                "OPENCODE_PERMISSION": json.dumps(
                    self.permission_config(request), separators=(",", ":")
                ),
                "OPENCODE_CONFIG_CONTENT": json.dumps(
                    self.opencode_config(request), separators=(",", ":")
                ),
                **self._disable_environment(),
            },
            sensitive_argument_indexes=frozenset({len(argv) - 1}),
        )

    def parse_output(self, result: CommandResult) -> ProviderRunOutput:
        payloads = _json_objects(result.stdout)
        error = result.stderr if result.returncode else None
        session_id: str | None = None
        usage: dict[str, Any] = {}
        responses: list[str] = []
        failed_event = False
        for payload in payloads:
            session_id = session_id or _first_string(
                payload, "sessionID", "session_id", "sessionId"
            )
            if isinstance(payload.get("usage"), dict):
                usage = payload["usage"]
            text = _first_string(payload, "text", "content", "message", "response")
            if text:
                responses.append(text)
            event_type = str(payload.get("type") or payload.get("event") or "").lower()
            if event_type in {"error", "failed"}:
                failed_event = True
                error = error or _first_string(payload, "error", "message")
        status = "success" if result.returncode == 0 and not failed_event else "failed"
        return ProviderRunOutput(
            provider_id=self.provider_id,
            status=status,
            response="\n".join(responses[-3:]),
            session_id=session_id,
            usage=usage,
            error=redact_text(error) if error else None,
        )


def _json_objects(stdout: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        text = line.strip()
        if not text:
            continue
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            result.append(value)
    return result


def _first_string(value: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        item = value.get(key)
        if isinstance(item, str) and item.strip():
            return item.strip()
    return None
