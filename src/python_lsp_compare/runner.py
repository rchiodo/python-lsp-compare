from __future__ import annotations

import json
import statistics
import sys
import tempfile
import time
from pathlib import Path
from typing import Callable, Sequence

from .benchmark_suites import BenchmarkPoint, BenchmarkSuite, BenchmarkValidation, discover_benchmark_suites
from .environments import cleanup_benchmark_environment, prepare_benchmark_environment
from .lsp_client import LspClient
from .metrics import BenchmarkPointReport, BenchmarkSuiteReport, CallMetric, RunReport, ScenarioReport
from .scenarios.base import SAMPLE_SOURCE, ScenarioContext
from .scenarios.builtin import BUILTIN_SCENARIOS


def run_scenarios(
    command: Sequence[str],
    scenario_names: Sequence[str] | None = None,
    timeout_seconds: float = 10.0,
) -> RunReport:
    selected_names = list(scenario_names or BUILTIN_SCENARIOS.keys())
    unknown = [name for name in selected_names if name not in BUILTIN_SCENARIOS]
    if unknown:
        raise ValueError(f"Unknown scenarios: {', '.join(unknown)}")

    started_at = time.time()
    scenario_reports: list[ScenarioReport] = []
    for name in selected_names:
        scenario = BUILTIN_SCENARIOS[name]
        scenario_reports.append(_run_single_scenario(command, scenario, timeout_seconds))

    return RunReport(
        server_command=list(command),
        requested_scenarios=selected_names,
        requested_benchmarks=[],
        started_at_unix=started_at,
        finished_at_unix=time.time(),
        scenario_reports=scenario_reports,
        benchmark_reports=[],
    )


def run_benchmarks(
    command: Sequence[str],
    benchmark_names: Sequence[str] | None = None,
    timeout_seconds: float = 10.0,
    benchmark_root: Path | None = None,
    install_requirements: bool = False,
    python_executable: str | None = None,
    environment_mode: str = "current",
    environment_root: Path | None = None,
    progress: Callable[[str], None] | None = None,
) -> RunReport:
    suites = discover_benchmark_suites(benchmark_root)
    selected_names = list(benchmark_names or suites.keys())
    unknown = [name for name in selected_names if name not in suites]
    if unknown:
        raise ValueError(f"Unknown benchmarks: {', '.join(unknown)}")

    started_at = time.time()
    benchmark_reports: list[BenchmarkSuiteReport] = []
    for name in selected_names:
        benchmark_reports.append(
            _run_single_benchmark_suite(
                command=command,
                suite=suites[name],
                timeout_seconds=timeout_seconds,
                install_requirements=install_requirements,
                python_executable=python_executable or sys.executable,
                environment_mode=environment_mode,
                environment_root=environment_root,
                progress=progress,
            )
        )
    return RunReport(
        server_command=list(command),
        requested_scenarios=[],
        requested_benchmarks=selected_names,
        started_at_unix=started_at,
        finished_at_unix=time.time(),
        scenario_reports=[],
        benchmark_reports=benchmark_reports,
    )


def write_report(report: RunReport, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report.to_dict(), indent=2), encoding="utf-8")


def _run_single_scenario(command: Sequence[str], scenario, timeout_seconds: float) -> ScenarioReport:
    started_perf = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="python-lsp-compare-") as temp_dir:
        workspace_path = Path(temp_dir)
        document_path = workspace_path / "sample.py"
        document_path.write_text(SAMPLE_SOURCE, encoding="utf-8")
        context = ScenarioContext(
            workspace_path=workspace_path,
            document_path=document_path,
            document_uri=document_path.as_uri(),
        )
        client = LspClient(command, timeout_seconds=timeout_seconds)
        client.start()
        error_message: str | None = None
        success = False
        try:
            client.initialize(workspace_path)
            client.initialized()
            scenario.run(client, context)
            client.shutdown()
            success = True
        except Exception as exc:
            error_message = str(exc)
        finally:
            try:
                client.exit()
            except Exception:
                pass
            client.close()
        if client.stderr_lines and error_message is not None:
            error_message = f"{error_message}\n--- server stderr ---\n" + "\n".join(client.stderr_lines)
        return ScenarioReport(
            name=scenario.name,
            description=scenario.description,
            success=success,
            total_duration_ms=(time.perf_counter() - started_perf) * 1000,
            metrics=client.metrics,
            error_message=error_message,
            summary=_summarize_metrics(client.metrics),
        )


