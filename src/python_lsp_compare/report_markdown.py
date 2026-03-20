from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_markdown_report(
    summary_path: Path,
    output_path: Path,
    title: str | None = None,
    baseline_server_id: str | None = None,
    data_link_prefix: str | None = None,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_markdown_report(summary_path, title=title, baseline_server_id=baseline_server_id, data_link_prefix=data_link_prefix), encoding="utf-8")
    return output_path


def render_markdown_report(summary_path: Path, title: str | None = None, baseline_server_id: str | None = None, data_link_prefix: str | None = None) -> str:
    summary = _read_json(summary_path)
    servers = [_load_server_entry(summary_path, entry) for entry in summary.get("servers", [])]
    baseline_server = _select_baseline_server(servers, baseline_server_id or summary.get("baseline_server"))
    server_links = _build_server_links(summary, data_link_prefix) if data_link_prefix else {}
    if any(server["report"].get("benchmark_reports") for server in servers):
        return _render_benchmark_report(summary_path, summary, servers, baseline_server, title=title, server_links=server_links)
    return _render_scenario_report(summary_path, summary, servers, baseline_server, title=title, server_links=server_links)


def _build_server_links(summary: dict[str, Any], prefix: str) -> dict[str, str]:
    """Map server display_name -> markdown link for per-server data files."""
    links: dict[str, str] = {}
    for entry in summary.get("servers", []):
        display_name = entry.get("display_name", entry.get("id", "server"))
        output_path = entry.get("output_path", "")
        filename = Path(output_path).name
        if filename:
            links[display_name] = f"[{display_name}]({prefix}/{filename})"
    return links


def _linked_server_name(display_name: str, server_links: dict[str, str]) -> str:
    return server_links.get(display_name, display_name)


