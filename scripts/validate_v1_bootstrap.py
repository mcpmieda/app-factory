#!/usr/bin/env python3
"""Install App Factory through Codex 0.149 in a clean archive and compare origins."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CODEX_PACKAGE = "@openai/codex@0.149.0"


def run(arguments: list[str], *, cwd: Path, env: dict[str, str]) -> str:
    result = subprocess.run(
        arguments,
        cwd=cwd,
        env=env,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    return result.stdout


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    npx = shutil.which("npx.cmd" if os.name == "nt" else "npx")
    if not npx:
        raise SystemExit("ERROR: npx is required for isolated Codex bootstrap")

    with tempfile.TemporaryDirectory(prefix="app-factory-v1-bootstrap-") as raw_temp:
        temp = Path(raw_temp)
        archive = temp / "source.tar"
        source = temp / "source"
        codex_home = temp / "codex-home"
        source.mkdir()
        codex_home.mkdir()

        with archive.open("wb") as stream:
            subprocess.run(
                ["git", "archive", "--format=tar", "HEAD"],
                cwd=ROOT,
                check=True,
                stdout=stream,
            )
        with tarfile.open(archive) as bundle:
            bundle.extractall(source, filter="data")

        env = os.environ.copy()
        env["CODEX_HOME"] = str(codex_home)
        codex = [npx, "--yes", CODEX_PACKAGE, "--enable", "plugins", "plugin"]
        run(codex + ["marketplace", "add", str(source)], cwd=source, env=env)
        available = run(codex + ["list"], cwd=source, env=env)
        if "app-factory@app-factory-local" not in available:
            raise SystemExit("ERROR: App Factory was not discovered in isolated marketplace")
        run(codex + ["add", "app-factory@app-factory-local"], cwd=source, env=env)

        manifest = json.loads((source / ".codex-plugin/plugin.json").read_text("utf-8"))
        cache_root = (
            codex_home
            / "plugins"
            / "cache"
            / "app-factory-local"
            / "app-factory"
            / manifest["version"]
        )
        if not cache_root.is_dir():
            raise SystemExit("ERROR: installed plugin cache was not created")

        origin_skills = sorted((source / "skills").glob("*/SKILL.md"))
        cached_skills = sorted((cache_root / "skills").glob("*/SKILL.md"))
        origin_names = [path.parent.name for path in origin_skills]
        cached_names = [path.parent.name for path in cached_skills]
        if (
            not origin_skills
            or len(origin_names) != len(set(origin_names))
            or cached_names != origin_names
        ):
            raise SystemExit("ERROR: skills were duplicated, omitted or unexpectedly added")
        for origin in origin_skills:
            cached = cache_root / origin.relative_to(source)
            if digest(origin) != digest(cached):
                raise SystemExit(f"ERROR: divergent installed skill: {origin.parent.name}")

        router = cache_root / "skills/factory-router/SKILL.md"
        if not router.is_file():
            raise SystemExit("ERROR: factory-router was not discovered in cache")
        cache_bytes = sum(path.stat().st_size for path in cache_root.rglob("*") if path.is_file())
        if cache_bytes > 20 * 1024 * 1024:
            raise SystemExit(f"ERROR: plugin cache is unexpectedly heavy: {cache_bytes} bytes")

        print(
            "OK: isolated Codex 0.149 bootstrap installed "
            f"{len(cached_skills)} identical Skills; cache={cache_bytes} bytes; factory-router found."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