def _run_single_benchmark_suite(
    *,
    command: Sequence[str],
    suite: BenchmarkSuite,
    timeout_seconds: float,
    install_requirements: bool,
    python_executable: str,
    environment_mode: str,
    environment_root: Path | None,
    progress: Callable[[str], None] | None,
) -> BenchmarkSuiteReport:
    started_perf = time.perf_counter()
    _emit_progress(progress, f"[{suite.name}] preparing benchmark environment")
    benchmark_environment = prepare_benchmark_environment(
        suite=suite,
        command=command,
        environment_mode=environment_mode,
        base_python_executable=python_executable,
        install_requirements=install_requirements,
        environment_root=environment_root,
        logger=progress,
    )

    _emit_progress(progress, f"[{suite.name}] launch command: {benchmark_environment.launch_command}")
    _emit_progress(progress, f"[{suite.name}] workspace root: {benchmark_environment.workspace_root}")
    _emit_progress(progress, f"[{suite.name}] python: {benchmark_environment.python_executable}")
    client = LspClient(
        benchmark_environment.launch_command,
        timeout_seconds=timeout_seconds,
        cwd=suite.root_path,
        env=benchmark_environment.process_env,
        trace=progress,
    )
    client.start()
    error_message: str | None = None
    point_reports: list[BenchmarkPointReport] = []
    success = True
    try:
        _emit_progress(progress, f"[{suite.name}] sending initialize request (timeout={timeout_seconds}s)")
        client.initialize(benchmark_environment.workspace_root)
        _emit_progress(progress, f"[{suite.name}] initialize response received")
        client.initialized()
        _emit_progress(progress, f"[{suite.name}] send workspace configuration")
        client.did_change_configuration(
            benchmark_environment.workspace_settings,
            context={"suite": suite.name, "phase": "setup"},
        )
        _emit_progress(progress, f"[{suite.name}] open benchmark documents")
        opened = _open_benchmark_documents(client, suite)
        try:
            for method, points in suite.points_by_method.items():
                for point in points:
                    point_reports.append(
                        _run_benchmark_point(
                            client=client,
                            suite=suite,
                            method=method,
                            point=point,
                            progress=progress,
                        )
                    )
        finally:
            for uri in reversed(opened):
                client.did_close(uri,)
        client.shutdown()
        success = all(point.success for point in point_reports)
    except Exception as exc:
        success = False
        error_message = str(exc)
        _emit_progress(progress, f"[{suite.name}] ERROR: {exc}")
        if client.stderr_lines:
            _emit_progress(progress, f"[{suite.name}] server stderr (last 10 lines):")
            for line in client.stderr_lines[-10:]:
                _emit_progress(progress, f"[{suite.name}]   {line}")
    finally:
        try:
            client.exit()
        except Exception:
            pass
        client.close()
        cleanup_benchmark_environment(benchmark_environment)
    if client.stderr_lines and error_message is not None:
        error_message = f"{error_message}\n--- server stderr ---\n" + "\n".join(client.stderr_lines)
    _emit_progress(progress, f"[{suite.name}] {'ok' if success else 'failed'}")
    return BenchmarkSuiteReport(
        name=suite.name,
        description=suite.description,
        workspace_dir=str(suite.workspace_dir),
        requirements_file=None if suite.requirements_file is None else str(suite.requirements_file),
        install_packages=suite.install_packages,
        environment_mode=benchmark_environment.mode,
        environment_path=None if benchmark_environment.root_path is None else str(benchmark_environment.root_path),
        python_executable=benchmark_environment.python_executable,
        success=success,
        total_duration_ms=(time.perf_counter() - started_perf) * 1000,
        points=point_reports,
        metrics=client.metrics,
        error_message=error_message,
        summary=_summarize_benchmark_suite(point_reports, client.metrics),
    )


