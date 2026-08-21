from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import subprocess
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = 1
DEFAULT_MAX_BYTES = 512 * 1024
IGNORE_DIRS = {
    ".git", ".hg", ".svn", ".factory", ".idea", ".vscode", "node_modules",
    ".ssh", ".gnupg", ".aws", ".azure", ".kube",
    "vendor", "dist", "build", "out", ".next", ".nuxt", ".svelte-kit",
    "coverage", "target", ".cache", ".turbo", ".vercel", ".venv", "venv",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "playwright-report", "test-results",
}
SENSITIVE_NAMES = {
    ".env", ".envrc", ".npmrc", ".pypirc", ".netrc", ".git-credentials",
    "credentials", "credentials.json", "credentials.ini", "service-account.json",
    "id_rsa", "id_ed25519", "kubeconfig", "auth.json",
    "secrets.json", "secrets.yaml", "secrets.yml", "terraform.tfvars",
}
SENSITIVE_SUFFIXES = {
    ".pem", ".key", ".p12", ".pfx", ".jks", ".keystore", ".tfvars",
}
SENSITIVE_NAME_PARTS = ("secret", "credential")
BINARY_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".bmp", ".pdf",
    ".zip", ".gz", ".tgz", ".7z", ".rar", ".woff", ".woff2", ".ttf",
    ".otf", ".mp3", ".mp4", ".mov", ".avi", ".sqlite", ".sqlite3", ".db",
    ".exe", ".dll", ".so", ".dylib", ".class", ".jar", ".wasm",
}
LANGUAGE_BY_SUFFIX = {
    ".py": "Python", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript/React", ".jsx": "JavaScript/React",
    ".rs": "Rust", ".go": "Go", ".java": "Java", ".kt": "Kotlin", ".kts": "Kotlin",
    ".cs": "C#", ".cpp": "C++", ".cc": "C++", ".c": "C", ".h": "C/C++",
    ".php": "PHP", ".rb": "Ruby", ".swift": "Swift", ".dart": "Dart",
    ".html": "HTML", ".css": "CSS", ".scss": "SCSS", ".sass": "Sass",
    ".md": "Markdown", ".json": "JSON", ".yaml": "YAML", ".yml": "YAML",
    ".toml": "TOML", ".sql": "SQL", ".sh": "Shell", ".ps1": "PowerShell",
}
IMPORTANT_NAMES = {
    "AGENTS.md", "PROJECT_STATE.md", "README.md", "ARCHITECTURE.md", "CHANGELOG.md",
    "package.json", "pyproject.toml", "requirements.txt", "Cargo.toml", "go.mod",
    "pom.xml", "build.gradle", "build.gradle.kts", "Dockerfile", "docker-compose.yml",
    "docker-compose.yaml", "next.config.js", "next.config.mjs", "next.config.ts",
    "vite.config.js", "vite.config.ts", "astro.config.mjs", "tsconfig.json",
}
MANIFEST_NAMES = {
    "package.json", "pyproject.toml", "requirements.txt", "Cargo.toml", "go.mod",
    "pom.xml", "build.gradle", "build.gradle.kts", "composer.json", "Gemfile",
}
JS_IMPORT_RE = re.compile(r"(?:import|export)\s+(?:[^;]*?\s+from\s+)?[\"']([^\"']+)[\"']|require\(\s*[\"']([^\"']+)[\"']\s*\)")
JS_SYMBOL_RE = re.compile(
    r"(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)|"
    r"(?:export\s+)?class\s+([A-Za-z_$][\w$]*)|"
    r"(?:export\s+)?(?:interface|type|enum)\s+([A-Za-z_$][\w$]*)|"
    r"(?:export\s+)?const\s+([A-Za-z_$][\w$]*)\s*="
)
GENERIC_SYMBOL_RE = re.compile(
    r"^\s*(?:pub\s+)?(?:async\s+)?(?:fn|func|class|struct|interface|trait)\s+([A-Za-z_][\w]*)",
    re.MULTILINE,
)
MD_HEADING_RE = re.compile(r"^(#{1,3})\s+(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class ScanResult:
    repo_map: dict[str, Any]
    summary: str
    output_dir: Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def relpath(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_sensitive(path: Path) -> bool:
    name = path.name.lower()
    if name in SENSITIVE_NAMES:
        return True
    if name.startswith(".env.") or name.endswith(".tfvars.json"):
        return True
    if path.suffix.lower() in SENSITIVE_SUFFIXES:
        return True
    if any(part in name for part in SENSITIVE_NAME_PARTS) and path.suffix.lower() in {".json", ".yaml", ".yml", ".toml", ".ini", ".txt"}:
        return True
    return False


def is_binary(path: Path, data: bytes) -> bool:
    if path.suffix.lower() in BINARY_SUFFIXES:
        return True
    return b"\x00" in data[:8192]


def iter_candidate_files(root: Path, max_bytes: int = DEFAULT_MAX_BYTES) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        dirs[:] = sorted(d for d in dirs if d not in IGNORE_DIRS)
        for name in sorted(files):
            path = current_path / name
            if is_sensitive(path):
                continue
            try:
                if path.is_symlink() or path.stat().st_size > max_bytes:
                    continue
            except OSError:
                continue
            yield path


def detect_language(path: Path) -> str:
    if path.name == "Dockerfile":
        return "Dockerfile"
    return LANGUAGE_BY_SUFFIX.get(path.suffix.lower(), "Text")


def extract_python(text: str) -> tuple[list[str], list[str]]:
    symbols: list[str] = []
    imports: list[str] = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return symbols, imports
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            symbols.append(node.name)
        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return unique_limited(symbols), unique_limited(imports)


def unique_limited(values: Iterable[str], limit: int = 80) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
            if len(result) >= limit:
                break
    return result


def extract_text_metadata(path: Path, text: str) -> tuple[list[str], list[str]]:
    suffix = path.suffix.lower()
    if suffix == ".py":
        return extract_python(text)
    if suffix in {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}:
        symbols: list[str] = []
        for match in JS_SYMBOL_RE.finditer(text):
            symbols.append(next(group for group in match.groups() if group))
        imports = [a or b for a, b in JS_IMPORT_RE.findall(text)]
        return unique_limited(symbols), unique_limited(imports)
    if suffix == ".md":
        headings = [heading.strip() for _, heading in MD_HEADING_RE.findall(text)]
        return unique_limited(headings, 40), []
    if suffix in {".rs", ".go", ".java", ".kt", ".kts", ".cs", ".cpp", ".cc", ".c", ".h"}:
        return unique_limited(GENERIC_SYMBOL_RE.findall(text)), []
    return [], []


def file_metadata(path: Path, root: Path, data: bytes) -> dict[str, Any]:
    relative = relpath(path, root)
    language = detect_language(path)
    text = data.decode("utf-8", errors="replace")
    symbols, imports = extract_text_metadata(path, text)
    return {
        "path": relative,
        "sha256": sha256_bytes(data),
        "bytes": len(data),
        "language": language,
        "symbols": symbols,
        "imports": imports,
        "important": path.name in IMPORTANT_NAMES or relative.startswith("core/") or relative.startswith("skills/"),
    }


def git_snapshot(root: Path) -> dict[str, Any]:
    def run(*args: str) -> str | None:
        try:
            result = subprocess.run(
                ["git", *args], cwd=root, check=True, capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return None

    head = run("rev-parse", "HEAD")
    branch = run("rev-parse", "--abbrev-ref", "HEAD")
    status = run("status", "--porcelain")
    return {
        "head": head,
        "branch": branch,
        "dirty": bool(status) if status is not None else None,
    }


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else None
    except (OSError, json.JSONDecodeError):
        return None


def parse_package_json(path: Path) -> tuple[list[str], list[str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [], []
    deps: list[str] = []
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        section = value.get(key, {})
        if isinstance(section, dict):
            deps.extend(str(name) for name in section)
    scripts = value.get("scripts", {})
    return sorted(set(deps)), sorted(scripts) if isinstance(scripts, dict) else []


def parse_pyproject(path: Path) -> list[str]:
    try:
        value = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError):
        return []
    deps: list[str] = []
    project = value.get("project", {})
    if isinstance(project, dict):
        raw = project.get("dependencies", [])
        if isinstance(raw, list):
            deps.extend(re.split(r"[<>=!~\[ ;]", str(item), maxsplit=1)[0] for item in raw)
    return sorted({dep for dep in deps if dep})


def detect_stack(root: Path, file_paths: set[str], language_counts: dict[str, int]) -> dict[str, Any]:
    manifests = sorted(path for path in file_paths if Path(path).name in MANIFEST_NAMES)
    frameworks: set[str] = set()
    dependencies: dict[str, list[str]] = {}
    package_scripts: list[str] = []

    package_paths = sorted(path for path in file_paths if Path(path).name == "package.json")
    npm_deps: set[str] = set()
    for package_path in package_paths[:20]:
        deps, scripts = parse_package_json(root / package_path)
        npm_deps.update(deps)
        if package_path == "package.json":
            package_scripts = scripts
    if npm_deps:
        dependencies["npm"] = sorted(npm_deps)
        checks = {
            "Next.js": "next", "React": "react", "Vue": "vue", "Svelte": "svelte",
            "Astro": "astro", "Vite": "vite", "Drizzle": "drizzle-orm", "Prisma": "prisma",
            "Playwright": "@playwright/test", "Vitest": "vitest", "HeroUI": "@heroui/react",
        }
        frameworks.update(label for label, dep in checks.items() if dep in npm_deps)

    python_deps: set[str] = set()
    for pyproject_path in sorted(path for path in file_paths if Path(path).name == "pyproject.toml")[:20]:
        python_deps.update(parse_pyproject(root / pyproject_path))
    for requirements_path in sorted(path for path in file_paths if Path(path).name == "requirements.txt")[:20]:
        try:
            for line in (root / requirements_path).read_text("utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    python_deps.add(re.split(r"[<>=!~\[ ;]", line, maxsplit=1)[0])
        except OSError:
            pass
    if python_deps:
        dependencies["python"] = sorted(dep for dep in python_deps if dep)
    if "Cargo.toml" in file_paths:
        frameworks.add("Rust/Cargo")
    if "go.mod" in file_paths:
        frameworks.add("Go modules")

    package_manager = None
    for lock, label in (("pnpm-lock.yaml", "pnpm"), ("yarn.lock", "yarn"), ("bun.lockb", "bun"), ("bun.lock", "bun"), ("package-lock.json", "npm")):
        if lock in file_paths:
            package_manager = label
            break

    return {
        "manifests": manifests,
        "languages": dict(sorted(language_counts.items(), key=lambda item: (-item[1], item[0]))),
        "frameworks": sorted(frameworks),
        "package_manager": package_manager,
        "dependencies": dependencies,
        "package_scripts": package_scripts,
    }


def local_dependency_edges(files: dict[str, dict[str, Any]]) -> list[dict[str, str]]:
    """Return lightweight relative-import edges without pretending to resolve aliases."""
    edges: list[dict[str, str]] = []
    for path, meta in sorted(files.items()):
        for specifier in meta.get("imports", []):
            if isinstance(specifier, str) and specifier.startswith("."):
                edges.append({"from": path, "import": specifier})
                if len(edges) >= 1000:
                    return edges
    return edges


def fingerprint(files: dict[str, dict[str, Any]]) -> str:
    material = "\n".join(f"{path}:{meta['sha256']}" for path, meta in sorted(files.items()))
    return sha256_bytes(material.encode("utf-8"))


def render_summary(repo_map: dict[str, Any]) -> str:
    stack = repo_map["stack"]
    delta = repo_map["delta"]
    stats = repo_map["stats"]
    git = repo_map["git"]
    lines = [
        "# App Factory Context Summary",
        "",
        f"- fingerprint: `{repo_map['fingerprint']}`",
        f"- files mapped: **{stats['files']}**",
        f"- cache hits: **{stats['cache_hits']}**; reprocessed: **{stats['reprocessed']}**",
        f"- git: branch `{git.get('branch') or 'unknown'}`, head `{git.get('head') or 'unknown'}`, dirty `{git.get('dirty')}`",
        "",
        "## Stack",
        "",
        f"- frameworks/tools: {', '.join(stack['frameworks']) or 'not inferred'}",
        f"- package manager: {stack['package_manager'] or 'not inferred'}",
        f"- manifests: {', '.join(stack['manifests']) or 'none'}",
        f"- languages: {', '.join(f'{name} ({count})' for name, count in list(stack['languages'].items())[:10]) or 'none'}",
        "",
        "## Delta since previous context",
        "",
        f"- added: {', '.join(delta['added']) or 'none'}",
        f"- changed: {', '.join(delta['changed']) or 'none'}",
        f"- removed: {', '.join(delta['removed']) or 'none'}",
        "",
        "## Important files",
        "",
    ]
    important = repo_map.get("important_files", [])
    lines.extend(f"- `{path}`" for path in important[:80])
    if not important:
        lines.append("- none detected")
    return "\n".join(lines) + "\n"


def scan_repository(root: Path | str, output_dir: Path | str | None = None, max_bytes: int = DEFAULT_MAX_BYTES) -> ScanResult:
    root = Path(root).resolve()
    output = Path(output_dir).resolve() if output_dir else root / ".factory" / "context"
    previous = load_json(output / "repo-map.json") or {}
    previous_files = previous.get("files", {}) if isinstance(previous.get("files", {}), dict) else {}

    files: dict[str, dict[str, Any]] = {}
    cache_hits = 0
    reprocessed = 0
    skipped_binary = 0
    current_paths: set[str] = set()

    for path in iter_candidate_files(root, max_bytes=max_bytes):
        relative = relpath(path, root)
        try:
            data = path.read_bytes()
        except OSError:
            continue
        if is_binary(path, data):
            skipped_binary += 1
            continue
        current_paths.add(relative)
        digest = sha256_bytes(data)
        cached = previous_files.get(relative)
        if isinstance(cached, dict) and cached.get("sha256") == digest:
            files[relative] = cached
            cache_hits += 1
            continue
        files[relative] = file_metadata(path, root, data)
        reprocessed += 1

    old_paths = set(previous_files)
    added = sorted(current_paths - old_paths)
    removed = sorted(old_paths - current_paths)
    changed = sorted(
        path for path in (current_paths & old_paths)
        if isinstance(previous_files.get(path), dict)
        and previous_files[path].get("sha256") != files[path].get("sha256")
    )

    language_counts: dict[str, int] = {}
    for meta in files.values():
        language = str(meta.get("language", "Text"))
        language_counts[language] = language_counts.get(language, 0) + 1

    repo_map: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now(),
        "root_name": root.name,
        "fingerprint": fingerprint(files),
        "git": git_snapshot(root),
        "stack": detect_stack(root, set(files), language_counts),
        "delta": {"added": added, "changed": changed, "removed": removed},
        "stats": {
            "files": len(files), "cache_hits": cache_hits, "reprocessed": reprocessed,
            "skipped_binary": skipped_binary,
        },
        "important_files": sorted(path for path, meta in files.items() if meta.get("important")),
        "local_dependency_edges": local_dependency_edges(files),
        "files": dict(sorted(files.items())),
    }
    summary = render_summary(repo_map)
    output.mkdir(parents=True, exist_ok=True)
    (output / "repo-map.json").write_text(json.dumps(repo_map, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "SUMMARY.md").write_text(summary, encoding="utf-8")
    return ScanResult(repo_map=repo_map, summary=summary, output_dir=output)
