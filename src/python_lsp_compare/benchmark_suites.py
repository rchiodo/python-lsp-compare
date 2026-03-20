from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


METHOD_CONFIG_KEYS: dict[str, str] = {
    "completion_points": "textDocument/completion",
    "hover_points": "textDocument/hover",
    "document_symbol_points": "textDocument/documentSymbol",
    "goto_definition_points": "textDocument/definition",
    "find_references_points": "textDocument/references",
}


@dataclass(slots=True)
class BenchmarkValidation:
    require_non_empty: bool | None = None
    min_completion_items: int | None = None
    min_hover_text_chars: int | None = None
    min_symbol_count: int | None = None
    min_location_count: int | None = None
    min_size_chars: int | None = None


@dataclass(slots=True)
class BenchmarkPoint:
    label: str
    file_path: Path
    line: int
    character: int
    validation: BenchmarkValidation = field(default_factory=BenchmarkValidation)


@dataclass(slots=True)
class BenchmarkSuite:
    name: str
    description: str
    root_path: Path
    workspace_dir: Path
    requirements_file: Path | None
    install_packages: list[str] = field(default_factory=list)
    iterations: int = 3
    warmup_iterations: int = 1
    points_by_method: dict[str, list[BenchmarkPoint]] = field(default_factory=dict)


def discover_benchmark_suites(benchmark_root: Path | None = None) -> dict[str, BenchmarkSuite]:
    root = benchmark_root or default_benchmark_root()
    if not root.exists():
        return {}
    suites: dict[str, BenchmarkSuite] = {}
    for child in sorted(root.iterdir()):
        config_path = child / "config.json"
        if child.is_dir() and config_path.exists():
            suite = load_benchmark_suite(config_path)
            suites[suite.name] = suite
    return suites


def default_benchmark_root() -> Path:
    return Path(__file__).resolve().parents[2] / "benchmarks"


def load_benchmark_suite(config_path: Path) -> BenchmarkSuite:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    suite_root = config_path.parent.resolve()
    workspace_dir = suite_root / _pick(data, "workspace_dir", "WORKSPACE_DIR", default="src")
    requirements_name = _pick(data, "requirements_file", "ENV_SOURCE", default=None)
    requirements_file = None if requirements_name is None else suite_root / requirements_name
    points_by_method: dict[str, list[BenchmarkPoint]] = {}
    for config_key, method in METHOD_CONFIG_KEYS.items():
        raw_points = _pick(data, config_key, config_key.upper(), default=[])
        points_by_method[method] = [_load_point(item, suite_root) for item in raw_points]
    return BenchmarkSuite(
        name=_pick(data, "name", "TEST_NAME", default=suite_root.name),
        description=_pick(data, "description", "DESCRIPTION", default=f"Benchmark suite for {suite_root.name}."),
        root_path=suite_root,
        workspace_dir=workspace_dir,
        requirements_file=requirements_file,
        install_packages=list(_pick(data, "install_packages", "INSTALL_PACKAGE", default=[])),
        iterations=int(_pick(data, "iterations", "ITERATIONS", default=3)),
        warmup_iterations=int(_pick(data, "warmup_iterations", "WARMUP_ITERATIONS", default=1)),
        points_by_method={key: value for key, value in points_by_method.items() if value},
    )


def _load_point(data: dict[str, Any], suite_root: Path) -> BenchmarkPoint:
    label = data.get("label") or data.get("_comment") or data.get("comment") or f"{data['file']}:{data['line']}:{data['character']}"
    return BenchmarkPoint(
        label=label,
        file_path=_resolve_point_path(suite_root, data["file"]),
        line=int(data["line"]),
        character=int(data["character"]),
        validation=_load_validation(data.get("validation", {})),
    )


def _load_validation(data: dict[str, Any]) -> BenchmarkValidation:
    return BenchmarkValidation(
        require_non_empty=_read_optional_bool(data.get("requireNonEmpty")),
        min_completion_items=_read_optional_int(data.get("minCompletionItems")),
        min_hover_text_chars=_read_optional_int(data.get("minHoverTextChars")),
        min_symbol_count=_read_optional_int(data.get("minSymbolCount")),
        min_location_count=_read_optional_int(data.get("minLocationCount")),
        min_size_chars=_read_optional_int(data.get("minSizeChars")),
    )


def _resolve_point_path(suite_root: Path, raw_path: str) -> Path:
    expanded = raw_path.replace("${SYS_PREFIX}", str(Path(sys.prefix)))
    candidate = Path(expanded)
    if candidate.is_absolute():
        return candidate
    return (suite_root / candidate).resolve()


def _pick(data: dict[str, Any], *keys: str, default: Any) -> Any:
    for key in keys:
        if key in data:
            return data[key]
    return default


def _read_optional_int(value: Any) -> int | None:
    if value is None:
        return None
    return int(value)


def _read_optional_bool(value: Any) -> bool | None:
    if value is None:
        return None
    return bool(value)