def _render_benchmark_report(
    summary_path: Path,
    summary: dict[str, Any],
    servers: list[dict[str, Any]],
    baseline_server: dict[str, Any] | None,
    title: str | None,
    server_links: dict[str, str] | None = None,
) -> str:
    if server_links is None:
        server_links = {}
    lines: list[str] = []
    lines.append(f"# {title or 'Python LSP Benchmark Comparison'}")
    lines.append("")
    lines.extend(_metadata_lines(summary_path, summary, baseline_server))
    lines.extend(_server_versions_lines(summary))
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("| Server | Success | Benchmarks | Total ms | Avg measured ms | Measured requests | Non-empty % | Failed points |")
    lines.append("| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |")
    overview_rows = []
    for server in servers:
        benchmark_reports = server["report"].get("benchmark_reports", [])
        measured_metrics = [metric for report in benchmark_reports for point in report.get("points", []) for metric in _measured_request_metrics(point)]
        failed_points = sum(1 for report in benchmark_reports for point in report.get("points", []) if not point.get("summary", {}).get("validation", {}).get("passed", True))
        avg_measured_ms = _mean_duration(measured_metrics)
        overview_rows.append(
            {
                "server": _linked_server_name(server["display_name"], server_links),
                "success": "yes" if server["success"] else "no",
                "benchmarks": len(benchmark_reports),
                "total_ms": _format_float(sum(report.get("total_duration_ms", 0.0) for report in benchmark_reports)),
                "avg_measured_ms": _format_float(avg_measured_ms),
                "request_count": len(measured_metrics),
                "non_empty_rate": _format_percent(_non_empty_rate(measured_metrics)),
                "failed_points": failed_points,
                "sort_avg_ms": avg_measured_ms,
            }
        )
    for row in _sort_rows_by_average(overview_rows, "sort_avg_ms"):
        lines.append(
            "| {server} | {success} | {benchmarks} | {total_ms} | {avg_measured_ms} | {request_count} | {non_empty_rate} | {failed_points} |".format(
                **row,
            )
        )

    suite_order = summary.get("requested_benchmarks") or _ordered_unique(
        report.get("name")
        for server in servers
        for report in server["report"].get("benchmark_reports", [])
    )
    for suite_name in suite_order:
        suite_servers = []
        for server in servers:
            report = _find_by_name(server["report"].get("benchmark_reports", []), suite_name)
            if report is not None:
                suite_servers.append({**server, "suite_report": report})
        if not suite_servers:
            continue
        lines.append("")
        lines.append(f"## Benchmark: {suite_name}")
        lines.append("")
        lines.append("| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |")
        lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
        suite_rows = []
        for server in suite_servers:
            suite_report = server["suite_report"]
            measured_metrics = [metric for point in suite_report.get("points", []) for metric in _measured_request_metrics(point)]
            failed_points = sum(1 for point in suite_report.get("points", []) if not point.get("summary", {}).get("validation", {}).get("passed", True))
            avg_measured_ms = _mean_duration(measured_metrics)
            suite_rows.append(
                {
                    "server": _linked_server_name(server["display_name"], server_links),
                    "success": "yes" if suite_report.get("success") else "no",
                    "total_ms": _format_float(suite_report.get("total_duration_ms")),
                    "avg_measured_ms": _format_float(avg_measured_ms),
                    "points": len(suite_report.get("points", [])),
                    "requests": len(measured_metrics),
                    "non_empty_rate": _format_percent(_non_empty_rate(measured_metrics)),
                    "failed_points": failed_points,
                    "sort_avg_ms": avg_measured_ms,
                }
            )
        for row in _sort_rows_by_average(suite_rows, "sort_avg_ms"):
            lines.append(
                "| {server} | {success} | {total_ms} | {avg_measured_ms} | {points} | {requests} | {non_empty_rate} | {failed_points} |".format(**row)
            )

        point_order = _ordered_unique(
            _point_key(point)
            for server in suite_servers
            for point in server["suite_report"].get("points", [])
        )
        observations: list[str] = []
        baseline_suite_server = _find_server_in_collection(suite_servers, baseline_server)
        for point_key in point_order:
            point_rows = []
            point_label = None
            method = None
            measure_label = None
            differing_values: list[str] = []
            baseline_value: float | None = None
            if baseline_suite_server is not None:
                baseline_point = _find_point(baseline_suite_server["suite_report"].get("points", []), point_key)
                if baseline_point is not None:
                    baseline_metrics = _measured_request_metrics(baseline_point)
                    metric_key, measure_label = _preferred_result_metric(baseline_point.get("method"), baseline_metrics)
                    baseline_value = _mean_numeric(baseline_metrics, metric_key) if metric_key is not None else None
            for server in suite_servers:
                point = _find_point(server["suite_report"].get("points", []), point_key)
                if point is None:
                    continue
                point_label = point.get("label")
                method = point.get("method")
                measured_metrics = _measured_request_metrics(point)
                metric_key, measure_label = _preferred_result_metric(point.get("method"), measured_metrics)
                result_value = _mean_numeric(measured_metrics, metric_key) if metric_key is not None else None
                if baseline_value is None and baseline_suite_server is None:
                    baseline_value = result_value
                point_rows.append(
                    {
                        "server": _linked_server_name(server["display_name"], server_links),
                        "success": "yes" if point.get("success") else "no",
                        "mean_ms": _format_float(point.get("summary", {}).get("mean_ms")),
                        "p95_ms": _format_float(point.get("summary", {}).get("p95_ms")),
                        "non_empty_rate": _format_percent(_non_empty_rate(measured_metrics)),
                        "result_value": _format_result_value(result_value),
                        "delta": _format_delta(result_value, baseline_value),
                        "validation": _validation_text(point),
                        "sort_avg_ms": point.get("summary", {}).get("mean_ms"),
                    }
                )
                differing_values.append(_format_result_value(result_value))
            if point_label is None or method is None or measure_label is None:
                continue
            lines.append("")
            lines.append(f"### {point_label}")
            lines.append("")
            lines.append(f"Method: `{method}`")
            lines.append("")
            baseline_label = baseline_server["display_name"] if baseline_server is not None else point_rows[0]["server"]
            lines.append(f"| Server | Success | Mean ms | P95 ms | Non-empty % | {measure_label} | Delta vs {baseline_label} | Validation |")
            lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |")
            for row in _sort_rows_by_average(point_rows, "sort_avg_ms"):
                lines.append(
                    "| {server} | {success} | {mean_ms} | {p95_ms} | {non_empty_rate} | {result_value} | {delta} | {validation} |".format(**row)
                )
            unique_values = {value for value in differing_values if value != "n/a"}
            if len(unique_values) > 1:
                observations.append(f"{point_label}: result differences detected ({', '.join(sorted(unique_values))}).")
        if observations:
            lines.append("")
            lines.append("### Result Differences")
            lines.append("")
            for observation in observations:
                lines.append(f"- {observation}")

    return "\n".join(lines).rstrip() + "\n"


