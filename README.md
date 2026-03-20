# python-lsp-compare

`python-lsp-compare` is a small benchmark and regression harness for Python Language Server Protocol implementations.

This repository provides a vendor-neutral comparison harness and test corpus for
Python language servers. It is intended to surface behavioral and performance
differences across implementations and does not define a specification or
normative behavior.

It focuses on four things:

1. Running LSP servers over stdio with raw JSON-RPC messages.
2. Executing repeatable scenarios against those servers.
3. Capturing request/notification timings, payload sizes, and results.
4. Producing machine-readable reports that are easy to diff across servers.

Benchmark suites are package-oriented, not just API-oriented. That means testing LSP behavior against realistic dependency surfaces like SQLAlchemy-heavy code, web frameworks, and data-science imports.

Benchmark runs are intentionally deterministic: each suite creates or reuses its own `.venv`, installs the suite requirements there, writes temporary workspace configuration for language servers, and then runs every selected server against that same suite-local environment.

## Features

- Pure Python implementation of LSP framing over stdio.
- Built-in Python scenarios for hover, completion, and document symbols.
- Config-driven benchmark suites under `benchmarks/` with package-specific fixtures and `requirements.txt` files.
- Per-call metrics including latency, bytes sent, bytes received, success, and errors.
- Aggregate stats for benchmark points including mean, median, min, max, and p95.
- JSON report output for later aggregation.
- MIT licensed from the start.

## Quick Start

Create a virtual environment, install the package in editable mode, and point it at an LSP server command.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
python -m python_lsp_compare list-scenarios
python -m python_lsp_compare list-benchmarks
python -m python_lsp_compare list-servers
python -m python_lsp_compare run --server-command pylsp --scenario hover --scenario completion
python -m python_lsp_compare run --server-command pyright-langserver --server-arg=--stdio
python -m python_lsp_compare run-benchmark --server-command pyright-langserver --server-arg=--stdio
python -m python_lsp_compare run-servers --scenario hover --scenario completion
python -m python_lsp_compare bench-servers
python -m python_lsp_compare render-report --summary results/bench-servers/summary-20260319T000000Z.json --baseline-server pylance
```

The default report path is created under `results/`.

## CLI

List the bundled scenarios:

```powershell
python -m python_lsp_compare list-scenarios
```

List the benchmark suites:

```powershell
python -m python_lsp_compare list-benchmarks
```

List the locally configured servers:

```powershell
python -m python_lsp_compare list-servers
```

Run one or more scenarios:

```powershell
python -m python_lsp_compare run \
  --server-command pyright-langserver \
  --server-arg=--stdio \
  --scenario hover \
  --scenario completion \
  --output results/pyright.json
```

Run one or more package-oriented benchmark suites:

```powershell
python -m python_lsp_compare run-benchmark \
  --server-command pyright-langserver \
  --server-arg=--stdio \
  --output results/pyright-benchmarks.json
```

Run the same scenarios across all locally configured servers:

```powershell
python -m python_lsp_compare run-servers \
  --scenario hover \
  --scenario completion \
  --output-dir results/servers
```

Run benchmark suites across all locally configured servers:

```powershell
python -m python_lsp_compare bench-servers \
  --baseline-server pylance \
  --output-dir results/bench-servers
```

Render or re-render a markdown comparison report from an existing multi-server summary JSON file:

```powershell
python -m python_lsp_compare render-report \
  --summary results/bench-servers/summary-20260319T000000Z.json \
  --baseline-server pylance \
  --output results/bench-servers/comparison.md
