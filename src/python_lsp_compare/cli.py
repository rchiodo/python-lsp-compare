from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

from .benchmark_suites import discover_benchmark_suites
from .report_csv import write_csv_report
from .report_markdown import render_markdown_report, write_markdown_report
from .runner import BUILTIN_SCENARIOS, run_benchmarks, run_scenarios, write_report
from .server_configs import load_server_config_file, load_server_configs, write_summary
from .server_download import ALL_SERVER_SPECS, ALL_PYPI_SERVER_SPECS, download_all_servers
from .server_versions import describe_server_version


DEFAULT_REQUEST_TIMEOUT_SECONDS = 10.0
DEFAULT_BENCHMARK_TIMEOUT_SECONDS = 300.0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m python_lsp_compare")
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-scenarios", help="List bundled scenarios.")
    list_parser.set_defaults(func=handle_list_scenarios)

    list_benchmarks_parser = subparsers.add_parser("list-benchmarks", help="List config-driven benchmark suites.")
    list_benchmarks_parser.add_argument("--benchmark-root", type=Path, help=argparse.SUPPRESS)
    list_benchmarks_parser.set_defaults(func=handle_list_benchmarks)

    list_servers_parser = subparsers.add_parser("list-servers", help="List configured LSP servers. Downloads from GitHub releases by default, or reads from a config file if --config is given.")
    list_servers_parser.add_argument("--config", type=Path, default=None, help="Path to a local server config JSON. When omitted, servers are downloaded from GitHub releases.")
    list_servers_parser.set_defaults(func=handle_list_servers)

    render_report_parser = subparsers.add_parser("render-report", help="Render a markdown comparison report from a multi-server summary JSON file.")
    render_report_parser.add_argument("--summary", type=Path, required=True, help="Path to a summary JSON file produced by run-servers or bench-servers.")
    render_report_parser.add_argument("--output", type=Path, help="Write the markdown report to this path. Defaults to the summary path with a .md suffix.")
    render_report_parser.add_argument("--csv-output", type=Path, help="Write the CSV comparison report to this path. Defaults to the summary path with a .csv suffix.")
    render_report_parser.add_argument("--baseline-server", help="Configured server id or display name to use as the comparison baseline.")
    render_report_parser.add_argument("--title", help="Optional markdown title.")
    render_report_parser.set_defaults(func=handle_render_report)

    download_parser = subparsers.add_parser("download-servers", help="Download LSP server binaries from GitHub releases.")
    download_parser.add_argument("--server", action="append", default=[], help="Server id to download (pyright, ty, pyrefly). Repeatable. Downloads all if omitted.")
    download_parser.add_argument("--force", action="store_true", help="Re-download even if already cached.")
    download_parser.set_defaults(func=handle_download_servers)

    run_parser = subparsers.add_parser("run", help="Run scenarios against an LSP server.")
    run_parser.add_argument("--server-command", required=True, help="Executable to launch.")
    run_parser.add_argument("--server-arg", action="append", default=[], help="Additional executable argument. Repeatable.")
    run_parser.add_argument("--scenario", action="append", default=[], help="Scenario to run. Repeatable.")
    run_parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_REQUEST_TIMEOUT_SECONDS, help="Per-request timeout in seconds.")
    run_parser.add_argument("--output", type=Path, help="Write the JSON report to this path.")
    run_parser.set_defaults(func=handle_run)

    run_servers_parser = subparsers.add_parser("run-servers", help="Run one or more LSP servers. Downloads from GitHub releases by default, or reads from a config file if --config is given.")
    run_servers_parser.add_argument("--config", type=Path, default=None, help="Path to a local server config JSON. When omitted, servers are downloaded from GitHub releases.")
    run_servers_parser.add_argument("--server", action="append", default=[], help="Server id to run. Repeatable.")
    run_servers_parser.add_argument("--scenario", action="append", default=[], help="Scenario to run. Repeatable.")
    run_servers_parser.add_argument("--timeout-seconds", type=float, help=f"Per-request timeout in seconds. Defaults to {DEFAULT_REQUEST_TIMEOUT_SECONDS:.0f}.")
    run_servers_parser.add_argument("--output-dir", type=Path, default=Path("results") / "servers", help="Directory for per-server JSON reports.")
    run_servers_parser.add_argument("--summary-output", type=Path, help="Write a JSON summary for the full multi-server run.")
    run_servers_parser.add_argument("--markdown-output", type=Path, help="Write a markdown comparison report for the full multi-server run.")
    run_servers_parser.add_argument("--csv-output", type=Path, help="Write a CSV comparison report for the full multi-server run.")
    run_servers_parser.add_argument("--baseline-server", help="Configured server id or display name to use as the comparison baseline.")
    run_servers_parser.set_defaults(func=handle_run_servers)

    bench_servers_parser = subparsers.add_parser("bench-servers", help="Run benchmark suites across one or more LSP servers. Downloads from GitHub releases by default, or reads from a config file if --config is given.")
    bench_servers_parser.add_argument("--config", type=Path, default=None, help="Path to a local server config JSON. When omitted, servers are downloaded from GitHub releases.")
    bench_servers_parser.add_argument("--server", action="append", default=[], help="Server id to run. Repeatable.")
    bench_servers_parser.add_argument("--benchmark-root", type=Path, help=argparse.SUPPRESS)
    bench_servers_parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_BENCHMARK_TIMEOUT_SECONDS, help=f"Per-request timeout in seconds. Defaults to {DEFAULT_BENCHMARK_TIMEOUT_SECONDS:.0f}.")
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
    run_benchmark_parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_BENCHMARK_TIMEOUT_SECONDS, help=f"Per-request timeout in seconds. Defaults to {DEFAULT_BENCHMARK_TIMEOUT_SECONDS:.0f}.")
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
    if args.config is not None:
        config = load_server_config_file(args.config)
        for server in config.servers:
            status = "enabled" if server.enabled else "disabled"
            baseline_text = ", baseline" if config.baseline_server == server.id or config.baseline_server == server.display_name else ""
            print(f"{server.id}: {server.display_name} ({status}{baseline_text})")
    else:
        servers = download_all_servers()
        for server in servers:
            print(f"{server.id}: {server.display_name} (enabled)")
    return 0