def _render_scenario_report(
    summary_path: Path,
    summary: dict[str, Any],
    servers: list[dict[str, Any]],
    baseline_server: dict[str, Any] | None,
    title: str | None,
    server_links: dict[str, str] | None = None,
) -> str:
    if server_links is None:
        server_links = {}
    lines: list[str] = []
    lines.append(f"# {title or 'Python LSP Scenario Comparison'}")
    lines.append("")
    lines.extend(_metadata_lines(summary_path, summary, baseline_server))
    lines.extend(_server_versions_lines(summary))
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append("| Server | Success | Scenarios | Total ms | Avg request ms | Requests | Non-empty % |")
    lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: |")
    overview_rows = []
    for server in servers:
        scenario_reports = server["report"].get("scenario_reports", [])
        request_metrics = [metric for report in scenario_reports for metric in _request_metrics(report.get("metrics", []))]
        avg_request_ms = _mean_duration(request_metrics)
        overview_rows.append(
            {
                "server": _linked_server_name(server["display_name"], server_links),
                "success": "yes" if server["success"] else "no",
                "scenarios": len(scenario_reports),
                "total_ms": _format_float(sum(report.get("total_duration_ms", 0.0) for report in scenario_reports)),
                "avg_request_ms": _format_float(avg_request_ms),
                "requests": len(request_metrics),
                "non_empty_rate": _format_percent(_non_empty_rate(request_metrics)),
                "sort_avg_ms": avg_request_ms,
            }
        )
    for row in _sort_rows_by_average(overview_rows, "sort_avg_ms"):
        lines.append(
            "| {server} | {success} | {scenarios} | {total_ms} | {avg_request_ms} | {requests} | {non_empty_rate} |".format(**row)
        )

    scenario_order = summary.get("requested_scenarios") or _ordered_unique(
        report.get("name")
        for server in servers
        for report in server["report"].get("scenario_reports", [])
    )
    baseline_reports = baseline_server["report"].get("scenario_reports", []) if baseline_server is not None else []
    baseline_label = baseline_server["display_name"] if baseline_server is not None else (servers[0]["display_name"] if servers else "baseline")
    for scenario_name in scenario_order:
        baseline_report = _find_by_name(baseline_reports, scenario_name)
        baseline_metrics = [] if baseline_report is None else _request_metrics(baseline_report.get("metrics", []))
        metric_key, measure_label = _preferred_result_metric_for_scenario(scenario_name, baseline_metrics)
        baseline_value = None if baseline_report is None or metric_key is None else _mean_numeric(baseline_metrics, metric_key)
        lines.append("")
        lines.append(f"## Scenario: {scenario_name}")
        lines.append("")
        if measure_label is None:
            lines.append(f"| Server | Success | Total ms | Avg request ms | Requests | Non-empty % |")
            lines.append("| --- | --- | ---: | ---: | ---: | ---: |")
        else:
            lines.append(f"| Server | Success | Total ms | Avg request ms | Requests | Non-empty % | {measure_label} | Delta vs {baseline_label} |")
            lines.append("| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |")
        scenario_rows = []
        for server in servers:
            report = _find_by_name(server["report"].get("scenario_reports", []), scenario_name)
            if report is None:
                continue
            request_metrics = _request_metrics(report.get("metrics", []))
            metric_key, measure_label = _preferred_result_metric_for_scenario(scenario_name, request_metrics)
            metric_value = None if metric_key is None else _mean_numeric(request_metrics, metric_key)
            if baseline_value is None and baseline_server is None:
                baseline_value = metric_value
            avg_request_ms = _mean_duration(request_metrics)
            if measure_label is None:
                scenario_rows.append(
                    {
                        "server": _linked_server_name(server["display_name"], server_links),
                        "success": "yes" if report.get("success") else "no",
                        "total_ms": _format_float(report.get("total_duration_ms")),
                        "avg_request_ms": _format_float(avg_request_ms),
                        "requests": len(request_metrics),
                        "non_empty_rate": _format_percent(_non_empty_rate(request_metrics)),
                        "sort_avg_ms": avg_request_ms,
                    }
                )
            else:
                scenario_rows.append(
                    {
                        "server": _linked_server_name(server["display_name"], server_links),
                        "success": "yes" if report.get("success") else "no",
                        "total_ms": _format_float(report.get("total_duration_ms")),
                        "avg_request_ms": _format_float(avg_request_ms),
                        "requests": len(request_metrics),
                        "non_empty_rate": _format_percent(_non_empty_rate(request_metrics)),
                        "metric_value": _format_result_value(metric_value),
                        "delta": _format_delta(metric_value, baseline_value),
                        "sort_avg_ms": avg_request_ms,
                    }
                )
        for row in _sort_rows_by_average(scenario_rows, "sort_avg_ms"):
            if measure_label is None:
                lines.append(
                    "| {server} | {success} | {total_ms} | {avg_request_ms} | {requests} | {non_empty_rate} |".format(**row)
                )
            else:
                lines.append(
                    "| {server} | {success} | {total_ms} | {avg_request_ms} | {requests} | {non_empty_rate} | {metric_value} | {delta} |".format(**row)
                )
    return "\n".join(lines).rstrip() + "\n"


