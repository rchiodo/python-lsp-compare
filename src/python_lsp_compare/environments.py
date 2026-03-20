from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from .benchmark_suites import BenchmarkSuite


@dataclass(slots=True)
class WorkspaceConfigState:
    path: Path
    original_text: str | None


@dataclass(slots=True)
class BenchmarkEnvironment:
    mode: str
    root_path: Path | None
    python_executable: str
    process_env: dict[str, str]
    launch_command: list[str]
    workspace_root: Path
    workspace_settings: dict[str, object]
    workspace_config_state: WorkspaceConfigState | None


def prepare_benchmark_environment(
    *,
    suite: BenchmarkSuite,
    command: Sequence[str],
    environment_mode: str,
    base_python_executable: str,
    install_requirements: bool,
    environment_root: Path | None = None,
    logger: Callable[[str], None] | None = None,
) -> BenchmarkEnvironment:
    if environment_mode not in {"current", "isolated"}:
        raise ValueError(f"Unsupported environment mode: {environment_mode}")

    base_env = dict(os.environ)
    if environment_mode == "current":
        if install_requirements:
            _log(logger, f"[{suite.name}] installing requirements into current environment")
            _install_suite_requirements(suite, base_python_executable)
        workspace_settings = _build_workspace_settings(
            suite=suite,
            python_executable=base_python_executable,
            venv_root=None,
        )
        _log(logger, f"[{suite.name}] using current interpreter {base_python_executable}")
        return BenchmarkEnvironment(
            mode="current",
            root_path=None,
            python_executable=base_python_executable,
            process_env=base_env,
            launch_command=list(command),
            workspace_root=suite.root_path,
            workspace_settings=workspace_settings,
            workspace_config_state=None,
        )

    venv_root = (environment_root / suite.name if environment_root is not None else suite.root_path / ".venv").resolve()
    env_python = _ensure_virtual_environment(venv_root, base_python_executable)
    process_env = _build_isolated_process_env(base_env, venv_root)
    if install_requirements:
        _log(logger, f"[{suite.name}] installing requirements into {venv_root}")
        _install_suite_requirements(suite, env_python)
    workspace_settings = _build_workspace_settings(
        suite=suite,
        python_executable=env_python,
        venv_root=venv_root,
    )
    workspace_config_state = _write_pyrightconfig(
        suite=suite,
        python_executable=env_python,
        venv_root=venv_root,
    )
    _log(logger, f"[{suite.name}] wrote pyrightconfig.json for {venv_root.name}")
    return BenchmarkEnvironment(
        mode="isolated",
        root_path=venv_root,
        python_executable=env_python,
        process_env=process_env,
        launch_command=_adapt_command_for_environment(command, env_python),
        workspace_root=suite.root_path,
        workspace_settings=workspace_settings,
        workspace_config_state=workspace_config_state,
    )


def cleanup_benchmark_environment(environment: BenchmarkEnvironment) -> None:
    state = environment.workspace_config_state
    if state is None:
        return
    if state.original_text is None:
        try:
            state.path.unlink()
        except FileNotFoundError:
            pass
        return
    state.path.write_text(state.original_text, encoding="utf-8")


def _ensure_virtual_environment(venv_root: Path, base_python_executable: str) -> str:
    python_path = _venv_python_path(venv_root)
    if python_path.exists():
        return str(python_path)
    venv_root.parent.mkdir(parents=True, exist_ok=True)
    completed = subprocess.run(
        [base_python_executable, "-m", "venv", str(venv_root)],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or f"failed to create virtual environment at {venv_root}")
    return str(python_path)


def _build_isolated_process_env(base_env: dict[str, str], venv_root: Path) -> dict[str, str]:
    process_env = dict(base_env)
    scripts_dir = str(_venv_scripts_path(venv_root))
    original_path = base_env.get("PATH", "")
    process_env["PATH"] = scripts_dir if not original_path else os.pathsep.join([scripts_dir, original_path])
    process_env["VIRTUAL_ENV"] = str(venv_root)
    process_env["PYTHONNOUSERSITE"] = "1"
    process_env.pop("PYTHONHOME", None)
    process_env.pop("PYTHONPATH", None)
    return process_env


def _adapt_command_for_environment(command: Sequence[str], env_python: str) -> list[str]:
    if not command:
        raise ValueError("command must not be empty")
    adapted = list(command)
    if _looks_like_python_command(adapted[0]):
        adapted[0] = env_python
    return adapted