def _run_benchmark_point(
    *,
    client: LspClient,
    suite: BenchmarkSuite,
    method: str,
    point: BenchmarkPoint,
    progress: Callable[[str], None] | None,
) -> BenchmarkPointReport:
    metrics: list[CallMetric] = []
    error_message: str | None = None
    success = True
    uri = point.file_path.as_uri()
    _emit_progress(progress, f"[{suite.name}] {point.label} start ({method})")
    for iteration in range(suite.warmup_iterations + suite.iterations):
        is_warmup = iteration < suite.warmup_iterations
        before = len(client.metrics)
        context = {
            "suite": suite.name,
            "label": point.label,
            "file_path": str(point.file_path),
            "line": point.line,
            "character": point.character,
            "phase": "warmup" if is_warmup else "measured",
            "iteration": iteration + 1 if is_warmup else iteration - suite.warmup_iterations + 1,
        }
        try:
            _dispatch_benchmark_request(client, method, uri, point.line, point.character, context)
        except Exception as exc:
            success = False
            error_message = str(exc)
            _emit_progress(progress, f"[{suite.name}] {point.label} request failed: {error_message}")
            break
        metrics.extend(client.metrics[before:])

    measured_metrics = [metric for metric in metrics if metric.context.get("phase") == "measured" and metric.kind == "request"]
    validation_summary = _validate_benchmark_point_results(method, point.validation, measured_metrics)
    if not validation_summary["passed"]:
        success = False
        error_message = _combine_error_messages(error_message, validation_summary["message"])
    summary = _summarize_metrics(measured_metrics)
    summary["validation"] = validation_summary
    _emit_progress(
        progress,
        f"[{suite.name}] {point.label} {'ok' if success else 'failed'}"
        + (f": {error_message}" if error_message else ""),
    )
    return BenchmarkPointReport(
        label=point.label,
        method=method,
        file_path=str(point.file_path),
        line=point.line,
        character=point.character,
        success=success,
        warmup_iterations=suite.warmup_iterations,
        measured_iterations=suite.iterations,
        metrics=metrics,
        summary=summary,
        error_message=error_message,
    )


def _dispatch_benchmark_request(
    client: LspClient,
    method: str,
    uri: str,
    line: int,
    character: int,
    context: dict[str, object],
) -> object:
    if method == "textDocument/hover":
        return client.hover(uri, line, character, context=context)
    if method == "textDocument/completion":
        return client.completion(uri, line, character, context=context)
    if method == "textDocument/documentSymbol":
        return client.document_symbols(uri, context=context)
    if method == "textDocument/definition":
        return client.definition(uri, line, character, context=context)
    if method == "textDocument/references":
        return client.references(uri, line, character, context=context)
    raise ValueError(f"Unsupported benchmark method: {method}")


def _open_benchmark_documents(client: LspClient, suite: BenchmarkSuite) -> list[str]:
    opened: list[str] = []
    seen: set[str] = set()
    for points in suite.points_by_method.values():
        for point in points:
            uri = point.file_path.as_uri()
            if uri in seen:
                continue
            seen.add(uri)
            client.did_open(uri, point.file_path.read_text(encoding="utf-8"), context={"suite": suite.name, "phase": "setup"})
            opened.append(uri)
    return opened


