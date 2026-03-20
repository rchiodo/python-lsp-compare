from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from .benchmark_suites import discover_benchmark_suites
from .report_csv import write_csv_report
from .report_markdown import write_markdown_report
from .runner import BUILTIN_SCENARIOS, run_benchmarks, run_scenarios, write_report
from .server_configs import default_local_server_config_path, load_server_config_file, load_server_configs, write_summary
from .server_versions import describe_server_version


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m python_lsp_compare")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-scenarios", help="List bundled scenarios.")
    list_parser.set_defaults(func=handle_list_scenarios)

    list_benchmarks_parser = subparsers.add_parser("list-benchmarks", help="List config-driven benchmark suites.")
    list_benchmarks_parser.add_argument("--benchmark-root", type=Path, help=argparse.SUPPRESS)
    list_benchmarks_parser.set_defaults(func=handle_list_benchmarks)

    list_servers_parser = subparsers.add_parser("list-servers", help="List configured LSP servers from the local config file.")
    list_servers_parser.add_argument("--config", type=Path, default=default_local_server_config_path(), help="Path to the local server config JSON.")
    list_servers_parser.set_defaults(func=handle_list_servers)

    render_report_parser = subparsers.add_parser("render-report", help="Render a markdown comparison report from a multi-server summary JSON file.")
    render_report_parser.add_argument("--summary", type=Path, required=True, help="Path to a summary JSON file produced by run-servers or bench-servers.")
    render_report_parser.add_argument("--output", type=Path, help="Write the markdown report to this path. Defaults to the summary path with a .md suffix.")
    render_report_parser.add_argument("--csv-output", type=Path, help="Write the CSV comparison report to this path. Defaults to the summary path with a .csv suffix.")
    render_report_parser.add_argument("--baseline-server", help="Configured server id or display name to use as the comparison baseline.")
    render_report_parser.add_argument("--title", help="Optional markdown title.")
    render_report_parser.set_defaults(func=handle_render_report)

    run_parser = subparsers.add_parser("run", help="Run scenarios against an LSP server.")
    run_parser.add_argument("--server-command", required=True, help="Executable to launch.")
    run_parser.add_argument("--server-arg", action="append", default=[], help="Additional executable argument. Repeatable.")
    run_parser.add_argument("--scenario", action="append", default=[], help="Scenario to run. Repeatable.")
    run_parser.add_argument("--timeout-seconds", type=float, default=10.0, help="Per-request timeout in seconds.")
    run_parser.add_argument("--output", type=Path, help="Write the JSON report to this path.")
    run_parser.set_defaults(func=handle_run)

    run_servers_parser = subparsers.add_parser("run-servers", help="Run one or more configured LSP servers from the local config file.")
    run_servers_parser.add_argument("--config", type=Path, default=default_local_server_config_path(), help="Path to the local server config JSON.")
    run_servers_parser.add_argument("--server", action="append", default=[], help="Configured server id to run. Repeatable.")
    run_servers_parser.add_argument("--scenario", action="append", default=[], help="Scenario to run. Repeatable.")
    run_servers_parser.add_argument("--timeout-seconds", type=float, help="Per-request timeout in seconds.")
    run_servers_parser.add_argument("--output-dir", type=Path, default=Path("results") / "servers", help="Directory for per-server JSON reports.")
    run_servers_parser.add_argument("--summary-output", type=Path, help="Write a JSON summary for the full multi-server run.")
    run_servers_parser.add_argument("--markdown-output", type=Path, help="Write a markdown comparison report for the full multi-server run.")
    run_servers_parser.add_argument("--csv-output", type=Path, help="Write a CSV comparison report for the full multi-server run.")
    run_servers_parser.add_argument("--baseline-server", help="Configured server id or display name to use as the comparison baseline.")
    run_servers_parser.set_defaults(func=handle_run_servers)

    bench_servers_parser = subparsers.add_parser("bench-servers", help="Run benchmark suites across one or more configured LSP servers from the local config file.")
    bench_servers_parser.add_argument("--config", type=Path, default=default_local_server_config_path(), help="Path to the local server config JSON.")
    bench_servers_parser.add_argument("--server", action="append", default=[], help="Configured server id to run. Repeatable.")
    bench_servers_parser.add_argument("--benchmark-root", type=Path, help=argparse.SUPPRESS)
    bench_servers_parser.add_argument("--timeout-seconds", type=float, help="Per-request timeout in seconds.")
    bench_servers_parser.add_argument("--output-dir", type=Path, default=Path("results") / "bench-servers", help="Directory for per-server benchmark reports.")
    bench_servers_parser.add_argument("--summary-output", type=Path, help="Write a JSON summary for the full multi-server benchmark run.")
    bench_servers_parser.add_argument("--markdown-output", type=Path, help="Write a markdown comparison report for the full multi-server benchmark run.")
    bench_servers_parser.add_argument("--csv-output", type=Path, help="Write a CSV comparison report for the full multi-server benchmark run.")
    bench_servers_parser.add_argument("--baseline-server", help="Configured server id or display name to use as the comparison baseline.")
    bench_servers_parser.set_defaults(func=handle_bench_servers)

    run_benchmark_parser = subparsers.add_parser("run-benchmark", help="Run config-driven benchmark suites against an LSP server.")
    run_benchmark_parser.add_argument("--server-command", required=True, help="Executable to launch.")
    run_benchmark_parser.add_argument("--server-arg", action="append", default=[], help="Additional executable argument. Repeatable.")
    run_benchmark_parser.add_argument("--benchmark-root", type=Path, help=argparse.SUPPRESS)
    run_benchmark_parser.add_argument("--timeout-seconds", type=float, default=10.0, help="Per-request timeout in seconds.")
    run_benchmark_parser.add_argument("--output", type=Path, help="Write the JSON report to this path.")
    run_benchmark_parser.set_defaults(func=handle_run_benchmark)
    return parser