```

Arguments:

- `--server-command`: executable to launch.
- `--server-arg`: additional argument, repeatable.
- `--scenario`: scenario name, repeatable. If omitted, all scenarios run.
- `--timeout-seconds`: per-request timeout.
- `--output`: JSON report path.

Configured server arguments:

- `--config`: path to the local server config file. Defaults to `.python-lsp-compare/lsp_servers.json`.
- `--server`: configured server id to run, repeatable. If omitted, all enabled servers run.
- `--output-dir`: directory for per-server JSON reports and the summary JSON file.
- `--summary-output`: optional path for the combined multi-server summary file.
- `--markdown-output`: optional path for the combined markdown comparison report. If omitted, a markdown report is written next to the summary JSON.
- `--csv-output`: optional path for the combined CSV comparison report. If omitted, a CSV report is written next to the summary JSON.
- `--baseline-server`: configured server id or display name to use as the comparison baseline in markdown and CSV reports.

Configured benchmark runner arguments:

- `--timeout-seconds`: override the per-request timeout for all benchmark calls.
- `--output-dir`: directory for per-server JSON reports and the combined summary/report outputs.
- `--summary-output`, `--markdown-output`, `--csv-output`: override report destinations.
- `--baseline-server`: choose the comparison baseline for the rendered reports.

Benchmark arguments:

- `run-benchmark` runs all bundled suites under `benchmarks/`.
- `bench-servers` runs that same full bundled suite set for each selected server.

Benchmark runs always use an isolated suite environment and install each suite's declared requirements before launching the server. That keeps runs reproducible and avoids depending on whatever happens to be installed in the caller's active environment.

## Report Shape

Reports include:

- Server command and run timestamp.
- One entry per scenario.
- One entry per benchmark suite when using `run-benchmark`.
- One summary JSON file plus one report per server when using `run-servers`.
- One markdown comparison report when using `run-servers` or `bench-servers`.
- One CSV comparison report when using `run-servers` or `bench-servers`.
- One metric per LSP call, including initialize/shutdown.
- Scenario success/failure and any captured error message.
- Aggregate duration summaries for each benchmark point and method.
- Structured result summaries per request, including whether the result was empty and method-specific counts such as completion items, symbol count, hover text length, or location count.
- Benchmark-point validation results, including whether semantic result checks passed and how many measured iterations failed validation.

The markdown comparison report is intended for check-ins, PRs, or ongoing benchmark notes. It shows both total wall-clock time and average request time, and highlights semantic result differences for matching benchmark points, such as hover length, completion count, and definition count relative to the baseline server.

The CSV comparison report flattens the same run into spreadsheet-friendly rows with server id, suite or scenario name, point label, preferred result metric, delta versus the chosen baseline server, and validation status.

## Local Server Config

Machine-specific server paths are kept out of the tracked repository by default.

- Copy `configs/lsp_servers.example.json` to `.python-lsp-compare/lsp_servers.json`.
- Fill in the local executable paths for each server.
- The `.python-lsp-compare/` directory is ignored by Git.

The local config is intentionally minimal: it identifies where each server executable or launcher lives on the current machine. Scenario selection, benchmark selection, benchmark environment creation, and package installation are handled by the runner so the same suite runs the same way for everyone.

## Setting Up Servers

`run-servers`, `bench-servers`, and `list-servers` all read from `.python-lsp-compare/lsp_servers.json` by default. The easiest way to get started is:

1. Copy `configs/lsp_servers.example.json` to `.python-lsp-compare/lsp_servers.json`.
2. Replace each placeholder path with the local path to that server on your machine.
3. Keep only the servers you actually want to run, or set `"enabled": false` on entries you want to leave in the file but skip.
4. Run `python -m python_lsp_compare list-servers` to confirm the config is valid and the servers are visible.

Example config shape:

```json
{
  "version": 1,
  "baselineServer": "pylance",
  "servers": [
    {
      "id": "pylance",
      "displayName": "Pylance",
      "enabled": true,
      "sourcePath": "C:/path/to/pylance-server/dist/server.js",
      "launch": {
        "command": "C:/Program Files/nodejs/node.exe",
        "args": [
          "../tools/pylance_stdio_launcher.cjs",
          "--server-path",
          "C:/path/to/pylance-server/dist/server.js"
        ]
      }
    },
    {
      "id": "ty",
      "displayName": "Ty",
      "enabled": true,
      "sourcePath": "C:/path/to/ty.exe",
      "launch": {
        "command": "C:/path/to/ty.exe",
        "args": ["server"]
      }
    },
    {
      "id": "pyrefly",
      "displayName": "Pyrefly",
      "enabled": true,
      "sourcePath": "C:/path/to/pyrefly.exe",
      "launch": {
        "command": "C:/path/to/pyrefly.exe",
        "args": [
          "lsp",
          "--indexing-mode",
          "lazy-blocking",
          "--build-system-blocking"
        ]
      }
    }
  ]
}
```

Linux/macOS example config shape:

```json
{
  "version": 1,
  "baselineServer": "pylance",
  "servers": [
    {
      "id": "pylance",
      "displayName": "Pylance",
      "enabled": true,
      "sourcePath": "/home/you/src/pylance-server/dist/server.js",
      "launch": {
        "command": "node",
        "args": [
          "../tools/pylance_stdio_launcher.cjs",
          "--server-path",
          "/home/you/src/pylance-server/dist/server.js"
        ]
      }
    },
    {
      "id": "ty",
      "displayName": "Ty",
      "enabled": true,
      "sourcePath": "/home/you/bin/ty",
      "launch": {
        "command": "/home/you/bin/ty",
        "args": ["server"]
      }
    },
    {
      "id": "pyrefly",
      "displayName": "Pyrefly",
      "enabled": true,
      "sourcePath": "/home/you/bin/pyrefly",
      "launch": {
        "command": "/home/you/bin/pyrefly",
        "args": [
          "lsp",
          "--indexing-mode",
          "lazy-blocking",
          "--build-system-blocking"
        ]
      }
    }
  ]
}
```

Notes on the fields:

- `id`: stable identifier used by `--server` and `--baseline-server`.
- `displayName`: friendly label shown in reports.
- `enabled`: optional; defaults to enabled if omitted.
- `sourcePath`: optional but useful in generated reports so you can see which build or binary was measured.
- `launch.command`: the actual executable to start.
- `launch.args`: extra arguments passed to that executable. Relative paths inside `args` are resolved relative to the config file directory.
- On Linux and macOS, `launch.command` may be either an absolute path such as `/home/you/bin/ty` or a command on `PATH` such as `node`.
- `launch.benchmarkArgs`: optional advanced field for servers that need extra arguments only during `bench-servers`. Most setups should omit it.

### Pylance

Pylance is a Node-hosted server, so you need both:

- a local `node.exe`
- the built `server.js` for the Pylance server

On Linux or macOS, replace `node.exe` with either `node` or the absolute path to your Node installation.

This repo includes [tools/pylance_stdio_launcher.cjs](tools/pylance_stdio_launcher.cjs), which wraps the Node server so it behaves like a stdio LSP process for the benchmark harness. In the config:

- `launch.command` should point to `node.exe`
- `launch.args` should point to `../tools/pylance_stdio_launcher.cjs`
- `--server-path` should point to the actual Pylance `dist/server.js`

### Ty

Ty is configured as a native executable. Point both `sourcePath` and `launch.command` at the built `ty.exe`, and use:

```json
"args": ["server"]
```

because Ty exposes LSP mode through the `server` subcommand.

### Pyrefly

Pyrefly is also configured as a native executable. Point both `sourcePath` and `launch.command` at `pyrefly.exe`, and use:

```json
"args": [
  "lsp",
  "--indexing-mode",
  "lazy-blocking",
  "--build-system-blocking"
]
```

Those flags match the settings used in the benchmark runs documented in this repository.

## Test Configs

The automated tests do not load your checked-in example config or your personal local config. The test suite builds temporary config JSON files inline inside the test cases and passes them with `--config`, which is why tests continue to pass even if the example file and your local file drift apart.

In practice:

- [tests/test_server_configs.py](tests/test_server_configs.py) creates temporary config files and verifies the loader and CLI behavior directly.
- [tests/test_cli.py](tests/test_cli.py) and [tests/test_reporting.py](tests/test_reporting.py) also create temporary config files for isolated test runs.

That means the example config is documentation, not a fixture that the test suite executes verbatim.

### Verifying Setup

After editing the config, use these commands to verify everything is wired correctly:

```powershell
python -m python_lsp_compare list-servers
python -m python_lsp_compare run-servers --scenario hover
python -m python_lsp_compare bench-servers --server pylance --server ty --server pyrefly
```

If `list-servers` shows the expected ids and `run-servers` can complete a small scenario run, the same config is ready for `bench-servers`.

On Linux or macOS, the same verification commands apply:

```bash
python -m python_lsp_compare list-servers
python -m python_lsp_compare run-servers --scenario hover
python -m python_lsp_compare bench-servers --server pylance --server ty --server pyrefly
```

## Benchmark Suites

Each suite folder follows the same internal structure:

- `config.json` describes request points and iteration counts.
- `requirements.txt` describes the dependency surface to benchmark.
- `src/` contains the Python files to open and query.
- `.venv/` is created automatically per suite and reused across servers.

Each benchmark point can also define an optional `validation` block in `config.json` to enforce semantic expectations on measured results:

```json
{
  "label": "query completion",
  "file": "src/models.py",
  "line": 16,
  "character": 22,
  "validation": {
    "minCompletionItems": 1,
    "requireNonEmpty": true
  }
}
```

Supported validation keys:

- `requireNonEmpty`
- `minCompletionItems`
- `minHoverTextChars`
- `minSymbolCount`
- `minLocationCount`
- `minSizeChars`

If a measured iteration fails these checks, the benchmark point is marked failed and the report records the validation failure details.

Bundled examples:

- `benchmarks/sqlalchemy`
- `benchmarks/web`
- `benchmarks/data_science`
- `benchmarks/django`
- `benchmarks/pandas`
- `benchmarks/transformers`

## Isolated Environments

Benchmark suites run inside per-suite virtual environments. This keeps third-party dependencies isolated from the interpreter used for development or testing and ensures every selected server sees the same package set.

Example:

```powershell
python -m python_lsp_compare run-benchmark \
  --server-command python \
  --server-arg=-m \
  --server-arg=pylsp
