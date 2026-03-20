# python-lsp-compare

`python-lsp-compare` is a small benchmark and regression harness for Python Language Server Protocol implementations.

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

- `--config`: path to the local server config file. Defaults to `configs/local/lsp_servers.json`.
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

- Copy `configs/lsp_servers.example.json` to `configs/local/lsp_servers.json`.
- Fill in the local executable paths for each server.
- The `configs/local/` directory is ignored by Git.

The local config is intentionally minimal: it identifies where each server executable or launcher lives on the current machine. Scenario selection, benchmark selection, benchmark environment creation, and package installation are handled by the runner so the same suite runs the same way for everyone.

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

The repository includes unit tests with a fake stdio LSP server.

```powershell
python -m unittest discover -s tests -v
```