def _looks_like_python_command(command_part: str) -> bool:
    name = Path(command_part).name.lower()
    return name in {"python", "python.exe", "py", "py.exe"} or Path(command_part).resolve() == Path(sys.executable).resolve()


def _install_suite_requirements(suite: BenchmarkSuite, python_executable: str) -> None:
    state_path = _install_state_path(python_executable)
    desired_state = _build_install_state(suite)
    if state_path.exists():
        try:
            installed_state = json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            installed_state = None
        if installed_state == desired_state:
            return
    commands: list[list[str]] = []
    if suite.requirements_file is not None and suite.requirements_file.exists():
        commands.append([python_executable, "-m", "pip", "install", "-r", str(suite.requirements_file)])
    if suite.install_packages:
        commands.append([python_executable, "-m", "pip", "install", *suite.install_packages])
    for command in commands:
        completed = subprocess.run(command, capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or f"pip install failed for {suite.name}")
    state_path.write_text(json.dumps(desired_state, indent=2), encoding="utf-8")


def _build_workspace_settings(
    *,
    suite: BenchmarkSuite,
    python_executable: str,
    venv_root: Path | None,
) -> dict[str, object]:
    analysis_settings: dict[str, object] = {
        "autoSearchPaths": True,
        "useLibraryCodeForTypes": True,
        "diagnosticMode": "workspace",
        "extraPaths": [str(suite.workspace_dir)],
    }
    python_settings: dict[str, object] = {
        "defaultInterpreterPath": python_executable,
        "pythonPath": python_executable,
        "analysis": analysis_settings,
    }
    if venv_root is not None:
        python_settings["venvPath"] = str(venv_root.parent)
        python_settings["venv"] = venv_root.name
    return {"python": python_settings}


def _write_pyrightconfig(
    *,
    suite: BenchmarkSuite,
    python_executable: str,
    venv_root: Path,
) -> WorkspaceConfigState:
    config_path = suite.root_path / "pyrightconfig.json"
    original_text = config_path.read_text(encoding="utf-8") if config_path.exists() else None
    relative_root = _relative_workspace_path(suite.workspace_dir, suite.root_path)
    venv_parent = _relative_workspace_path(venv_root.parent, suite.root_path)
    config_payload: dict[str, object] = {
        "include": [relative_root],
        "venvPath": venv_parent,
        "venv": venv_root.name,
        "pythonVersion": _read_python_version(python_executable),
    }
    if relative_root != ".":
        config_payload["executionEnvironments"] = [{"root": relative_root, "extraPaths": [relative_root]}]
    config_path.write_text(json.dumps(config_payload, indent=2), encoding="utf-8")
    return WorkspaceConfigState(path=config_path, original_text=original_text)


def _relative_workspace_path(path: Path, workspace_root: Path) -> str:
    try:
        relative_path = path.resolve().relative_to(workspace_root.resolve())
    except ValueError:
        return str(path)
    if str(relative_path) in {"", "."}:
        return "."
    return str(relative_path).replace("\\", "/")


def _read_python_version(python_executable: str) -> str:
    completed = subprocess.run(
        [python_executable, "-c", "import sys; print(f'{sys.version_info[0]}.{sys.version_info[1]}')"],
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        return f"{sys.version_info[0]}.{sys.version_info[1]}"
    return completed.stdout.strip() or f"{sys.version_info[0]}.{sys.version_info[1]}"


def _build_install_state(suite: BenchmarkSuite) -> dict[str, object]:
    requirements_hash = None
    if suite.requirements_file is not None and suite.requirements_file.exists():
        requirements_hash = hashlib.sha256(suite.requirements_file.read_bytes()).hexdigest()
    return {
        "requirements_file": None if suite.requirements_file is None else str(suite.requirements_file.resolve()),
        "requirements_hash": requirements_hash,
        "install_packages": list(suite.install_packages),
    }


def _install_state_path(python_executable: str) -> Path:
    return Path(python_executable).resolve().parent.parent / ".python-lsp-compare-install.json"


def _venv_python_path(venv_root: Path) -> Path:
    if os.name == "nt":
        return venv_root / "Scripts" / "python.exe"
    return venv_root / "bin" / "python"


def _venv_scripts_path(venv_root: Path) -> Path:
    if os.name == "nt":
        return venv_root / "Scripts"
    return venv_root / "bin"


def _log(logger: Callable[[str], None] | None, message: str) -> None:
    if logger is not None:
        logger(message)