def _metadata_lines(summary_path: Path, summary: dict[str, Any], baseline_server: dict[str, Any] | None) -> list[str]:
    generated_at = summary.get("generated_at")
    generated_text = generated_at if isinstance(generated_at, str) else datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = [
        f"Generated from `{summary_path}`",
        "",
        f"- Generated at: {generated_text}",
    ]
    if summary.get("config_path"):
        lines.append(f"- Config: `{summary['config_path']}`")
    requested_servers = summary.get("requested_servers")
    if isinstance(requested_servers, list) and requested_servers:
        lines.append(f"- Servers: {', '.join(str(item) for item in requested_servers)}")
    if baseline_server is not None:
        lines.append(f"- Baseline server: {baseline_server['display_name']} ({baseline_server['id']})")
    requested_benchmarks = summary.get("requested_benchmarks")
    if isinstance(requested_benchmarks, list) and requested_benchmarks:
        lines.append(f"- Benchmarks: {', '.join(str(item) for item in requested_benchmarks)}")
    requested_scenarios = summary.get("requested_scenarios")
    if isinstance(requested_scenarios, list) and requested_scenarios:
        lines.append(f"- Scenarios: {', '.join(str(item) for item in requested_scenarios)}")
    lines.append("")
    return lines


def _server_versions_lines(summary: dict[str, Any]) -> list[str]:
    servers = summary.get("servers")
    if not isinstance(servers, list) or not servers:
        return []
    lines = ["## Server Versions", "", "| Server | Version | Commit | Source |", "| --- | --- | --- | --- |"]
    for server in servers:
        version = server.get("version") if isinstance(server, dict) else None
        if not isinstance(version, dict):
            version = {}
        lines.append(
            "| {server} | {label} | {commit} | {source} |".format(
                server=server.get("display_name", server.get("id", "server")),
                label=_escape_table(str(version.get("label") or "unknown")),
                commit=_escape_table(str(version.get("short_commit") or version.get("commit") or "n/a")),
                source=_escape_table(str(version.get("source_path") or server.get("source_path") or "n/a")),
            )
        )
    lines.append("")
    return lines


def _load_server_entry(summary_path: Path, entry: dict[str, Any]) -> dict[str, Any]:
    report_path = _resolve_report_path(summary_path, entry["output_path"])
    report = _read_json(report_path)
    return {
        "id": entry.get("id"),
        "display_name": entry.get("display_name", entry.get("id", "server")),
        "success": bool(entry.get("success", False)),
        "report_path": report_path,
        "report": report,
    }


def _resolve_report_path(summary_path: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute() and path.exists():
        return path
    candidates = [Path.cwd() / path, summary_path.parent / path, summary_path.parent / path.name]
    for candidate in candidates:
        if candidate.exists():
            return candidate.resolve()
    return path.resolve()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _request_metrics(metrics: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [metric for metric in metrics if metric.get("kind") == "request"]


def _measured_request_metrics(point: dict[str, Any]) -> list[dict[str, Any]]:
    return [metric for metric in _request_metrics(point.get("metrics", [])) if metric.get("context", {}).get("phase") == "measured"]


def _non_empty_rate(metrics: list[dict[str, Any]]) -> float | None:
    present = [metric for metric in metrics if metric.get("result_summary", {}).get("present")]
    if not present:
        return None
    non_empty = [metric for metric in present if not metric.get("result_summary", {}).get("empty")]
    return len(non_empty) / len(present)


def _mean_numeric(metrics: list[dict[str, Any]], key: str) -> float | None:
    values: list[float] = []
    for metric in metrics:
        result_summary = metric.get("result_summary", {})
        value = result_summary.get(key)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            continue
        values.append(float(value))
    if not values:
        return None
    return sum(values) / len(values)


def _mean_duration(metrics: list[dict[str, Any]]) -> float | None:
    durations = [float(metric["duration_ms"]) for metric in metrics if isinstance(metric.get("duration_ms"), (int, float))]
    if not durations:
        return None
    return sum(durations) / len(durations)


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


def _find_by_name(items: list[dict[str, Any]], name: str) -> dict[str, Any] | None:
    for item in items:
        if item.get("name") == name:
            return item
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


def _sort_rows_by_average(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    def sort_key(row: dict[str, Any]) -> tuple[float, str]:
        value = row.get(key)
        if isinstance(value, (int, float)):
            return float(value), str(row.get("server", ""))
        return float("inf"), str(row.get("server", ""))

    return sorted(rows, key=sort_key)


def _format_float(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}"


def _format_percent(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value * 100:.0f}%"


def _format_result_value(value: float | None) -> str:
    if value is None:
        return "n/a"
    return f"{value:.2f}"


def _format_delta(value: float | None, baseline: float | None) -> str:
    if value is None or baseline is None:
        return "n/a"
    delta = value - baseline
    if abs(delta) < 0.005:
        return "0.00"
    return f"{delta:+.2f}"


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|")


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


def _validation_text(point: dict[str, Any]) -> str:
    validation = point.get("summary", {}).get("validation", {})
    if validation.get("passed", True):
        return "pass"
    return f"fail ({validation.get('failure_count', 0)})"
