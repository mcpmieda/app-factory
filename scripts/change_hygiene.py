#!/usr/bin/env python3
"""Scan a project/diff for objective change-hygiene risks.

The scanner is intentionally conservative: objective residue can block, while
heuristics (shadow copies, suppressions, CSS overrides) remain advisory unless a
project explicitly promotes them to a gate.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
SOURCE_SUFFIXES = {
    ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx",
    ".py", ".java", ".kt", ".kts", ".go", ".rs", ".rb", ".php",
    ".cs", ".cpp", ".cc", ".c", ".h", ".hpp", ".css", ".scss", ".less",
    ".vue", ".svelte", ".astro",
}
JS_LIKE_SUFFIXES = {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".svelte", ".astro"}
PYTHON_SUFFIXES = {".py"}
CSS_SUFFIXES = {".css", ".scss", ".less"}
C_STYLE_SUFFIXES = SOURCE_SUFFIXES - PYTHON_SUFFIXES
TRANSIENT_SUFFIXES = {".bak", ".orig", ".rej", ".tmp", ".temp", ".swp"}
TRANSIENT_NAMES = {"npm-debug.log", "yarn-error.log", "debug.log"}
SHADOW_SUFFIX = re.compile(
    r"(?i)(?:[-_.](?:old|new|fixed|final|copy|backup|legacy|tmp|temp|v[2-9][0-9]*))$"
)
TEMP_DEBT_RE = re.compile(
    r"(?i)(?:todo|fixme).{0,80}(?:temporary|workaround|remove|legacy|compat)|"
    r"(?:temporary|workaround).{0,80}(?:todo|fixme|remove)"
)
CONFLICT_RE = re.compile(r"^(?:<<<<<<<\s|>>>>>>>\s)", re.MULTILINE)


def git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
        timeout=30,
        shell=False,
    )


def is_git_repo(root: Path) -> bool:
    result = git(root, "rev-parse", "--is-inside-work-tree")
    return result.returncode == 0 and result.stdout.strip() == "true"


def safe_repo_path(root: Path, raw: str) -> Path | None:
    path = (root / raw).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path


def tracked_files(root: Path) -> list[str]:
    if not is_git_repo(root):
        values: list[str] = []
        for path in root.rglob("*"):
            if path.is_file() and ".git" not in path.parts:
                values.append(path.relative_to(root).as_posix())
        return sorted(values)
    result = git(root, "ls-files")
    if result.returncode != 0:
        return []
    return sorted(line for line in result.stdout.splitlines() if line.strip())


def changed_files(root: Path, base: str | None) -> tuple[list[str], str]:
    if not is_git_repo(root):
        return tracked_files(root), "repository"

    values: set[str] = set()
    if base:
        comparison = git(root, "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD")
        if comparison.returncode != 0:
            comparison = git(root, "diff", "--name-only", "--diff-filter=ACMR", base)
        if comparison.returncode == 0:
            values.update(line for line in comparison.stdout.splitlines() if line.strip())

    for args in (
        ("diff", "--name-only", "--diff-filter=ACMR"),
        ("diff", "--cached", "--name-only", "--diff-filter=ACMR"),
    ):
        result = git(root, *args)
        if result.returncode == 0:
            values.update(line for line in result.stdout.splitlines() if line.strip())

    if values:
        return sorted(values), "diff"
    return tracked_files(root), "repository"


def parse_added_lines(diff_text: str) -> dict[str, list[str]]:
    by_file: dict[str, list[str]] = {}
    current: str | None = None
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
            by_file.setdefault(current, [])
            continue
        if current and line.startswith("+") and not line.startswith("+++"):
            by_file[current].append(line[1:])
    return by_file


def added_lines(root: Path, base: str | None) -> dict[str, list[str]]:
    if not is_git_repo(root):
        return {}
    chunks: list[str] = []
    if base:
        result = git(root, "diff", "--unified=0", f"{base}...HEAD")
        if result.returncode == 0:
            chunks.append(result.stdout)
    for args in (("diff", "--unified=0"), ("diff", "--cached", "--unified=0")):
        result = git(root, *args)
        if result.returncode == 0:
            chunks.append(result.stdout)
    merged: dict[str, list[str]] = {}
    for chunk in chunks:
        for path, lines in parse_added_lines(chunk).items():
            merged.setdefault(path, []).extend(lines)
    return merged


def add_finding(target: list[dict[str, Any]], kind: str, path: str, message: str, **extra: Any) -> None:
    finding: dict[str, Any] = {"kind": kind, "path": path, "message": message}
    finding.update(extra)
    target.append(finding)


def scan_transient(path: str, blockers: list[dict[str, Any]]) -> None:
    candidate = Path(path)
    lowered = candidate.name.lower()
    if lowered in TRANSIENT_NAMES or candidate.suffix.lower() in TRANSIENT_SUFFIXES or lowered.endswith("~"):
        add_finding(
            blockers,
            "tracked-temporary-artifact",
            path,
            "Arquivo temporário/backup não deve permanecer rastreado no estado final.",
        )


def scan_shadow_copy(root: Path, path: str, tracked: set[str], advisories: list[dict[str, Any]]) -> None:
    candidate = Path(path)
    if candidate.suffix.lower() not in SOURCE_SUFFIXES:
        return
    stripped = SHADOW_SUFFIX.sub("", candidate.stem)
    if stripped == candidate.stem or not stripped:
        return
    sibling = candidate.with_name(stripped + candidate.suffix).as_posix()
    if sibling in tracked:
        add_finding(
            advisories,
            "possible-shadow-copy",
            path,
            f"Possível implementação paralela a {sibling}; confirme se há compatibilidade real ou consolide.",
            sibling=sibling,
        )


def scan_content(root: Path, path: str, blockers: list[dict[str, Any]]) -> None:
    candidate = safe_repo_path(root, path)
    if candidate is None or not candidate.is_file() or candidate.suffix.lower() not in SOURCE_SUFFIXES:
        return
    try:
        text = candidate.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return
    if CONFLICT_RE.search(text):
        add_finding(
            blockers,
            "merge-conflict-marker",
            path,
            "Marcador de conflito Git permaneceu em arquivo-fonte.",
        )


def _outside_simple_quotes(prefix: str) -> bool:
    """Cheap guard against matching directive-like strings as comments.

    This is not a language parser. It only reduces obvious false positives; the
    findings remain advisory and stack-native linters stay authoritative.
    """

    return prefix.count('"') % 2 == 0 and prefix.count("'") % 2 == 0


def comment_segment(path: str, line: str) -> str:
    suffix = Path(path).suffix.lower()
    tokens: tuple[str, ...]
    if suffix in PYTHON_SUFFIXES:
        tokens = ("#",)
    elif suffix in C_STYLE_SUFFIXES:
        tokens = ("//", "/*")
    else:
        return ""

    candidates: list[tuple[int, str]] = []
    for token in tokens:
        index = line.find(token)
        if index >= 0 and _outside_simple_quotes(line[:index]):
            candidates.append((index, line[index:]))
    if not candidates:
        return ""
    return min(candidates, key=lambda item: item[0])[1]


def suppression_marker(path: str, comment: str) -> str | None:
    suffix = Path(path).suffix.lower()
    lowered = comment.lower()
    if suffix in JS_LIKE_SUFFIXES:
        for marker in ("eslint-disable", "@ts-ignore", "@ts-expect-error"):
            if marker in lowered:
                return marker
    if suffix in CSS_SUFFIXES and "stylelint-disable" in lowered:
        return "stylelint-disable"
    if suffix in PYTHON_SUFFIXES:
        if re.search(r"#\s*noqa\b", lowered):
            return "# noqa"
        if re.search(r"#\s*type:\s*ignore\b", lowered):
            return "# type: ignore"
    if suffix in C_STYLE_SUFFIXES and "noinspection" in lowered:
        return "noinspection"
    return None


def scan_added_risks(path: str, lines: list[str], advisories: list[dict[str, Any]]) -> None:
    suffix = Path(path).suffix.lower()
    if suffix not in SOURCE_SUFFIXES:
        return

    for line_number, line in enumerate(lines, start=1):
        lowered = line.lower()
        comment = comment_segment(path, line)
        marker = suppression_marker(path, comment) if comment else None
        if marker:
            add_finding(
                advisories,
                "new-suppression",
                path,
                f"Nova suppression detectada ({marker}); prefira corrigir a causa ou justificar a exceção.",
                added_line=line_number,
            )
        if suffix in CSS_SUFFIXES and "!important" in lowered:
            add_finding(
                advisories,
                "css-important-added",
                path,
                "Novo !important pode indicar camada de override; revisar se a regra original pode ser corrigida.",
                added_line=line_number,
            )
        if comment and TEMP_DEBT_RE.search(comment):
            add_finding(
                advisories,
                "temporary-debt-marker",
                path,
                "Marcador de workaround/dívida temporária adicionado; registrar condição objetiva de remoção.",
                added_line=line_number,
            )


def detect_tooling(root: Path) -> dict[str, Any]:
    result: dict[str, Any] = {
        "javascript_typescript": False,
        "python": False,
        "lint": False,
        "knip": False,
        "stylelint": False,
        "jscpd": False,
        "ruff": False,
        "vulture": False,
    }
    package = root / "package.json"
    if package.is_file():
        result["javascript_typescript"] = True
        try:
            value = json.loads(package.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            value = {}
        deps: dict[str, Any] = {}
        for key in ("dependencies", "devDependencies", "peerDependencies"):
            current = value.get(key, {}) if isinstance(value, dict) else {}
            if isinstance(current, dict):
                deps.update(current)
        scripts = value.get("scripts", {}) if isinstance(value, dict) else {}
        result["lint"] = isinstance(scripts, dict) and "lint" in scripts
        result["knip"] = "knip" in deps or any((root / name).exists() for name in ("knip.json", "knip.jsonc", "knip.config.js", "knip.config.ts"))
        result["stylelint"] = "stylelint" in deps or any((root / name).exists() for name in ("stylelint.config.js", "stylelint.config.mjs", ".stylelintrc", ".stylelintrc.json"))
        result["jscpd"] = "jscpd" in deps or (root / ".jscpd.json").exists()

    pyproject = root / "pyproject.toml"
    requirements_text = ""
    for name in ("requirements.txt", "requirements-dev.txt"):
        requirement = root / name
        if requirement.is_file():
            try:
                requirements_text += "\n" + requirement.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                pass
    pyproject_text = ""
    if pyproject.is_file():
        try:
            pyproject_text = pyproject.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            pass
    if pyproject.is_file() or any(root.rglob("*.py")):
        result["python"] = True
    combined = (pyproject_text + requirements_text).lower()
    result["ruff"] = "ruff" in combined
    result["vulture"] = "vulture" in combined
    return result


def build_report(root: Path, base: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    files, scope = changed_files(root, base)
    tracked = set(tracked_files(root))
    additions = added_lines(root, base)
    blockers: list[dict[str, Any]] = []
    advisories: list[dict[str, Any]] = []

    for path in files:
        scan_transient(path, blockers)
        scan_shadow_copy(root, path, tracked, advisories)
        scan_content(root, path, blockers)
        scan_added_risks(path, additions.get(path, []), advisories)

    status = "fail" if blockers else ("review" if advisories else "pass")
    return {
        "schema_version": SCHEMA_VERSION,
        "root": str(root),
        "scope": scope,
        "base": base,
        "status": status,
        "files_scanned": len(files),
        "blockers": blockers,
        "advisories": advisories,
        "tooling": detect_tooling(root),
        "rules": {
            "block_objective_residue": True,
            "heuristics_are_advisory": True,
            "preserve_behavior_not_obsolete_implementation": True,
        },
    }


def render_text(report: dict[str, Any]) -> str:
    lines = [
        f"Change Hygiene: {report['status'].upper()}",
        f"Scope: {report['scope']} | files: {report['files_scanned']}",
    ]
    for label, key in (("BLOCKER", "blockers"), ("ADVISORY", "advisories")):
        for finding in report[key]:
            lines.append(f"{label}: {finding['path']}: {finding['message']}")
    tooling = ", ".join(name for name, enabled in report["tooling"].items() if enabled) or "none detected"
    lines.append(f"Tooling detected: {tooling}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="App Factory change-hygiene scanner")
    parser.add_argument("--root", default=".", help="Project/repository root")
    parser.add_argument("--base", default=None, help="Git base ref for diff-oriented signals")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--fail-on-advisory", action="store_true", help="Promote advisory findings for project-specific strict gates")
    args = parser.parse_args(argv)

    root = Path(args.root)
    if not root.is_dir():
        print(f"ERROR: root not found: {root}", file=sys.stderr)
        return 2

    report = build_report(root, args.base)
    print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else render_text(report))
    if report["blockers"]:
        return 1
    if args.fail_on_advisory and report["advisories"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
