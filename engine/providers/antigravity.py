from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from engine.provider_runtime import (
    CommandResult,
    CommandRunner,
    ProviderHealth,
    ProviderInvocation,
    ProviderRunOutput,
    ProviderTaskRequest,
    redact_text,
)


class AntigravityAdapter:
    provider_id = "antigravity"

    def __init__(
        self,
        *,
        binary: str = "agy",
        model: str | None = None,
        effort: str | None = None,
        agent: str | None = None,
        profile_home: Path | None = None,
    ) -> None:
        self.binary = binary
        self.model = model
        self.effort = effort
        self.agent = agent
        self.profile_home = profile_home.expanduser().resolve() if profile_home else None
        if effort not in {None, "low", "medium", "high"}:
            raise ValueError("Antigravity effort must be low, medium, or high")

    @classmethod
    def from_environment(cls) -> "AntigravityAdapter":
        return cls(
            binary=os.environ.get("ANTIGRAVITY_BIN", "agy"),
            model=os.environ.get("ANTIGRAVITY_MODEL") or None,
            effort=os.environ.get("ANTIGRAVITY_EFFORT") or None,
            agent=os.environ.get("ANTIGRAVITY_AGENT") or None,
            profile_home=(
                Path(os.environ["ANTIGRAVITY_PROFILE_HOME"])
                if os.environ.get("ANTIGRAVITY_PROFILE_HOME")
                else None
            ),
        )

    def profile_environment(self) -> dict[str, str]:
        if self.profile_home is None:
            raise ValueError(
                "Antigravity automatic execution requires ANTIGRAVITY_PROFILE_HOME"
            )
        if not self.profile_home.is_dir():
            raise ValueError(f"Antigravity profile home does not exist: {self.profile_home}")
        return {
            "HOME": str(self.profile_home),
            "USERPROFILE": str(self.profile_home),
            "APPDATA": str(self.profile_home / "AppData" / "Roaming"),
            "LOCALAPPDATA": str(self.profile_home / "AppData" / "Local"),
            "XDG_CONFIG_HOME": str(self.profile_home / "xdg" / "config"),
            "XDG_DATA_HOME": str(self.profile_home / "xdg" / "data"),
            "XDG_CACHE_HOME": str(self.profile_home / "xdg" / "cache"),
            "XDG_STATE_HOME": str(self.profile_home / "xdg" / "state"),
        }

    def validate_workspace(self, request: ProviderTaskRequest) -> None:
        request.validate()
        if self.profile_home is None:
            raise ValueError(
                "Antigravity automatic execution requires ANTIGRAVITY_PROFILE_HOME"
            )
        try:
            self.profile_home.relative_to(request.worktree.resolve())
        except ValueError:
            return
        raise ValueError("Antigravity profile home must be outside the provider worktree")

    def probe(self, runner: CommandRunner) -> ProviderHealth:
        try:
            profile_environment = self.profile_environment()
        except ValueError as error:
            return ProviderHealth(
                provider_id=self.provider_id,
                status="unavailable",
                reason=str(error),
            )
        if shutil.which(self.binary) is None:
            return ProviderHealth(
                provider_id=self.provider_id,
                status="unavailable",
                reason=f"Antigravity CLI binary not found: {self.binary}",
            )
        version = runner.run(ProviderInvocation(
            provider_id=self.provider_id,
            argv=(self.binary, "--version"),
            cwd=_probe_cwd(),
            timeout_seconds=30,
            env=profile_environment,
        ))
        if version.returncode != 0:
            return ProviderHealth(
                provider_id=self.provider_id,
                status="unavailable",
                reason=version.stderr or version.stdout or "Antigravity version probe failed",
            )
        models = runner.run(ProviderInvocation(
            provider_id=self.provider_id,
            argv=(self.binary, "models"),
            cwd=_probe_cwd(),
            timeout_seconds=60,
            env=profile_environment,
        ))
        if models.returncode != 0:
            return ProviderHealth(
                provider_id=self.provider_id,
                status="degraded",
                reason=(
                    models.stderr
                    or models.stdout
                    or "Antigravity is installed but authentication/model discovery failed"
                ),
                details={"version": version.stdout.strip() or version.stderr.strip()},
            )
        if self.model and self.model not in models.stdout:
            return ProviderHealth(
                provider_id=self.provider_id,
                status="unavailable",
                reason=f"Configured Antigravity model is not available: {self.model}",
                details={"version": version.stdout.strip() or version.stderr.strip()},
            )
        return ProviderHealth(
            provider_id=self.provider_id,
            status="healthy",
            reason="Antigravity CLI, isolated cached authentication, and model discovery are available.",
            details={"version": version.stdout.strip() or version.stderr.strip()},
        )

    def build_invocation(self, request: ProviderTaskRequest) -> ProviderInvocation:
        self.validate_workspace(request)
        prompt = request.worker_prompt()
        argv: list[str] = [self.binary, "-p", prompt, "--output-format", "json"]
        if self.model:
            argv.extend(("--model", self.model))
        if self.effort:
            argv.extend(("--effort", self.effort))
        if self.agent:
            argv.extend(("--agent", self.agent))
        return ProviderInvocation(
            provider_id=self.provider_id,
            argv=tuple(argv),
            cwd=request.worktree,
            timeout_seconds=request.timeout_seconds,
            env=self.profile_environment(),
            sensitive_argument_indexes=frozenset({2}),
        )

    def parse_output(self, result: CommandResult) -> ProviderRunOutput:
        payload = _last_json_object(result.stdout)
        raw_status = str(payload.get("status") or "").upper()
        status = "success" if result.returncode == 0 and raw_status == "SUCCESS" else "failed"
        if raw_status in {"CANCELED", "CANCELLED"}:
            status = "canceled"
        elif raw_status == "INTERRUPTED":
            status = "interrupted"
        error = payload.get("error") or (result.stderr if result.returncode else None)
        return ProviderRunOutput(
            provider_id=self.provider_id,
            status=status,
            response=str(payload.get("response") or ""),
            session_id=str(payload.get("conversation_id") or "") or None,
            usage=payload.get("usage") if isinstance(payload.get("usage"), dict) else {},
            error=redact_text(error) if error else None,
        )


def _probe_cwd() -> Path:
    return Path.cwd()


def _last_json_object(stdout: str) -> dict[str, Any]:
    try:
        value = json.loads(stdout)
    except json.JSONDecodeError:
        value = None
    if isinstance(value, dict):
        return value
    for line in reversed(stdout.splitlines()):
        text = line.strip()
        if not text:
            continue
        try:
            value = json.loads(text)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            return value
    return {}