def _summarize_benchmark_suite(points: Sequence[BenchmarkPointReport], metrics: Sequence[CallMetric]) -> dict[str, object]:
    summary = _summarize_metrics(metrics)
    by_method: dict[str, dict[str, object]] = {}
    for point in points:
        current = by_method.setdefault(point.method, {"point_count": 0, "durations_ms": []})
        current["point_count"] = int(current["point_count"]) + 1
        current["durations_ms"].extend(metric.duration_ms for metric in point.metrics if metric.context.get("phase") == "measured")
    summary["by_method"] = {
        method: _summarize_values(value["durations_ms"], extra={"point_count": value["point_count"]})
        for method, value in by_method.items()
    }
    summary["validation"] = {
        "point_count": len(points),
        "passed_point_count": len([point for point in points if point.summary.get("validation", {}).get("passed")]),
        "failed_point_count": len([point for point in points if not point.summary.get("validation", {}).get("passed", True)]),
    }
    return summary


def _summarize_metrics(metrics: Sequence[CallMetric]) -> dict[str, object]:
    request_metrics = [metric for metric in metrics if metric.kind == "request"]
    durations = [metric.duration_ms for metric in request_metrics]
    summary = _summarize_values(
        durations,
        extra={
            "request_count": len(request_metrics),
            "notification_count": len([metric for metric in metrics if metric.kind == "notification"]),
            "success_count": len([metric for metric in request_metrics if metric.success]),
            "failure_count": len([metric for metric in request_metrics if not metric.success]),
            "bytes_sent": sum(metric.bytes_sent for metric in metrics),
            "bytes_received": sum(metric.bytes_received for metric in metrics),
        },
    )
    summary["result_summary"] = _summarize_result_metrics(request_metrics)
    return summary


def _summarize_values(values: Sequence[float], extra: dict[str, object] | None = None) -> dict[str, object]:
    summary: dict[str, object] = dict(extra or {})
    if not values:
        summary.update({"min_ms": None, "max_ms": None, "mean_ms": None, "median_ms": None, "p95_ms": None})
        return summary
    sorted_values = sorted(values)
    summary.update(
        {
            "min_ms": min(sorted_values),
            "max_ms": max(sorted_values),
            "mean_ms": statistics.fmean(sorted_values),
            "median_ms": statistics.median(sorted_values),
            "p95_ms": _percentile(sorted_values, 0.95),
        }
    )
    return summary


def _summarize_result_metrics(metrics: Sequence[CallMetric]) -> dict[str, object]:
    result_metrics = [metric for metric in metrics if metric.result_summary]
    present_count = len([metric for metric in result_metrics if metric.result_summary.get("present")])
    empty_count = len([metric for metric in result_metrics if metric.result_summary.get("empty")])
    non_empty_count = len([metric for metric in result_metrics if metric.result_summary.get("present") and not metric.result_summary.get("empty")])

    numeric_fields: dict[str, list[float]] = {}
    for metric in result_metrics:
        for key, value in metric.result_summary.items():
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                continue
            numeric_fields.setdefault(key, []).append(float(value))

    return {
        "present_count": present_count,
        "empty_count": empty_count,
        "non_empty_count": non_empty_count,
        "non_empty_rate": None if present_count == 0 else non_empty_count / present_count,
        "metrics": {
            key: _summarize_numeric_values(values)
            for key, values in sorted(numeric_fields.items())
        },
    }


def _summarize_numeric_values(values: Sequence[float]) -> dict[str, float | None]:
    if not values:
        return {"min": None, "max": None, "mean": None, "median": None, "p95": None}
    sorted_values = sorted(values)
    return {
        "min": min(sorted_values),
        "max": max(sorted_values),
        "mean": statistics.fmean(sorted_values),
        "median": statistics.median(sorted_values),
        "p95": _percentile(sorted_values, 0.95),
    }