def handle_render_report(args: argparse.Namespace) -> int:
    output_path = args.output or args.summary.with_suffix(".md")
    csv_path = args.csv_output or args.summary.with_suffix(".csv")
    write_markdown_report(args.summary, output_path, title=args.title, baseline_server_id=args.baseline_server)
    write_csv_report(args.summary, csv_path, baseline_server_id=args.baseline_server)
    # For render-report, extract the run stamp from the summary filename
    stem = args.summary.stem
    stamp = stem.split("-", 1)[1] if "-" in stem else stem
    _update_latest_results(args.summary.parent, stamp, output_path, args.summary, baseline_server_id=args.baseline_server, title=args.title)
    print(f"Wrote markdown report to {output_path}")
    print(f"Wrote CSV report to {csv_path}")
    return 0


def handle_download_servers(args: argparse.Namespace) -> int:
    server_ids = args.server or None
    known_ids = {s.id for s in ALL_SERVER_SPECS} | {s.id for s in ALL_PYPI_SERVER_SPECS}
    if server_ids:
        unknown = set(server_ids) - known_ids
        if unknown:
            print(f"Unknown server ids: {', '.join(sorted(unknown))}")
            print(f"Available: {', '.join(sorted(known_ids))}")
            return 1

    servers = download_all_servers(force=args.force, server_ids=server_ids)
    if not servers:
        print("No servers were downloaded successfully.")
        return 1

    print(f"\nDownloaded {len(servers)} server(s):")
    for s in servers:
        print(f"  {s.id}: {s.display_name}")
        print(f"    command: {' '.join(s.launch_command)}")

    return 0


