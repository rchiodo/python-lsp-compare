from __future__ import annotations

import io
import json
import statistics
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Sequence

from .benchmark_suites import BenchmarkEditPoint, BenchmarkPoint, BenchmarkSuite, BenchmarkValidation, TspBenchmarkEditPoint, TspBenchmarkPoint, discover_benchmark_suites
from .environments import cleanup_benchmark_environment, prepare_benchmark_environment
from .lsp_client import LspClient
from .metrics import BenchmarkPointReport, BenchmarkSuiteReport, CallMetric, RunReport, ScenarioReport
from .scenarios.base import SAMPLE_SOURCE, ScenarioContext
from .scenarios.builtin import BUILTIN_SCENARIOS
from .tsp_semantic_tokens import compute_semantic_tokens


def run_scenarios(
    command: Sequence[str],
    scenario_names: Sequence[str] | None = None,
    timeout_seconds: float = 10.0,
    response_log_path: Path | None = None,
) -> RunReport:
    selected_names = list(scenario_names or BUILTIN_SCENARIOS.keys())
    unknown = [name for name in selected_names if name not in BUILTIN_SCENARIOS]
    if unknown:
        raise ValueError(f"Unknown scenarios: {', '.join(unknown)}")

    started_at = time.time()
    scenario_reports: list[ScenarioReport] = []
    response_log = _open_response_log(response_log_path)
    try:
        for name in selected_names:
            scenario = BUILTIN_SCENARIOS[name]
            scenario_reports.append(_run_single_scenario(command, scenario, timeout_seconds, response_log=response_log))
    finally:
        if response_log is not None:
            response_log.close()

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
    response_log_path: Path | None = None,
    allowed_protocols: Sequence[str] | None = None,
    command_for_protocol: Callable[[str], Sequence[str]] | None = None,
) -> RunReport:
    suites = discover_benchmark_suites(benchmark_root)
    selected_names = list(benchmark_names or suites.keys())
    unknown = [name for name in selected_names if name not in suites]
    if unknown:
        raise ValueError(f"Unknown benchmarks: {', '.join(unknown)}")
    if allowed_protocols is not None:
        allowed = set(allowed_protocols)
        skipped = [name for name in selected_names if suites[name].protocol not in allowed]
        for name in skipped:
            _emit_progress(progress, f"[{name}] skipped: protocol {suites[name].protocol} not supported by this server")
        selected_names = [name for name in selected_names if suites[name].protocol in allowed]

    started_at = time.time()
    benchmark_reports: list[BenchmarkSuiteReport] = []
    response_log = _open_response_log(response_log_path)
    try:
        for name in selected_names:
            suite = suites[name]
            suite_command = list(command_for_protocol(suite.protocol)) if command_for_protocol is not None else list(command)
            benchmark_reports.append(
                _run_single_benchmark_suite(
                    command=suite_command,
                    suite=suite,
                    timeout_seconds=timeout_seconds,
                    install_requirements=install_requirements,
                    python_executable=python_executable or sys.executable,
                    environment_mode=environment_mode,
                    environment_root=environment_root,
                    progress=progress,
                    response_log=response_log,
                )
            )
    finally:
        if response_log is not None:
            response_log.close()
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