def _validate_benchmark_point_results(
    method: str,
    validation: BenchmarkValidation,
    measured_metrics: Sequence[CallMetric],
) -> dict[str, object]:
    thresholds = _effective_validation_thresholds(method, validation)
    failures: list[str] = []
    checked_metrics = 0
    for metric in measured_metrics:
        checked_metrics += 1
        result_summary = metric.result_summary
        if thresholds["require_non_empty"] and result_summary.get("empty"):
            failures.append(f"iteration {metric.context.get('iteration', '?')}: empty result")
        if not _passes_numeric_threshold(result_summary.get("completion_item_count"), thresholds["min_completion_items"]):
            failures.append(
                f"iteration {metric.context.get('iteration', '?')}: completion_item_count={result_summary.get('completion_item_count')} < {thresholds['min_completion_items']}"
            )
        if not _passes_numeric_threshold(result_summary.get("hover_text_char_count"), thresholds["min_hover_text_chars"]):
            failures.append(
                f"iteration {metric.context.get('iteration', '?')}: hover_text_char_count={result_summary.get('hover_text_char_count')} < {thresholds['min_hover_text_chars']}"
            )
        if not _passes_numeric_threshold(result_summary.get("symbol_count"), thresholds["min_symbol_count"]):
            failures.append(
                f"iteration {metric.context.get('iteration', '?')}: symbol_count={result_summary.get('symbol_count')} < {thresholds['min_symbol_count']}"
            )
        if not _passes_numeric_threshold(result_summary.get("location_count"), thresholds["min_location_count"]):
            failures.append(
                f"iteration {metric.context.get('iteration', '?')}: location_count={result_summary.get('location_count')} < {thresholds['min_location_count']}"
            )
        if not _passes_numeric_threshold(result_summary.get("size_chars"), thresholds["min_size_chars"]):
            failures.append(
                f"iteration {metric.context.get('iteration', '?')}: size_chars={result_summary.get('size_chars')} < {thresholds['min_size_chars']}"
            )
    message = None if not failures else "Result validation failed: " + "; ".join(failures)
    return {
        "passed": not failures,
        "checked_iterations": checked_metrics,
        "failure_count": len(failures),
        "message": message,
        "rules": thresholds,
    }


def _effective_validation_thresholds(method: str, validation: BenchmarkValidation) -> dict[str, int | bool | None]:
    thresholds: dict[str, int | bool | None] = {
        "require_non_empty": validation.require_non_empty,
        "min_completion_items": validation.min_completion_items,
        "min_hover_text_chars": validation.min_hover_text_chars,
        "min_symbol_count": validation.min_symbol_count,
        "min_location_count": validation.min_location_count,
        "min_size_chars": validation.min_size_chars,
    }
    if method == "textDocument/completion" and thresholds["min_completion_items"] is None:
        thresholds["min_completion_items"] = 1
    if method == "textDocument/hover" and thresholds["min_hover_text_chars"] is None:
        thresholds["min_hover_text_chars"] = 1
    if method == "textDocument/documentSymbol" and thresholds["min_symbol_count"] is None:
        thresholds["min_symbol_count"] = 1
    if method in {"textDocument/definition", "textDocument/references"} and thresholds["min_location_count"] is None:
        thresholds["min_location_count"] = 1
    if thresholds["require_non_empty"] is None:
        thresholds["require_non_empty"] = method in {
            "textDocument/completion",
            "textDocument/hover",
            "textDocument/documentSymbol",
            "textDocument/definition",
            "textDocument/references",
        }
    return thresholds


def _passes_numeric_threshold(value: object, minimum: int | bool | None) -> bool:
    if minimum is None:
        return True
    if isinstance(minimum, bool):
        return True
    if not isinstance(value, (int, float)):
        return False
    return float(value) >= float(minimum)


def _combine_error_messages(existing: str | None, new_message: str | None) -> str | None:
    if existing and new_message:
        return f"{existing}; {new_message}"
    return existing or new_message


def _emit_progress(progress: Callable[[str], None] | None, message: str) -> None:
    if progress is not None:
        progress(message)


def _percentile(sorted_values: Sequence[float], percentile: float) -> float:
    if len(sorted_values) == 1:
        return sorted_values[0]
    index = (len(sorted_values) - 1) * percentile
    lower = int(index)
    upper = min(lower + 1, len(sorted_values) - 1)
    if lower == upper:
        return sorted_values[lower]
    remainder = index - lower
    return sorted_values[lower] * (1 - remainder) + sorted_values[upper] * remainder