def handle_run(args: argparse.Namespace) -> int:
    command = [args.server_command, *args.server_arg]
    requested = args.scenario or list(BUILTIN_SCENARIOS.keys())
    output_path = args.output or _default_output_path(command[0])
    response_log_path = output_path.with_stem(output_path.stem + "-responses").with_suffix(".jsonl")
    report = run_scenarios(command=command, scenario_names=requested, timeout_seconds=args.timeout_seconds, response_log_path=response_log_path)
    write_report(report, output_path)
    print(f"Wrote report to {output_path}")
    print(f"Wrote response log to {response_log_path}")
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
    for server in configured_servers:
        version_info = describe_server_version(server)
        requested_scenarios = args.scenario or list(BUILTIN_SCENARIOS.keys())
        timeout_seconds = args.timeout_seconds or DEFAULT_REQUEST_TIMEOUT_SECONDS
        response_log_path = output_dir / f"{server.id}-{run_stamp}-responses.jsonl"
        report = run_scenarios(
            command=server.launch_command,
            scenario_names=requested_scenarios,
            timeout_seconds=timeout_seconds,
            response_log_path=response_log_path,
        )
        output_path = output_dir / f"{server.id}-{run_stamp}.json"
        write_report(report, output_path)
        success = all(item.success for item in report.scenario_reports)
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
                "notes": server.notes,
            }
        )

    write_summary(
        summary_path,
        {
            "config_path": str(args.config) if args.config else "github-releases",
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
    _update_latest_results(output_dir, run_stamp, markdown_path, summary_path, baseline_server_id=baseline_server)
    print(f"Wrote summary to {summary_path}")
    print(f"Wrote markdown report to {markdown_path}")
    print(f"Wrote CSV report to {csv_path}")
    return 0


def handle_bench_servers(args: argparse.Namespace) -> int:
    configured_servers, requested_ids = _select_configured_servers(args.config, args.server)
    baseline_server = _resolve_baseline_server(args.config, args.baseline_server)
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    run_stamp = _timestamp()
    summary_path = args.summary_output or output_dir / f"summary-{run_stamp}.json"

    server_summaries: list[dict[str, object]] = []
    requested_benchmarks: list[str] | None = None
    for server in configured_servers:
        print(f"=== Starting server: {server.id} ({server.display_name}) ===")
        print(f"  command: {server.command}")
        print(f"  args: {server.args}")
        print(f"  benchmark_launch_command: {server.benchmark_launch_command}")
        version_info = describe_server_version(server)
        print(f"  version: {version_info.get('label', 'unknown')}")
        timeout_seconds = args.timeout_seconds or DEFAULT_BENCHMARK_TIMEOUT_SECONDS
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
            response_log_path=output_dir / f"{server.id}-{run_stamp}-responses.jsonl",
        )
        requested_benchmarks = report.requested_benchmarks
        output_path = output_dir / f"{server.id}-{run_stamp}.json"
        write_report(report, output_path)
        success = all(item.success for item in report.benchmark_reports)
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
                "notes": server.notes,
            }
        )

    write_summary(
        summary_path,
        {
            "config_path": str(args.config) if args.config else "github-releases",
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
    _update_latest_results(output_dir, run_stamp, markdown_path, summary_path, baseline_server_id=baseline_server)
    print(f"Wrote summary to {summary_path}")
    print(f"Wrote markdown report to {markdown_path}")
    print(f"Wrote CSV report to {csv_path}")
    return 0


def handle_run_benchmark(args: argparse.Namespace) -> int:
    command = [args.server_command, *args.server_arg]
    output_path = args.output or _default_output_path(f"{command[0]}-benchmarks")
    response_log_path = output_path.with_stem(output_path.stem + "-responses").with_suffix(".jsonl")
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
        response_log_path=response_log_path,
    )
    write_report(report, output_path)
    print(f"Wrote report to {output_path}")
    print(f"Wrote response log to {response_log_path}")
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


def _select_configured_servers(config_path: Path | None, requested_server_ids: list[str]) -> tuple[list, set[str]]:
    if config_path is not None:
        configured_servers = [server for server in load_server_configs(config_path) if server.enabled]
    else:
        configured_servers = download_all_servers(server_ids=requested_server_ids or None)
    requested_ids = set(requested_server_ids)
    if requested_ids:
        configured_servers = [server for server in configured_servers if server.id in requested_ids]
        missing = requested_ids.difference(server.id for server in configured_servers)
        if missing:
            raise ValueError(f"Unknown servers: {', '.join(sorted(missing))}")
    return configured_servers, requested_ids


def _path_or_none(value: str | None) -> Path | None:
    if value is None:
        return None
    return Path(value)


def _resolve_baseline_server(config_path: Path | None, cli_value: str | None) -> str | None:
    if cli_value:
        return cli_value
    if config_path is not None:
        return load_server_config_file(config_path).baseline_server
    return "pyright"


def _latest_results_path(summary_path: Path) -> Path:
    for parent in summary_path.parents:
        if parent.name == "results":
            return parent.parent / "latest-results.md"
    return summary_path.parent / "latest-results.md"


def _latest_results_dir(summary_path: Path) -> Path:
    for parent in summary_path.parents:
        if parent.name == "results":
            return parent.parent / "latest-results"
    return summary_path.parent / "latest-results"


def _update_latest_results(
    output_dir: Path,
    run_stamp: str,
    markdown_path: Path,
    summary_path: Path,
    baseline_server_id: str | None = None,
    title: str | None = None,
) -> None:
    """Copy all files from the latest run into a latest-results/ folder."""
    latest_md = _latest_results_path(summary_path)
    latest_dir = _latest_results_dir(summary_path)

    # Clear and recreate
    if latest_dir.exists():
        shutil.rmtree(latest_dir)
    latest_dir.mkdir(parents=True, exist_ok=True)

    # Copy all files from this run (matching the timestamp)
    for path in sorted(output_dir.iterdir()):
        if path.is_file() and run_stamp in path.name:
            shutil.copy2(path, latest_dir / path.name)

    # Re-render the markdown with links to the data files in latest-results/
    linked_md = render_markdown_report(
        summary_path,
        title=title,
        baseline_server_id=baseline_server_id,
        data_link_prefix=latest_dir.name,
    )
    latest_md.write_text(linked_md, encoding="utf-8")
    print(f"Wrote latest results to {latest_dir} and {latest_md}")