def _run_single_scenario(command: Sequence[str], scenario, timeout_seconds: float, response_log: io.TextIOBase | None = None) -> ScenarioReport:
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
            client.did_change_configuration({})
            before = len(client.metrics)
            scenario.run(client, context)
            _write_scenario_responses(response_log, scenario.name, client.metrics[before:])
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
    response_log: io.TextIOBase | None = None,
) -> BenchmarkSuiteReport:
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
    started_perf = time.perf_counter()

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
        # Track document versions per-URI across benchmark points.
        # did_open uses version 1, so the next version is 2.
        document_versions: dict[str, int] = {uri: 2 for uri in opened}
        try:
            if suite.protocol == "tsp":
                protocol_version = client.tsp_get_supported_protocol_version(context={"suite": suite.name, "phase": "setup"})
                _emit_progress(progress, f"[{suite.name}] tsp protocol version: {protocol_version}")
                for point in suite.tsp_points:
                    point_reports.append(
                        _run_tsp_benchmark_point(
                            client=client,
                            suite=suite,
                            point=point,
                            progress=progress,
                            response_log=response_log,
                        )
                    )
                for edit_point in suite.tsp_edit_points:
                    point_reports.append(
                        _run_tsp_edit_benchmark_point(
                            client=client,
                            suite=suite,
                            edit_point=edit_point,
                            document_versions=document_versions,
                            progress=progress,
                            response_log=response_log,
                        )
                    )
            else:
                for method, points in suite.points_by_method.items():
                    for point in points:
                        point_reports.append(
                            _run_benchmark_point(
                                client=client,
                                suite=suite,
                                method=method,
                                point=point,
                                progress=progress,
                                response_log=response_log,
                            )
                        )
                for edit_point in suite.edit_points:
                    point_reports.append(
                        _run_edit_benchmark_point(
                            client=client,
                            suite=suite,
                            edit_point=edit_point,
                            document_versions=document_versions,
                            progress=progress,
                            response_log=response_log,
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
    response_log: io.TextIOBase | None = None,
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
            result = _dispatch_benchmark_request(client, method, uri, point.line, point.character, context)
        except Exception as exc:
            success = False
            error_message = str(exc)
            _emit_progress(progress, f"[{suite.name}] {point.label} request failed: {error_message}")
            break
        metrics.extend(client.metrics[before:])
        if response_log is not None and not is_warmup:
            _write_response_entry(response_log, context, method, result)

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


def _run_tsp_benchmark_point(
    *,
    client: LspClient,
    suite: BenchmarkSuite,
    point: TspBenchmarkPoint,
    progress: Callable[[str], None] | None,
    response_log: io.TextIOBase | None = None,
) -> BenchmarkPointReport:
    metrics: list[CallMetric] = []
    error_message: str | None = None
    success = True
    uri = point.file_path.as_uri()
    _emit_progress(progress, f"[{suite.name}] {point.label} start ({point.request})")
    for iteration in range(suite.warmup_iterations + suite.iterations):
        is_warmup = iteration < suite.warmup_iterations
        context = {
            "suite": suite.name,
            "label": point.label,
            "file_path": str(point.file_path),
            "line": point.start_line,
            "character": point.start_character,
            "phase": "warmup" if is_warmup else "measured",
            "iteration": iteration + 1 if is_warmup else iteration - suite.warmup_iterations + 1,
        }
        try:
            snapshot = client.tsp_get_snapshot(context={"suite": suite.name, "label": point.label, "phase": "snapshot"})
            before = len(client.metrics)
            result = _dispatch_tsp_request(
                client,
                point.request,
                point.file_path,
                uri,
                point.start_line,
                point.start_character,
                point.end_line,
                point.end_character,
                int(snapshot),
                context,
            )
        except Exception as exc:
            success = False
            error_message = str(exc)
            _emit_progress(progress, f"[{suite.name}] {point.label} request failed: {error_message}")
            break
        metrics.extend(client.metrics[before:])
        if response_log is not None and not is_warmup:
            _write_response_entry(response_log, context, point.request, result)

    measured_metrics = [metric for metric in metrics if metric.context.get("phase") == "measured" and metric.kind == "request"]
    validation_summary = _validate_benchmark_point_results(point.request, point.validation, measured_metrics)
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
        method=point.request,
        file_path=str(point.file_path),
        line=point.start_line,
        character=point.start_character,
        success=success,
        warmup_iterations=suite.warmup_iterations,
        measured_iterations=suite.iterations,
        metrics=metrics,
        summary=summary,
        error_message=error_message,
    )


def _run_tsp_edit_benchmark_point(
    *,
    client: LspClient,
    suite: BenchmarkSuite,
    edit_point: TspBenchmarkEditPoint,
    document_versions: dict[str, int],
    progress: Callable[[str], None] | None,
    response_log: io.TextIOBase | None = None,
) -> BenchmarkPointReport:
    metrics: list[CallMetric] = []
    error_message: str | None = None
    success = True
    uri = edit_point.file_path.as_uri()
    label = f"{edit_point.label} (edit+{edit_point.request.split('/')[-1]})"
    _emit_progress(progress, f"[{suite.name}] {label} start")
    version = document_versions.get(uri, 2)
    for iteration in range(suite.warmup_iterations + suite.iterations):
        is_warmup = iteration < suite.warmup_iterations
        context = {
            "suite": suite.name,
            "label": label,
            "file_path": str(edit_point.file_path),
            "line": edit_point.query_start_line,
            "character": edit_point.query_start_character,
            "phase": "warmup" if is_warmup else "measured",
            "iteration": iteration + 1 if is_warmup else iteration - suite.warmup_iterations + 1,
        }
        try:
            insert_line = edit_point.edit_line
            new_line = edit_point.edit_text + "\n"
            client.did_change(
                uri,
                version,
                [
                    {
                        "range": {
                            "start": {"line": insert_line, "character": 0},
                            "end": {"line": insert_line, "character": 0},
                        },
                        "text": new_line,
                    }
                ],
                context={"suite": suite.name, "label": label, "phase": "edit"},
            )
            version += 1
            snapshot = client.tsp_get_snapshot(context={"suite": suite.name, "label": label, "phase": "snapshot"})
            before = len(client.metrics)
            result = _dispatch_tsp_request(
                client,
                edit_point.request,
                edit_point.file_path,
                uri,
                edit_point.query_start_line,
                edit_point.query_start_character,
                edit_point.query_end_line,
                edit_point.query_end_character,
                int(snapshot),
                context,
            )
            metrics.extend(client.metrics[before:])
            if response_log is not None and not is_warmup:
                _write_response_entry(response_log, context, edit_point.request, result)
            client.did_change(
                uri,
                version,
                [
                    {
                        "range": {
                            "start": {"line": insert_line, "character": 0},
                            "end": {"line": insert_line + 1, "character": 0},
                        },
                        "text": "",
                    }
                ],
                context={"suite": suite.name, "label": label, "phase": "revert"},
            )
            version += 1
        except Exception as exc:
            success = False
            error_message = str(exc)
            _emit_progress(progress, f"[{suite.name}] {label} request failed: {error_message}")
            break

    document_versions[uri] = version
    measured_metrics = [metric for metric in metrics if metric.context.get("phase") == "measured" and metric.kind == "request"]
    validation_summary = _validate_benchmark_point_results(edit_point.request, edit_point.validation, measured_metrics)
    if not validation_summary["passed"]:
        success = False
        error_message = _combine_error_messages(error_message, validation_summary["message"])
    summary = _summarize_metrics(measured_metrics)
    summary["validation"] = validation_summary
    _emit_progress(
        progress,
        f"[{suite.name}] {label} {'ok' if success else 'failed'}"
        + (f": {error_message}" if error_message else ""),
    )
    return BenchmarkPointReport(
        label=label,
        method=edit_point.request,
        file_path=str(edit_point.file_path),
        line=edit_point.query_start_line,
        character=edit_point.query_start_character,
        success=success,
        warmup_iterations=suite.warmup_iterations,
        measured_iterations=suite.iterations,
        metrics=metrics,
        summary=summary,
        error_message=error_message,
    )


def _run_edit_benchmark_point(
    *,
    client: LspClient,
    suite: BenchmarkSuite,
    edit_point: BenchmarkEditPoint,
    document_versions: dict[str, int],
    progress: Callable[[str], None] | None,
    response_log: io.TextIOBase | None = None,
) -> BenchmarkPointReport:
    metrics: list[CallMetric] = []
    error_message: str | None = None
    success = True
    uri = edit_point.file_path.as_uri()
    original_text = edit_point.file_path.read_text(encoding="utf-8")
    original_lines = original_text.splitlines(keepends=True)
    method = edit_point.query_method
    label = f"{edit_point.label} (edit+{method.split('/')[-1]})"
    _emit_progress(progress, f"[{suite.name}] {label} start")
    version = document_versions.get(uri, 2)
    for iteration in range(suite.warmup_iterations + suite.iterations):
        is_warmup = iteration < suite.warmup_iterations
        context = {
            "suite": suite.name,
            "label": label,
            "file_path": str(edit_point.file_path),
            "line": edit_point.query_line,
            "character": edit_point.query_character,
            "phase": "warmup" if is_warmup else "measured",
            "iteration": iteration + 1 if is_warmup else iteration - suite.warmup_iterations + 1,
        }
        try:
            # Insert the edit text as a new line.
            insert_line = edit_point.edit_line
            new_line = edit_point.edit_text + "\n"
            client.did_change(
                uri,
                version,
                [
                    {
                        "range": {
                            "start": {"line": insert_line, "character": 0},
                            "end": {"line": insert_line, "character": 0},
                        },
                        "text": new_line,
                    }
                ],
                context={"suite": suite.name, "label": label, "phase": "edit"},
            )
            version += 1

            # Now measure the query after the edit.
            before = len(client.metrics)
            result = _dispatch_benchmark_request(
                client, method, uri,
                edit_point.query_line, edit_point.query_character, context,
            )
            metrics.extend(client.metrics[before:])
            if response_log is not None and not is_warmup:
                _write_response_entry(response_log, context, method, result)

            # Revert the edit to restore original document state.
            client.did_change(
                uri,
                version,
                [
                    {
                        "range": {
                            "start": {"line": insert_line, "character": 0},
                            "end": {"line": insert_line + 1, "character": 0},
                        },
                        "text": "",
                    }
                ],
                context={"suite": suite.name, "label": label, "phase": "revert"},
            )
            version += 1
        except Exception as exc:
            success = False
            error_message = str(exc)
            _emit_progress(progress, f"[{suite.name}] {label} request failed: {error_message}")
            break

    document_versions[uri] = version
    measured_metrics = [metric for metric in metrics if metric.context.get("phase") == "measured" and metric.kind == "request"]
    validation_summary = _validate_benchmark_point_results(method, edit_point.validation, measured_metrics)
    if not validation_summary["passed"]:
        success = False
        error_message = _combine_error_messages(error_message, validation_summary["message"])
    summary = _summarize_metrics(measured_metrics)
    summary["validation"] = validation_summary
    _emit_progress(
        progress,
        f"[{suite.name}] {label} {'ok' if success else 'failed'}"
        + (f": {error_message}" if error_message else ""),
    )
    return BenchmarkPointReport(
        label=label,
        method=method,
        file_path=str(edit_point.file_path),
        line=edit_point.query_line,
        character=edit_point.query_character,
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


def _dispatch_tsp_request(
    client: LspClient,
    method: str,
    file_path: Path,
    uri: str,
    start_line: int,
    start_character: int,
    end_line: int,
    end_character: int,
    snapshot: int,
    context: dict[str, object],
) -> object:
    node = {
        "uri": uri,
        "range": {
            "start": {"line": start_line, "character": start_character},
            "end": {"line": end_line, "character": end_character},
        },
    }
    if method == "typeServer/getComputedType":
        return client.tsp_get_computed_type(node, snapshot, context=context)
    if method == "typeServer/getDeclaredType":
        return client.tsp_get_declared_type(node, snapshot, context=context)
    if method == "typeServer/getExpectedType":
        return client.tsp_get_expected_type(node, snapshot, context=context)
    if method == "typeServer/semanticTokens":
        return _run_tsp_semantic_tokens_request(
            client=client,
            file_path=file_path,
            snapshot=snapshot,
            start_line=start_line,
            start_character=start_character,
            end_line=end_line,
            end_character=end_character,
            context=context,
        )
    raise ValueError(f"Unsupported TSP benchmark method: {method}")


def _run_tsp_semantic_tokens_request(
    *,
    client: LspClient,
    file_path: Path,
    snapshot: int,
    start_line: int,
    start_character: int,
    end_line: int,
    end_character: int,
    context: dict[str, object],
) -> object:
    started_perf = time.perf_counter()
    try:
        result = compute_semantic_tokens(
            client,
            file_path,
            snapshot=snapshot,
            start_line=start_line,
            start_character=start_character,
            end_line=end_line,
            end_character=end_character,
            context=dict(context),
        )
    except Exception as exc:
        client.record_local_request(
            "typeServer/semanticTokens",
            (time.perf_counter() - started_perf) * 1000,
            success=False,
            error={"message": str(exc)},
            context=context,
        )
        raise
    client.record_local_request(
        "typeServer/semanticTokens",
        (time.perf_counter() - started_perf) * 1000,
        result=result,
        context=context,
    )
    return result


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
    for edit_point in suite.edit_points:
        uri = edit_point.file_path.as_uri()
        if uri in seen:
            continue
        seen.add(uri)
        client.did_open(uri, edit_point.file_path.read_text(encoding="utf-8"), context={"suite": suite.name, "phase": "setup"})
        opened.append(uri)
    for point in suite.tsp_points:
        uri = point.file_path.as_uri()
        if uri in seen:
            continue
        seen.add(uri)
        client.did_open(uri, point.file_path.read_text(encoding="utf-8"), context={"suite": suite.name, "phase": "setup"})
        opened.append(uri)
    for edit_point in suite.tsp_edit_points:
        uri = edit_point.file_path.as_uri()
        if uri in seen:
            continue
        seen.add(uri)
        client.did_open(uri, edit_point.file_path.read_text(encoding="utf-8"), context={"suite": suite.name, "phase": "setup"})
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
    text_fields: dict[str, list[str]] = {}
    for metric in result_metrics:
        for key, value in metric.result_summary.items():
            if isinstance(value, bool):
                continue
            if isinstance(value, (int, float)):
                numeric_fields.setdefault(key, []).append(float(value))
                continue
            if isinstance(value, str):
                text_fields.setdefault(key, []).append(value)

    summarized_metrics: dict[str, object] = {
        key: _summarize_numeric_values(values)
        for key, values in sorted(numeric_fields.items())
    }
    summarized_metrics.update(
        {
            key: _summarize_text_values(values)
            for key, values in sorted(text_fields.items())
        }
    )

    return {
        "present_count": present_count,
        "empty_count": empty_count,
        "non_empty_count": non_empty_count,
        "non_empty_rate": None if present_count == 0 else non_empty_count / present_count,
        "metrics": summarized_metrics,
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


def _summarize_text_values(values: Sequence[str]) -> dict[str, object]:
    if not values:
        return {"representative": None, "unique_values": [], "count": 0}
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    representative = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[0][0]
    return {
        "representative": representative,
        "unique_values": sorted(counts),
        "count": len(values),
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
        expected_type_kinds = thresholds.get("expected_type_kinds")
        if isinstance(expected_type_kinds, list) and expected_type_kinds:
            actual_type_kind = result_summary.get("type_kind")
            if actual_type_kind not in expected_type_kinds:
                failures.append(
                    f"iteration {metric.context.get('iteration', '?')}: type_kind={actual_type_kind!r} not in {expected_type_kinds}"
                )
        expected_type_names = thresholds.get("expected_type_names")
        if isinstance(expected_type_names, list) and expected_type_names:
            actual_type_name = result_summary.get("type_name")
            if actual_type_name not in expected_type_names:
                failures.append(
                    f"iteration {metric.context.get('iteration', '?')}: type_name={actual_type_name!r} not in {expected_type_names}"
                )
        require_declaration_node = thresholds.get("require_declaration_node")
        if require_declaration_node is True and not result_summary.get("has_declaration_node"):
            failures.append(
                f"iteration {metric.context.get('iteration', '?')}: missing declaration node"
            )
    message = None if not failures else "Result validation failed: " + "; ".join(failures)
    return {
        "passed": not failures,
        "checked_iterations": checked_metrics,
        "failure_count": len(failures),
        "message": message,
        "rules": thresholds,
    }


def _effective_validation_thresholds(method: str, validation: BenchmarkValidation) -> dict[str, int | bool | list[str] | None]:
    thresholds: dict[str, int | bool | list[str] | None] = {
        "require_non_empty": validation.require_non_empty,
        "min_completion_items": validation.min_completion_items,
        "min_hover_text_chars": validation.min_hover_text_chars,
        "min_symbol_count": validation.min_symbol_count,
        "min_location_count": validation.min_location_count,
        "min_size_chars": validation.min_size_chars,
        "expected_type_kinds": validation.expected_type_kinds,
        "expected_type_names": validation.expected_type_names,
        "require_declaration_node": validation.require_declaration_node,
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
            "typeServer/getComputedType",
            "typeServer/getDeclaredType",
            "typeServer/getExpectedType",
            "typeServer/semanticTokens",
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


def _open_response_log(path: Path | None) -> io.TextIOBase | None:
    if path is None:
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    return open(path, "w", encoding="utf-8")  # noqa: SIM115


def _write_response_entry(
    log: io.TextIOBase,
    context: dict[str, Any],
    method: str,
    result: Any,
) -> None:
    entry = {
        "suite": context.get("suite"),
        "label": context.get("label"),
        "method": method,
        "file_path": context.get("file_path"),
        "line": context.get("line"),
        "character": context.get("character"),
        "iteration": context.get("iteration"),
        "result": result,
    }
    log.write(json.dumps(entry, default=str) + "\n")


def _write_scenario_responses(
    log: io.TextIOBase | None,
    scenario_name: str,
    metrics: Sequence[CallMetric],
) -> None:
    """Write full response bodies for scenario requests.

    Scenario metrics don't carry full results, but do have result_preview.
    We write the preview as a lightweight record so the log is consistent.
    """
    if log is None:
        return
    for metric in metrics:
        if metric.kind != "request" or not metric.success:
            continue
        entry = {
            "scenario": scenario_name,
            "method": metric.method,
            "result_preview": metric.result_preview,
            "result_summary": metric.result_summary,
        }
        log.write(json.dumps(entry, default=str) + "\n")
