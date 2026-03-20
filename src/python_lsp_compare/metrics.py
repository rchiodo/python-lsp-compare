from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any


def _truncate(value: Any, limit: int = 160) -> str | None:
    if value is None:
        return None
    text = repr(value)
    if len(text) <= limit:
        return text
    return f"{text[: limit - 3]}..."


@dataclass(slots=True)
class CallMetric:
    kind: str
    method: str
    duration_ms: float
    success: bool
    started_at_unix: float
    bytes_sent: int
    bytes_received: int
    request_id: int | str | None = None
    error_code: int | None = None
    error_message: str | None = None
    result_preview: str | None = None
    result_summary: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ScenarioReport:
    name: str
    description: str
    success: bool
    total_duration_ms: float
    metrics: list[CallMetric] = field(default_factory=list)
    error_message: str | None = None
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "success": self.success,
            "total_duration_ms": self.total_duration_ms,
            "error_message": self.error_message,
            "summary": self.summary,
            "metrics": [metric.to_dict() for metric in self.metrics],
        }


@dataclass(slots=True)
class BenchmarkPointReport:
    label: str
    method: str
    file_path: str
    line: int
    character: int
    success: bool
    warmup_iterations: int
    measured_iterations: int
    metrics: list[CallMetric] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "method": self.method,
            "file_path": self.file_path,
            "line": self.line,
            "character": self.character,
            "success": self.success,
            "warmup_iterations": self.warmup_iterations,
            "measured_iterations": self.measured_iterations,
            "summary": self.summary,
            "error_message": self.error_message,
            "metrics": [metric.to_dict() for metric in self.metrics],
        }


@dataclass(slots=True)
class BenchmarkSuiteReport:
    name: str
    description: str
    workspace_dir: str
    requirements_file: str | None
    install_packages: list[str]
    environment_mode: str
    environment_path: str | None
    python_executable: str
    success: bool
    total_duration_ms: float
    points: list[BenchmarkPointReport] = field(default_factory=list)
    metrics: list[CallMetric] = field(default_factory=list)
    error_message: str | None = None
    summary: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "workspace_dir": self.workspace_dir,
            "requirements_file": self.requirements_file,
            "install_packages": self.install_packages,
            "environment_mode": self.environment_mode,
            "environment_path": self.environment_path,
            "python_executable": self.python_executable,
            "success": self.success,
            "total_duration_ms": self.total_duration_ms,
            "error_message": self.error_message,
            "summary": self.summary,
            "points": [point.to_dict() for point in self.points],
            "metrics": [metric.to_dict() for metric in self.metrics],
        }


@dataclass(slots=True)
class RunReport:
    server_command: list[str]
    requested_scenarios: list[str]
    started_at_unix: float
    finished_at_unix: float
    requested_benchmarks: list[str] = field(default_factory=list)
    scenario_reports: list[ScenarioReport] = field(default_factory=list)
    benchmark_reports: list[BenchmarkSuiteReport] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "server_command": self.server_command,
            "requested_scenarios": self.requested_scenarios,
            "requested_benchmarks": self.requested_benchmarks,
            "started_at_unix": self.started_at_unix,
            "finished_at_unix": self.finished_at_unix,
            "scenario_reports": [report.to_dict() for report in self.scenario_reports],
            "benchmark_reports": [report.to_dict() for report in self.benchmark_reports],
        }


def build_call_metric(
    *,
    kind: str,
    method: str,
    duration_ms: float,
    success: bool,
    started_at_unix: float,
    bytes_sent: int,
    bytes_received: int,
    request_id: int | str | None = None,
    error: dict[str, Any] | None = None,
    result: Any = None,
    context: dict[str, Any] | None = None,
) -> CallMetric:
    result_summary = _summarize_result(method, result) if kind == "request" and error is None else {}
    return CallMetric(
        kind=kind,
        method=method,
        duration_ms=duration_ms,
        success=success,
        started_at_unix=started_at_unix,
        bytes_sent=bytes_sent,
        bytes_received=bytes_received,
        request_id=request_id,
        error_code=None if error is None else error.get("code"),
        error_message=None if error is None else error.get("message"),
        result_preview=_truncate(result),
        result_summary=result_summary,
        context=context or {},
    )


def _summarize_result(method: str, result: Any) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "present": result is not None,
        "empty": _is_empty_result(method, result),
        "top_level_kind": _result_kind(result),
        "size_chars": 0 if result is None else len(_stable_result_text(result)),
    }
    top_level_count = _top_level_count(result)
    if top_level_count is not None:
        summary["top_level_count"] = top_level_count

    if method == "textDocument/completion":
        completion_item_count = _completion_item_count(result)
        if completion_item_count is not None:
            summary["completion_item_count"] = completion_item_count
    elif method == "textDocument/hover":
        hover_text_char_count = _hover_text_char_count(result)
        if hover_text_char_count is not None:
            summary["hover_text_char_count"] = hover_text_char_count
    elif method == "textDocument/documentSymbol":
        symbol_count = _symbol_count(result)
        if symbol_count is not None:
            summary["symbol_count"] = symbol_count
    elif method in {"textDocument/definition", "textDocument/references"}:
        location_count = _location_count(result)
        if location_count is not None:
            summary["location_count"] = location_count
    return summary


def _stable_result_text(value: Any) -> str:
    try:
        return json.dumps(value, sort_keys=True, default=str)
    except TypeError:
        return repr(value)


def _result_kind(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "dict"
    return type(value).__name__


def _top_level_count(value: Any) -> int | None:
    if isinstance(value, (str, list, dict)):
        return len(value)
    return None


def _is_empty_result(method: str, result: Any) -> bool:
    if result is None:
        return True
    if method == "textDocument/completion":
        completion_item_count = _completion_item_count(result)
        return completion_item_count == 0 if completion_item_count is not None else False
    if method == "textDocument/hover":
        hover_text_char_count = _hover_text_char_count(result)
        return hover_text_char_count == 0 if hover_text_char_count is not None else False
    if method == "textDocument/documentSymbol":
        symbol_count = _symbol_count(result)
        return symbol_count == 0 if symbol_count is not None else False
    if method in {"textDocument/definition", "textDocument/references"}:
        location_count = _location_count(result)
        return location_count == 0 if location_count is not None else False
    if isinstance(result, (str, list, dict)):
        return len(result) == 0
    return False


def _completion_item_count(result: Any) -> int | None:
    if isinstance(result, dict):
        items = result.get("items")
        if isinstance(items, list):
            return len(items)
    if isinstance(result, list):
        return len(result)
    return None


def _hover_text_char_count(result: Any) -> int | None:
    if not isinstance(result, dict):
        return None
    contents = result.get("contents")
    return _text_length(contents)


def _text_length(value: Any) -> int | None:
    if value is None:
        return 0
    if isinstance(value, str):
        return len(value)
    if isinstance(value, dict):
        if isinstance(value.get("value"), str):
            return len(value["value"])
        if isinstance(value.get("language"), str) and isinstance(value.get("value"), str):
            return len(value["value"])
        return None
    if isinstance(value, list):
        lengths = [item for item in (_text_length(item) for item in value) if item is not None]
        return sum(lengths)
    return None


def _symbol_count(result: Any) -> int | None:
    if isinstance(result, list):
        return len(result)
    return None


def _location_count(result: Any) -> int | None:
    if result is None:
        return 0
    if isinstance(result, list):
        return len(result)
    if isinstance(result, dict) and "uri" in result and "range" in result:
        return 1
    return None
