from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


def write_csv_report(summary_path: Path, output_path: Path, baseline_server_id: str | None = None) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    rows = build_csv_rows(summary_path, baseline_server_id=baseline_server_id)
    if not rows:
        output_path.write_text("", encoding="utf-8")
        return output_path
    fieldnames = list(rows[0].keys())
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return output_path


def build_csv_rows(summary_path: Path, baseline_server_id: str | None = None) -> list[dict[str, object]]:
    summary = _read_json(summary_path)
    servers = [_load_server_entry(summary_path, entry) for entry in summary.get("servers", [])]
    baseline_server = _select_baseline_server(servers, baseline_server_id or summary.get("baseline_server"))
    if any(server["report"].get("benchmark_reports") for server in servers):
        return _build_benchmark_rows(summary, servers, baseline_server)
    return _build_scenario_rows(summary, servers, baseline_server)


def _build_benchmark_rows(
    summary: dict[str, Any],
    servers: list[dict[str, Any]],
    baseline_server: dict[str, Any] | None,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    suite_order = summary.get("requested_benchmarks") or _ordered_unique(
        report.get("name")
        for server in servers
        for report in server["report"].get("benchmark_reports", [])
    )
    for suite_name in suite_order:
        suite_servers = []
        for server in servers:
            suite_report = _find_by_name(server["report"].get("benchmark_reports", []), suite_name)
            if suite_report is not None:
                suite_servers.append({**server, "suite_report": suite_report})
        baseline_suite_server = _find_server_in_collection(suite_servers, baseline_server)
        point_order = _ordered_unique(
            _point_key(point)
            for server in suite_servers
            for point in server["suite_report"].get("points", [])
        )
        for point_key in point_order:
            baseline_value = None
            metric_key = None
            metric_label = None
            if baseline_suite_server is not None:
                baseline_point = _find_point(baseline_suite_server["suite_report"].get("points", []), point_key)
                if baseline_point is not None:
                    baseline_metrics = _measured_request_metrics(baseline_point)
                    metric_key, metric_label = _preferred_result_metric(baseline_point.get("method"), baseline_metrics)
                    baseline_value = _mean_numeric(baseline_metrics, metric_key) if metric_key is not None else None
            for server in suite_servers:
                point = _find_point(server["suite_report"].get("points", []), point_key)
                if point is None:
                    continue
                measured_metrics = _measured_request_metrics(point)
                metric_key, metric_label = _preferred_result_metric(point.get("method"), measured_metrics)
                point_value = _mean_numeric(measured_metrics, metric_key) if metric_key is not None else None
                if baseline_value is None and baseline_server is None:
                    baseline_value = point_value
                rows.append(
                    {
                        "report_type": "benchmark",
                        "baseline_server_id": None if baseline_server is None else baseline_server["id"],
                        "server_id": server["id"],
                        "server_name": server["display_name"],
                        "suite_name": suite_name,
                        "scenario_name": "",
                        "point_label": point.get("label", ""),
                        "method": point.get("method", ""),
                        "success": point.get("success", False),
                        "mean_ms": point.get("summary", {}).get("mean_ms"),
                        "p95_ms": point.get("summary", {}).get("p95_ms"),
                        "non_empty_rate": _non_empty_rate(measured_metrics),
                        "result_metric_name": metric_key or "",
                        "result_metric_label": metric_label or "",
                        "result_metric_value": point_value,
                        "result_metric_delta": None if baseline_value is None or point_value is None else point_value - baseline_value,
                        "validation_passed": point.get("summary", {}).get("validation", {}).get("passed", True),
                        "validation_failure_count": point.get("summary", {}).get("validation", {}).get("failure_count", 0),
                    }
                )
    return rows


def _build_scenario_rows(
    summary: dict[str, Any],
    servers: list[dict[str, Any]],
    baseline_server: dict[str, Any] | None,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    scenario_order = summary.get("requested_scenarios") or _ordered_unique(
        report.get("name")
        for server in servers
        for report in server["report"].get("scenario_reports", [])
    )
    baseline_reports = baseline_server["report"].get("scenario_reports", []) if baseline_server is not None else []
    for scenario_name in scenario_order:
        baseline_report = _find_by_name(baseline_reports, scenario_name)
        baseline_metrics = [] if baseline_report is None else _request_metrics(baseline_report.get("metrics", []))
        baseline_metric_key, baseline_metric_label = _preferred_result_metric_for_scenario(scenario_name, baseline_metrics)
        baseline_value = None if baseline_report is None or baseline_metric_key is None else _mean_numeric(baseline_metrics, baseline_metric_key)
        for server in servers:
            report = _find_by_name(server["report"].get("scenario_reports", []), scenario_name)
            if report is None:
                continue
            request_metrics = _request_metrics(report.get("metrics", []))
            metric_key, metric_label = _preferred_result_metric_for_scenario(scenario_name, request_metrics)
            metric_value = None if metric_key is None else _mean_numeric(request_metrics, metric_key)
            if baseline_value is None and baseline_server is None:
                baseline_value = metric_value
            rows.append(
                {
                    "report_type": "scenario",
                    "baseline_server_id": None if baseline_server is None else baseline_server["id"],
                    "server_id": server["id"],
                    "server_name": server["display_name"],
                    "suite_name": "",
                    "scenario_name": scenario_name,
                    "point_label": "",
                    "method": "",
                    "success": report.get("success", False),
                    "mean_ms": report.get("summary", {}).get("mean_ms"),
                    "p95_ms": report.get("summary", {}).get("p95_ms"),
                    "non_empty_rate": _non_empty_rate(request_metrics),
                    "result_metric_name": metric_key or baseline_metric_key or "",
                    "result_metric_label": metric_label or baseline_metric_label or "",
                    "result_metric_value": metric_value,
                    "result_metric_delta": None if baseline_value is None or metric_value is None else metric_value - baseline_value,
                    "validation_passed": True,
                    "validation_failure_count": 0,
                }
            )
    return rows


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_server_entry(summary_path: Path, entry: dict[str, Any]) -> dict[str, Any]:
    report_path = _resolve_report_path(summary_path, entry["output_path"])
    return {
        "id": entry.get("id"),
        "display_name": entry.get("display_name", entry.get("id", "server")),
        "report": _read_json(report_path),
    }


def _resolve_report_path(summary_path: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute() and path.exists():
        return path
    for candidate in [Path.cwd() / path, summary_path.parent / path, summary_path.parent / path.name]:
        if candidate.exists():
            return candidate.resolve()
    return path.resolve()


def _request_metrics(metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [metric for metric in metrics if metric.get("kind") == "request"]


def _measured_request_metrics(point: dict[str, Any]) -> list[dict[str, Any]]:
    return [metric for metric in _request_metrics(point.get("metrics", [])) if metric.get("context", {}).get("phase") == "measured"]


def _preferred_result_metric(method: str | None, metrics: list[dict[str, Any]]) -> tuple[str | None, str | None]:
    candidates = {
        "textDocument/completion": ("completion_item_count", "Completions found"),
        "textDocument/definition": ("location_count", "Definitions found"),
        "textDocument/references": ("location_count", "References found"),
        "textDocument/documentSymbol": ("symbol_count", "Symbols found"),
        "textDocument/hover": ("hover_text_char_count", "Hover length"),
    }
    if method in candidates:
        key, label = candidates[method]
        if any(metric.get("result_summary", {}).get(key) is not None for metric in metrics):
            return key, label
    if any(metric.get("result_summary", {}).get("top_level_count") is not None for metric in metrics):
        return "top_level_count", "Results found"
    return None, None


def _preferred_result_metric_for_scenario(scenario_name: str, metrics: list[dict[str, Any]]) -> tuple[str | None, str | None]:
    scenario_candidates = {
        "hover": ("hover_text_char_count", "Hover length"),
        "completion": ("completion_item_count", "Completions found"),
        "document_symbols": ("symbol_count", "Symbols found"),
    }
    if scenario_name in scenario_candidates:
        key, label = scenario_candidates[scenario_name]
        if any(metric.get("result_summary", {}).get(key) is not None for metric in metrics):
            return key, label
    for method in [metric.get("method") for metric in metrics if isinstance(metric, dict)]:
        metric_key, metric_label = _preferred_result_metric(method, metrics)
        if metric_key is not None:
            return metric_key, metric_label
    return None, None


def _mean_numeric(metrics: list[dict[str, Any]], key: str | None) -> float | None:
    if key is None:
        return None
    values: list[float] = []
    for metric in metrics:
        value = metric.get("result_summary", {}).get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        values.append(float(value))
    if not values:
        return None
    return sum(values) / len(values)


def _non_empty_rate(metrics: list[dict[str, Any]]) -> float | None:
    present = [metric for metric in metrics if metric.get("result_summary", {}).get("present")]
    if not present:
        return None
    non_empty = [metric for metric in present if not metric.get("result_summary", {}).get("empty")]
    return len(non_empty) / len(present)


def _select_baseline_server(servers: list[dict[str, Any]], baseline_server_id: str | None) -> dict[str, Any] | None:
    if not servers:
        return None
    if baseline_server_id is None:
        return servers[0]
    for server in servers:
        if server["id"] == baseline_server_id or server["display_name"] == baseline_server_id:
            return server
    return servers[0]


def _find_server_in_collection(candidates: list[dict[str, Any]], baseline_server: dict[str, Any] | None) -> dict[str, Any] | None:
    if baseline_server is None:
        return candidates[0] if candidates else None
    for candidate in candidates:
        if candidate["id"] == baseline_server["id"]:
            return candidate
    return None


def _ordered_unique(values: Any) -> list[Any]:
    ordered: list[Any] = []
    seen: set[Any] = set()
    for value in values:
        if value in seen or value is None:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def _find_by_name(items: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    for item in items:
        if item.get("name") == name:
            return item
    return None


def _point_key(point: dict[str, Any]) -> str:
    return "|".join([
        str(point.get("method", "")),
        str(point.get("label", "")),
        str(point.get("file_path", "")),
        str(point.get("line", "")),
        str(point.get("character", "")),
    ])


def _find_point(points: list[dict[str, Any]], point_key: str) -> dict[str, Any] | None:
    for point in points:
        if _point_key(point) == point_key:
            return point
    return None