```

When the server is launched with a Python executable, the runner swaps that executable for the suite's virtual environment interpreter. For non-Python launchers such as Node-based servers, the runner still isolates `PATH`, `VIRTUAL_ENV`, and related Python environment variables for the server process, writes a temporary `pyrightconfig.json` at the suite root, and serves workspace configuration requests so Pylance-style servers can resolve the suite interpreter consistently.

## Tests

The repository uses Python's built-in `unittest` runner and a fake stdio LSP server in `tests/fixtures/fake_lsp_server.py` to exercise the CLI, runner, reporting, configuration loading, and benchmark environment behavior without depending on a real language server during test runs.

Run the full suite:

```powershell
python -m unittest discover -s tests -v
```

That command is the main test entry point for the repository. It currently runs all test modules under `tests/` and validates the following areas:

- `tests/test_benchmarks.py`: benchmark suite discovery, benchmark execution, validation failures on empty results, suite-local virtual environment creation, temporary `pyrightconfig.json` generation, current-mode `python.pythonPath` handling, and `workspace/configuration` logging/round-trips.
- `tests/test_cli.py`: basic CLI behavior for `list-scenarios`, `list-benchmarks`, `list-servers`, and `run`.
- `tests/test_reporting.py`: markdown and CSV report generation, `latest-results.md` updates, report re-rendering from summary JSON, result-difference reporting, and markdown table sorting by fastest average time.
- `tests/test_runner.py`: built-in scenario execution through the raw JSON-RPC runner and fast failure for unknown scenarios.
- `tests/test_server_configs.py`: local server config loading, relative argument resolution, baseline selection, `run-servers`, and `bench-servers` behavior when using configured servers.

Run an individual test module when you only need one area:

```powershell
python -m unittest tests.test_benchmarks -v
python -m unittest tests.test_cli -v
python -m unittest tests.test_reporting -v
python -m unittest tests.test_runner -v
python -m unittest tests.test_server_configs -v
```

The benchmark-oriented tests use the fixture suite in `tests/fixtures/benchmark_suite/`. Those tests intentionally create or reuse a suite-local `.venv` inside the fixture directory so they can verify the same isolated-environment behavior used by real benchmark runs.

If you only changed markdown or CSV rendering, `tests.test_reporting` is usually the fastest targeted check. If you changed benchmark environment setup, suite discovery, or benchmark-point execution, start with `tests.test_benchmarks` and then run the full suite before finishing.