def handle_list_scenarios(_: argparse.Namespace) -> int:
    for scenario in BUILTIN_SCENARIOS.values():
        print(f"{scenario.name}: {scenario.description}")
    return 0


def handle_list_benchmarks(args: argparse.Namespace) -> int:
    suites = discover_benchmark_suites(args.benchmark_root)
    for suite in suites.values():
        point_count = sum(len(points) for points in suite.points_by_method.values())
        requirements = suite.requirements_file.name if suite.requirements_file is not None else "none"
        print(f"{suite.name}: {suite.description} ({point_count} points, requirements={requirements})")
    return 0


def handle_list_servers(args: argparse.Namespace) -> int:
    config = load_server_config_file(args.config)
    for server in config.servers:
        status = "enabled" if server.enabled else "disabled"
        baseline_text = ", baseline" if config.baseline_server == server.id or config.baseline_server == server.display_name else ""
        print(f"{server.id}: {server.display_name} ({status}{baseline_text})")
    return 0


def handle_render_report(args: argparse.Namespace) -> int:
    output_path = args.output or args.summary.with_suffix(".md")
    csv_path = args.csv_output or args.summary.with_suffix(".csv")
    write_markdown_report(args.summary, output_path, title=args.title, baseline_server_id=args.baseline_server)
    write_csv_report(args.summary, csv_path, baseline_server_id=args.baseline_server)
    latest_results_path = _latest_results_path(args.summary)
    latest_results_path.write_text(output_path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Wrote markdown report to {output_path}")
    print(f"Wrote CSV report to {csv_path}")
    print(f"Wrote latest results to {latest_results_path}")
    return 0


def handle_run(args: argparse.Namespace) -> int:
    command = [args.server_command, *args.server_arg]
    requested = args.scenario or list(BUILTIN_SCENARIOS.keys())
    report = run_scenarios(command=command, scenario_names=requested, timeout_seconds=args.timeout_seconds)
    output_path = args.output or _default_output_path(command[0])
    write_report(report, output_path)
    print(f"Wrote report to {output_path}")
    for scenario in report.scenario_reports:
        status = "ok" if scenario.success else "failed"
        print(f"{scenario.name}: {status} ({scenario.total_duration_ms:.2f} ms, {len(scenario.metrics)} calls)")
        if scenario.error_message:
            print(f"  error: {scenario.error_message}")
    return 0 if all(item.success for item in report.scenario_reports) else 1


def handle_run_servers(args: argparse.Namespace) -> int:
    configured_servers, requested_ids = _select_configured_servers(args.config, args.server)
    baseline_server = _resolve_baseline_server(args.config, args.baseline_server)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    run_stamp = _timestamp()
    summary_path = args.summary_output or output_dir / f"summary-{run_stamp}.json"

    server_summaries: list[dict[str, object]] = []
    overall_success = True
    for server in configured_servers:
        version_info = describe_server_version(server)
        requested_scenarios = args.scenario or list(BUILTIN_SCENARIOS.keys())
        timeout_seconds = args.timeout_seconds or 10.0
        report = run_scenarios(
            command=server.launch_command,
            scenario_names=requested_scenarios,
            timeout_seconds=timeout_seconds,
        )
        output_path = output_dir / f"{server.id}-{run_stamp}.json"
        write_report(report, output_path)
        success = all(item.success for item in report.scenario_reports)
        overall_success = overall_success and success
        print(f"{server.id}: {'ok' if success else 'failed'} -> {output_path}")
        for scenario in report.scenario_reports:
            status = "ok" if scenario.success else "failed"
            print(f"  {scenario.name}: {status} ({scenario.total_duration_ms:.2f} ms)")
            if scenario.error_message:
                print(f"    error: {scenario.error_message}")
        server_summaries.append(
            {
                "id": server.id,
                "display_name": server.display_name,
                "output_path": str(output_path),
                "success": success,
                "scenario_count": len(report.scenario_reports),
                "command": server.launch_command,
                "source_path": server.source_path,
                "version": version_info,
                "requested_scenarios": requested_scenarios,
                "timeout_seconds": timeout_seconds,
            }
        )

    write_summary(
        summary_path,
        {
            "config_path": str(args.config),
            "requested_servers": sorted(requested_ids) if requested_ids else [server.id for server in configured_servers],
            "requested_scenarios": args.scenario,
            "baseline_server": baseline_server,
            "generated_at": run_stamp,
            "servers": server_summaries,
        },
    )
    markdown_path = args.markdown_output or summary_path.with_suffix(".md")
    csv_path = args.csv_output or summary_path.with_suffix(".csv")
    write_markdown_report(summary_path, markdown_path, baseline_server_id=baseline_server)
    write_csv_report(summary_path, csv_path, baseline_server_id=baseline_server)
    latest_results_path = _latest_results_path(summary_path)
    latest_results_path.write_text(markdown_path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Wrote summary to {summary_path}")
    print(f"Wrote markdown report to {markdown_path}")
    print(f"Wrote CSV report to {csv_path}")
    print(f"Wrote latest results to {latest_results_path}")
    return 0 if overall_success else 1


def handle_bench_servers(args: argparse.Namespace) -> int:
    configured_servers, requested_ids = _select_configured_servers(args.config, args.server)
    baseline_server = _resolve_baseline_server(args.config, args.baseline_server)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    run_stamp = _timestamp()
    summary_path = args.summary_output or output_dir / f"summary-{run_stamp}.json"

    server_summaries: list[dict[str, object]] = []
    overall_success = True
    requested_benchmarks: list[str] | None = None
    for server in configured_servers:
        version_info = describe_server_version(server)
        timeout_seconds = args.timeout_seconds or 10.0
        benchmark_root = args.benchmark_root
        install_requirements = True
        environment_mode = "isolated"
        environment_root = None
        python_executable = None

        report = run_benchmarks(
            command=server.benchmark_launch_command,
            benchmark_names=None,
            timeout_seconds=timeout_seconds,
            benchmark_root=benchmark_root,
            install_requirements=install_requirements,
            python_executable=python_executable,
            environment_mode=environment_mode,
            environment_root=environment_root,
            progress=lambda message, server_id=server.id: print(f"{server_id}: {message}"),
        )
        requested_benchmarks = report.requested_benchmarks
        output_path = output_dir / f"{server.id}-{run_stamp}.json"
        write_report(report, output_path)
        success = all(item.success for item in report.benchmark_reports)
        overall_success = overall_success and success
        print(f"{server.id}: {'ok' if success else 'failed'} -> {output_path}")
        for benchmark in report.benchmark_reports:
            status = "ok" if benchmark.success else "failed"
            print(f"  {benchmark.name}: {status} ({benchmark.total_duration_ms:.2f} ms, {len(benchmark.points)} points)")
            if benchmark.error_message:
                print(f"    error: {benchmark.error_message}")
        server_summaries.append(
            {
                "id": server.id,
                "display_name": server.display_name,
                "output_path": str(output_path),
                "success": success,
                "benchmark_count": len(report.benchmark_reports),
                "command": server.benchmark_launch_command,
                "source_path": server.source_path,
                "version": version_info,
                "requested_benchmarks": report.requested_benchmarks,
                "benchmark_root": None if benchmark_root is None else str(benchmark_root),
                "timeout_seconds": timeout_seconds,
                "install_requirements": install_requirements,
                "environment_mode": environment_mode,
            }
        )

    write_summary(
        summary_path,
        {
            "config_path": str(args.config),
            "requested_servers": sorted(requested_ids) if requested_ids else [server.id for server in configured_servers],
            "requested_benchmarks": requested_benchmarks,
            "baseline_server": baseline_server,
            "generated_at": run_stamp,
            "servers": server_summaries,
        },
    )
    markdown_path = args.markdown_output or summary_path.with_suffix(".md")
    csv_path = args.csv_output or summary_path.with_suffix(".csv")
    write_markdown_report(summary_path, markdown_path, baseline_server_id=baseline_server)
    write_csv_report(summary_path, csv_path, baseline_server_id=baseline_server)
    latest_results_path = _latest_results_path(summary_path)
    latest_results_path.write_text(markdown_path.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"Wrote summary to {summary_path}")
    print(f"Wrote markdown report to {markdown_path}")
    print(f"Wrote CSV report to {csv_path}")
    print(f"Wrote latest results to {latest_results_path}")
    return 0 if overall_success else 1


def handle_run_benchmark(args: argparse.Namespace) -> int:
    command = [args.server_command, *args.server_arg]
    report = run_benchmarks(
        command=command,
        benchmark_names=None,
        timeout_seconds=args.timeout_seconds,
        benchmark_root=args.benchmark_root,
        install_requirements=True,
        python_executable=None,
        environment_mode="isolated",
        environment_root=None,
        progress=print,
    )
    output_path = args.output or _default_output_path(f"{command[0]}-benchmarks")
    write_report(report, output_path)
    print(f"Wrote report to {output_path}")
    for benchmark in report.benchmark_reports:
        status = "ok" if benchmark.success else "failed"
        print(f"{benchmark.name}: {status} ({benchmark.total_duration_ms:.2f} ms, {len(benchmark.points)} points, env={benchmark.environment_mode})")
        if benchmark.error_message:
            print(f"  error: {benchmark.error_message}")
        if benchmark.environment_path:
            print(f"  environment: {benchmark.environment_path}")
        for point in benchmark.points:
            point_status = "ok" if point.success else "failed"
            mean_ms = point.summary.get("mean_ms")
            mean_text = f"{mean_ms:.2f} ms" if isinstance(mean_ms, (float, int)) else "n/a"
            print(f"  {point.label}: {point_status} ({point.measured_iterations} measured, mean={mean_text})")
            if point.error_message:
                print(f"    error: {point.error_message}")
    return 0 if all(item.success for item in report.benchmark_reports) else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def _default_output_path(executable_name: str) -> Path:
    return Path("results") / f"{executable_name}-{_timestamp()}.json"


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _select_configured_servers(config_path: Path, requested_server_ids: list[str]) -> tuple[list, set[str]]:
    configured_servers = [server for server in load_server_configs(config_path) if server.enabled]
    requested_ids = set(requested_server_ids)
    if requested_ids:
        configured_servers = [server for server in configured_servers if server.id in requested_ids]
        missing = requested_ids.difference(server.id for server in configured_servers)
        if missing:
            raise ValueError(f"Unknown configured servers: {', '.join(sorted(missing))}")
    return configured_servers, requested_ids


def _path_or_none(value: str | None) -> Path | None:
    if value is None:
        return None
    return Path(value)


def _resolve_baseline_server(config_path: Path, cli_value: str | None) -> str | None:
    if cli_value:
        return cli_value
    return load_server_config_file(config_path).baseline_server


def _latest_results_path(summary_path: Path) -> Path:
    for parent in summary_path.parents:
        if parent.name == "results":
            return parent.parent / "latest-results.md"
    return summary_path.parent / "latest-results.md"
