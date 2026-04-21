# Python LSP Benchmark Comparison

Generated from `results/bench-servers/summary-20260421T072138Z.json`

- Generated at: 20260421T072138Z
- Config: `github-releases`
- Servers: pyright, ty, pyrefly, pylsp-mypy
- Baseline server: Pyright (pyright)
- Benchmarks: data_science, django, pandas, sqlalchemy, transformers, web

## Server Versions

| Server | Version | Source |
| --- | --- | --- |
| Pyright | 1.1.409 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/pyright/1.1.409/package/dist/pyright-langserver.js |
| Ty | 0.0.32 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/ty/0.0.32/ty-x86_64-unknown-linux-gnu/ty |
| Pyrefly | 0.62.0 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/pyrefly/venv/bin/pyrefly |
| pylsp-mypy | 1.14.0 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/pylsp-mypy/venv/bin/pylsp |

## Server Notes

- **Pyright**: Requires Node.js to be installed.
- **Pyrefly**: Installed from PyPI into an isolated venv because GitHub release binaries are no longer published.
- **pylsp-mypy**: Uses python-lsp-server (pylsp) with the pylsp-mypy plugin.
- **pylsp-mypy**: LSP features like hover and completion are provided by pylsp/jedi, not mypy.
- **pylsp-mypy**: mypy contributes diagnostics only.


## Overview

| Server | Success | Benchmarks | Wall clock ms | Avg measured ms | Measured requests | Non-empty % | Failed points |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 6 | 7038.22 | 3.52 | 150 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 6 | 10447.03 | 23.89 | 150 | 97% | 0 |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 6 | 87116.24 | 59.62 | 150 | 97% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | no | 6 | 212677.65 | 348.32 | 150 | 80% | 5 |

*Wall clock ms includes server startup, warmup iterations, and shutdown — not just measured requests.*

## Benchmark: data_science

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 1005.85 | 4.53 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 1466.95 | 14.06 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 14931.96 | 57.68 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | no | 8199.67 | 91.97 | 5 | 25 | 80% | 1 |

### dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 2.04 | 2.52 | 100% | 225.00 | +24.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 6.07 | 9.66 | 100% | 201.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 40.12 | 158.27 | 100% | 250.00 | +49.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 68.52 | 98.44 | 100% | 181.00 | -20.00 | pass |

### dataframe describe hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.33 | 0.35 | 100% | 4244.00 | +225.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 1.26 | 1.31 | 100% | 4019.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 6.61 | 16.99 | 100% | 3604.00 | -415.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 198.26 | 201.42 | 100% | 4134.00 | +115.00 | pass |

### summarize definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.24 | 0.25 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.29 | 0.31 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 0.42 | 0.48 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 1.12 | 1.23 | 100% | 1.00 | 0.00 | pass |

### edit array then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | no | 4.37 | 4.66 | 0% | 0.00 | -169.00 | fail (10) |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 17.92 | 18.70 | 100% | 167.00 | -2.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 22.51 | 31.57 | 100% | 149.00 | -20.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 248.19 | 361.76 | 100% | 169.00 | 0.00 | pass |

### edit array then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.77 | 0.86 | 100% | 2075.00 | +1797.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 2.14 | 2.20 | 100% | 376.00 | +98.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 32.46 | 39.13 | 100% | 278.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 187.59 | 189.61 | 100% | 5644.00 | +5366.00 | pass |

### Result Differences

- dataframe completion: result differences detected (181.00, 201.00, 225.00, 250.00).
- dataframe describe hover: result differences detected (3604.00, 4019.00, 4134.00, 4244.00).
- edit array then complete (edit+completion): result differences detected (0.00, 149.00, 167.00, 169.00).
- edit array then hover (edit+hover): result differences detected (2075.00, 278.00, 376.00, 5644.00).

## Benchmark: django

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 716.86 | 1.99 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 840.29 | 6.12 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 7354.42 | 14.56 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 8553.11 | 178.45 | 5 | 25 | 100% | 0 |

### queryset completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 4.96 | 7.77 | 100% | 10.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 5.11 | 8.17 | 100% | 256.00 | +246.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 24.13 | 94.79 | 100% | 38.00 | +28.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 206.68 | 613.28 | 100% | 2.00 | -8.00 | pass |

### queryset filter hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.25 | 0.27 | 100% | 46.00 | -11.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.25 | 0.30 | 100% | 298.00 | +241.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 0.51 | 0.61 | 100% | 57.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 177.83 | 180.34 | 100% | 57.00 | 0.00 | pass |

### model definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.20 | 0.22 | 100% | 1.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.22 | 0.24 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 0.43 | 0.57 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 1.08 | 1.13 | 100% | 1.00 | 0.00 | pass |

