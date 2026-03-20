from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class ServerPresets:
    scenarios: list[str] = field(default_factory=list)
    benchmarks: list[str] = field(default_factory=list)
    timeout_seconds: float | None = None
    benchmark_timeout_seconds: float | None = None
    benchmark_root: str | None = None
    benchmark_launch_args: list[str] = field(default_factory=list)
    install_requirements: bool | None = None
    environment_mode: str | None = None
    environment_root: str | None = None
    python_executable: str | None = None


@dataclass(slots=True)
class ServerConfigFile:
    baseline_server: str | None = None
    servers: list[ConfiguredServer] = field(default_factory=list)


@dataclass(slots=True)
class ConfiguredServer:
    id: str
    display_name: str
    command: str
    args: list[str] = field(default_factory=list)
    enabled: bool = True
    kind: str | None = None
    notes: list[str] = field(default_factory=list)
    source_path: str | None = None
    presets: ServerPresets = field(default_factory=ServerPresets)

    @property
    def launch_command(self) -> list[str]:
        return [self.command, *self.args]

    @property
    def benchmark_launch_command(self) -> list[str]:
        return [self.command, *self.args, *self.presets.benchmark_launch_args]


def default_local_server_config_path() -> Path:
    return Path(__file__).resolve().parents[2] / "configs" / "local" / "lsp_servers.json"


def example_server_config_path() -> Path:
    return Path(__file__).resolve().parents[2] / "configs" / "lsp_servers.example.json"


def load_server_configs(config_path: Path | None = None) -> list[ConfiguredServer]:
    return load_server_config_file(config_path).servers


def load_server_config_file(config_path: Path | None = None) -> ServerConfigFile:
    resolved = (config_path or default_local_server_config_path()).resolve()
    if not resolved.exists():
        raise FileNotFoundError(
            f"Server config file not found: {resolved}. Copy {example_server_config_path()} to that path and fill in local server commands."
        )
    data = json.loads(resolved.read_text(encoding="utf-8"))
    servers = [
        ConfiguredServer(
            id=item["id"],
            display_name=item.get("displayName", item["id"]),
            command=_resolve_value(item["launch"]["command"], resolved.parent),
            args=[_resolve_value(arg, resolved.parent) for arg in item["launch"].get("args", [])],
            enabled=bool(item.get("enabled", True)),
            kind=item.get("kind"),
            notes=list(item.get("notes", [])),
            source_path=item.get("sourcePath"),
            presets=_load_presets(item.get("presets", {}), resolved.parent),
        )
        for item in data.get("servers", [])
    ]
    return ServerConfigFile(
        baseline_server=data.get("baselineServer"),
        servers=servers,
    )


def _resolve_value(value: str, base_dir: Path) -> str:
    if value.startswith("./") or value.startswith("../"):
        return str((base_dir / value).resolve())
    return value


def _load_presets(data: dict[str, Any], base_dir: Path) -> ServerPresets:
    return ServerPresets(
        scenarios=list(data.get("scenarios", [])),
        benchmarks=list(data.get("benchmarks", [])),
        timeout_seconds=_read_float(data, "timeoutSeconds"),
        benchmark_timeout_seconds=_read_float(data, "benchmarkTimeoutSeconds"),
        benchmark_root=_resolve_optional_value(data.get("benchmarkRoot"), base_dir),
        benchmark_launch_args=[_resolve_value(arg, base_dir) for arg in data.get("benchmarkLaunchArgs", [])],
        install_requirements=_read_bool(data, "installRequirements"),
        environment_mode=data.get("environmentMode"),
        environment_root=_resolve_optional_value(data.get("environmentRoot"), base_dir),
        python_executable=_resolve_optional_value(data.get("pythonExecutable"), base_dir),
    )


def _resolve_optional_value(value: str | None, base_dir: Path) -> str | None:
    if value is None:
        return None
    return _resolve_value(value, base_dir)


def _read_float(data: dict[str, Any], key: str) -> float | None:
    value = data.get(key)
    if value is None:
        return None
    return float(value)


def _read_bool(data: dict[str, Any], key: str) -> bool | None:
    value = data.get(key)
    if value is None:
        return None
    return bool(value)


def write_summary(summary_path: Path, payload: dict[str, Any]) -> None:
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
