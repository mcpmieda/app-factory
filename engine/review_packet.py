from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .semantic_verification import read_spec, read_verification_plan, subject_fingerprint

MAX_DIFF_CHARS = 120_000


def _run_git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result.stdout.strip()


def review_diff(root: Path | str, *, base_ref: str = "main") -> dict[str, Any]:
    root = Path(root).resolve()
    try:
        merge_base = _run_git(root, "merge-base", "HEAD", base_ref)
        changed = _run_git(
            root,
            "diff",
            "--name-only",
            f"{merge_base}..HEAD",
            "--",
            ".",
            ":(exclude)specs/review-evidence.json",
            ":(exclude).factory",
        ).splitlines()
        diff = _run_git(
            root,
            "diff",
            "--no-ext-diff",
            "--unified=3",
            f"{merge_base}..HEAD",
            "--",
            ".",
            ":(exclude)specs/review-evidence.json",
            ":(exclude).factory",
        )
        truncated = len(diff) > MAX_DIFF_CHARS
        if truncated:
            diff = diff[:MAX_DIFF_CHARS] + "\n...[diff truncated by App Factory review packet]"
        return {
            "available": True,
            "base_ref": base_ref,
            "merge_base": merge_base,
            "changed_files": [item for item in changed if item],
            "diff": diff,
            "truncated": truncated,
        }
    except (OSError, subprocess.SubprocessError) as error:
        return {
            "available": False,
            "base_ref": base_ref,
            "merge_base": None,
            "changed_files": [],
            "diff": None,
            "truncated": False,
            "error": str(error),
        }


def build_clean_review_packet(root: Path | str, *, base_ref: str = "main") -> dict[str, Any]:
    root = Path(root).resolve()
    return {
        "review_contract": (
            "Fresh review input only. Judge whether the current diff satisfies the semantic contract and "
            "verification traceability. Do not use implementation reasoning, prior review conclusions or "
            "claims made by the implementing agent as evidence."
        ),
        "spec": read_spec(root),
        "verification_plan": read_verification_plan(root),
        "subject_fingerprint": subject_fingerprint(root),
        "change": review_diff(root, base_ref=base_ref),
    }