### edit queryset then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 2.68 | 4.94 | 100% | 83.00 | -22.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 2.85 | 3.10 | 100% | 104.00 | -1.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 25.17 | 26.95 | 100% | 105.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 298.46 | 332.95 | 100% | 143.00 | +38.00 | pass |

### edit queryset then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 1.51 | 1.54 | 100% | 100.00 | +17.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 3.35 | 4.10 | 100% | 1190.00 | +1107.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 41.73 | 47.84 | 100% | 83.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 208.17 | 210.85 | 100% | 71.00 | -12.00 | pass |

### Result Differences

- queryset completion: result differences detected (10.00, 2.00, 256.00, 38.00).
- queryset filter hover: result differences detected (298.00, 46.00, 57.00).
- edit queryset then complete (edit+completion): result differences detected (104.00, 105.00, 143.00, 83.00).
- edit queryset then hover (edit+hover): result differences detected (100.00, 1190.00, 71.00, 83.00).

## Benchmark: pandas

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 1389.29 | 6.75 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 1344.10 | 14.53 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 18544.90 | 89.87 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 8402.10 | 145.07 | 5 | 25 | 100% | 0 |

### report dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 17.75 | 22.92 | 100% | 1000.00 | +725.80 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 42.95 | 170.43 | 100% | 39.00 | -235.20 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 73.63 | 245.68 | 100% | 274.20 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 78.73 | 221.35 | 100% | 6.00 | -268.20 | pass |

### dataframe groupby hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.28 | 0.30 | 100% | 308.00 | -42.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 0.87 | 1.06 | 100% | 350.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 2.03 | 2.13 | 100% | 3120.00 | +2770.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 210.13 | 216.15 | 100% | 301.00 | -49.00 | pass |

### build report definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.22 | 0.23 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.23 | 0.24 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 0.43 | 0.51 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 1.04 | 1.09 | 100% | 1.00 | 0.00 | pass |

### edit dataframe then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 13.66 | 13.97 | 100% | 448.00 | +7.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 13.72 | 14.41 | 100% | 256.00 | -185.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 236.26 | 241.00 | 100% | 442.00 | +1.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 364.37 | 800.60 | 100% | 441.00 | 0.00 | pass |

### edit dataframe then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 1.87 | 2.09 | 100% | 4378.00 | +86.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 10.03 | 12.69 | 100% | 4292.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 13.70 | 41.87 | 100% | 2481.00 | -1811.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 199.20 | 201.06 | 100% | 232.00 | -4060.00 | pass |

### Result Differences

- report dataframe completion: result differences detected (1000.00, 274.20, 39.00, 6.00).
- dataframe groupby hover: result differences detected (301.00, 308.00, 3120.00, 350.00).
- edit dataframe then complete (edit+completion): result differences detected (256.00, 441.00, 442.00, 448.00).
- edit dataframe then hover (edit+hover): result differences detected (232.00, 2481.00, 4292.00, 4378.00).

## Benchmark: sqlalchemy

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 821.47 | 1.72 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 1366.13 | 17.43 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 8099.49 | 44.63 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | no | 7348.76 | 91.20 | 5 | 25 | 60% | 2 |

### query completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 4.36 | 10.65 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 17.63 | 21.81 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 66.10 | 105.43 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 84.49 | 321.04 | 100% | 38.00 | +37.00 | pass |

### sessionmaker hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.39 | 0.44 | 100% | 10628.00 | +56.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.82 | 0.88 | 100% | 13682.00 | +3110.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 1.96 | 2.23 | 100% | 10572.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 332.73 | 337.57 | 100% | 10498.00 | -74.00 | pass |

### mapped class definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.21 | 0.22 | 100% | 2.00 | +1.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.30 | 0.33 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 0.57 | 0.65 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 1.04 | 1.10 | 100% | 1.00 | 0.00 | pass |

### edit query then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.92 | 1.07 | 100% | 17.00 | -22.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 2.04 | 2.18 | 100% | 23.00 | -16.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | no | 28.65 | 29.07 | 0% | 0.00 | -39.00 | fail (10) |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 122.52 | 157.28 | 100% | 39.00 | 0.00 | pass |

### edit session then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.64 | 0.86 | 100% | 1869.00 | +969.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 1.61 | 1.64 | 100% | 958.00 | +58.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | no | 27.49 | 28.29 | 0% | 0.00 | -900.00 | fail (10) |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 80.45 | 89.13 | 100% | 900.00 | 0.00 | pass |

### Result Differences

