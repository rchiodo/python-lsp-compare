from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any, Sequence

from .server_configs import ConfiguredServer


def describe_server_version(server: ConfiguredServer) -> dict[str, Any]:
    source_path = None if server.source_path is None else Path(server.source_path)
    repo_root = _find_git_root(source_path)
    if repo_root is not None:
        commit = _run_command(["git", "-C", str(repo_root), "rev-parse", "HEAD"])
        short_commit = None if commit is None else commit[:12]
        return {
            "kind": "git",
            "label": short_commit or "unknown",
            "repo_root": str(repo_root),
            "commit": commit,
            "short_commit": short_commit,
            "source_path": None if source_path is None else str(source_path),
        }

    version_output = _run_command([server.command, "--version"])
    if version_output:
        return {
            "kind": "command",
            "label": version_output.splitlines()[0],
            "repo_root": None,
            "commit": None,
            "short_commit": None,
            "source_path": None if source_path is None else str(source_path),
        }

    return {
        "kind": "unknown",
        "label": "unknown",
        "repo_root": None,
        "commit": None,
        "short_commit": None,
        "source_path": None if source_path is None else str(source_path),
    }


def _find_git_root(source_path: Path | None) -> Path | None:
    if source_path is None:
        return None
    current = source_path if source_path.is_dir() else source_path.parent
    for candidate in [current, *current.parents]:
        if (candidate / ".git").exists():
            return candidate
    return None


def _run_command(command: Sequence[str]) -> str | None:
    try:
        completed = subprocess.run(
            list(command),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=5,
            check=True,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()
    return stdout or stderr or None