- query completion: result differences detected (1.00, 38.00).
- sessionmaker hover: result differences detected (10498.00, 10572.00, 10628.00, 13682.00).
- mapped class definition: result differences detected (1.00, 2.00).
- edit query then complete (edit+completion): result differences detected (0.00, 17.00, 23.00, 39.00).
- edit session then hover (edit+hover): result differences detected (0.00, 1869.00, 900.00, 958.00).

## Benchmark: transformers

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 2244.51 | 3.77 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 4088.71 | 80.58 | 5 | 25 | 80% | 0 |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 32595.79 | 141.83 | 5 | 25 | 80% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | no | 175237.10 | 1511.28 | 5 | 25 | 40% | 2 |

### classifier pipeline completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 12.26 | 14.69 | 100% | 768.00 | +645.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 55.50 | 83.84 | 100% | 123.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 138.90 | 139.94 | 100% | 2.00 | -121.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 386.58 | 1544.83 | 100% | 38.00 | -85.00 | pass |

### pipeline hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.20 | 0.22 | 100% | 7.00 | -27.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.22 | 0.22 | 100% | 48.00 | +14.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 0.49 | 0.54 | 100% | 34.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | no | 2551.49 | 2593.14 | 0% | 0.00 | -34.00 | fail (10) |

### auto tokenizer definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.23 | 0.25 | 100% | 1.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.24 | 0.26 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 0.42 | 0.46 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 2242.36 | 2305.34 | 100% | 1.00 | 0.00 | pass |

### edit prediction then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 2.60 | 2.75 | 0% | 0.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 3.20 | 3.36 | 100% | 23.00 | +23.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 6.41 | 7.36 | 0% | 0.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 15.42 | 20.46 | 0% | 0.00 | 0.00 | pass |

### edit tokenizer then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.47 | 0.52 | 100% | 33.00 | +3.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 2.93 | 2.94 | 100% | 7.00 | -23.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 646.34 | 668.91 | 100% | 30.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | no | 2621.07 | 2676.21 | 0% | 0.00 | -30.00 | fail (10) |

### Result Differences

- classifier pipeline completion: result differences detected (123.00, 2.00, 38.00, 768.00).
- pipeline hover: result differences detected (0.00, 34.00, 48.00, 7.00).
- edit prediction then complete (edit+completion): result differences detected (0.00, 23.00).
- edit tokenizer then hover (edit+hover): result differences detected (0.00, 30.00, 33.00, 7.00).

## Benchmark: web

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 860.25 | 2.34 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 5589.67 | 9.16 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 1340.85 | 10.63 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 4936.90 | 71.96 | 5 | 25 | 100% | 0 |

### request args completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 5.31 | 8.97 | 100% | 16.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 7.10 | 10.53 | 100% | 441.00 | +425.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 25.52 | 32.41 | 100% | 1.00 | -15.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 45.56 | 156.28 | 100% | 351.40 | +335.40 | pass |

### client session hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.22 | 0.23 | 100% | 7.00 | -19.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 0.58 | 0.70 | 100% | 26.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 4.35 | 11.70 | 100% | 314.00 | +288.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 27.53 | 48.84 | 100% | 359.00 | +333.00 | pass |

### client references

Method: `textDocument/references`

| Server | Success | Mean ms | P95 ms | Non-empty % | References found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.39 | 0.41 | 100% | 2.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.49 | 0.59 | 100% | 2.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 0.79 | 0.90 | 100% | 2.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 23.15 | 46.21 | 100% | 2.00 | 0.00 | pass |

### edit response then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 0.58 | 0.62 | 100% | 32.00 | -173.00 | pass |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 3.01 | 3.12 | 100% | 227.00 | +22.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 6.08 | 9.08 | 100% | 205.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 93.12 | 95.45 | 100% | 56.00 | -149.00 | pass |

### edit response then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260421T072138Z.json) | yes | 0.91 | 0.95 | 100% | 304.00 | -458.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260421T072138Z.json) | yes | 2.26 | 4.55 | 100% | 3486.00 | +2724.00 | pass |
| [Pyright](latest-results/pyright-20260421T072138Z.json) | yes | 33.06 | 35.82 | 100% | 762.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260421T072138Z.json) | yes | 190.46 | 192.04 | 100% | 257.00 | -505.00 | pass |

### Result Differences

- request args completion: result differences detected (1.00, 16.00, 351.40, 441.00).
- client session hover: result differences detected (26.00, 314.00, 359.00, 7.00).
- edit response then complete (edit+completion): result differences detected (205.00, 227.00, 32.00, 56.00).
- edit response then hover (edit+hover): result differences detected (257.00, 304.00, 3486.00, 762.00).
