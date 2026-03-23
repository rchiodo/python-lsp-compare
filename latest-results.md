# Python LSP Benchmark Comparison

Generated from `results/bench-servers/summary-20260323T165043Z.json`

- Generated at: 20260323T165043Z
- Config: `github-releases`
- Servers: pyright, ty, pyrefly, pylsp-mypy
- Baseline server: Pyright (pyright)
- Benchmarks: data_science, django, pandas, sqlalchemy, transformers, web

## Server Versions

| Server | Version | Source |
| --- | --- | --- |
| Pyright | 1.1.408 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/pyright/1.1.408/package/dist/pyright-langserver.js |
| Ty | 0.0.24 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/ty/0.0.24/ty-x86_64-unknown-linux-gnu/ty |
| Pyrefly | 0.57.1 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/pyrefly/0.57.1/pyrefly |
| pylsp-mypy | 1.14.0 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/pylsp-mypy/venv/bin/pylsp |

## Server Notes

- **Pyright**: Requires Node.js to be installed.
- **pylsp-mypy**: Uses python-lsp-server (pylsp) with the pylsp-mypy plugin.
- **pylsp-mypy**: LSP features like hover and completion are provided by pylsp/jedi, not mypy.
- **pylsp-mypy**: mypy contributes diagnostics only.


## Overview

| Server | Success | Benchmarks | Wall clock ms | Avg measured ms | Measured requests | Non-empty % | Failed points |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 6 | 7024.86 | 3.18 | 150 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | no | 6 | 10664.03 | 22.77 | 150 | 87% | 3 |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | no | 6 | 88302.06 | 60.88 | 150 | 93% | 1 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | no | 6 | 257040.62 | 599.51 | 150 | 80% | 5 |

*Wall clock ms includes server startup, warmup iterations, and shutdown — not just measured requests.*

## Benchmark: data_science

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 1006.06 | 4.14 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 1432.34 | 14.60 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 14601.68 | 49.27 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | no | 7878.70 | 90.18 | 5 | 25 | 80% | 1 |

### dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 1.67 | 1.97 | 100% | 225.00 | +24.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 6.69 | 12.01 | 100% | 201.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 40.72 | 160.53 | 100% | 250.00 | +49.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 44.37 | 50.65 | 100% | 181.00 | -20.00 | pass |

### dataframe describe hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.26 | 0.27 | 100% | 3908.00 | -111.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 1.09 | 1.21 | 100% | 4019.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 3.46 | 11.80 | 100% | 8341.00 | +4322.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 203.92 | 231.89 | 100% | 4134.00 | +115.00 | pass |

### summarize definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.21 | 0.21 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.29 | 0.34 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 0.38 | 0.43 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 1.05 | 1.12 | 100% | 1.00 | 0.00 | pass |

### edit array then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | no | 4.26 | 4.33 | 0% | 0.00 | -169.00 | fail (10) |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 16.61 | 17.08 | 100% | 167.00 | -2.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 28.22 | 37.12 | 100% | 149.00 | -20.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 209.88 | 317.34 | 100% | 169.00 | 0.00 | pass |

### edit array then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.28 | 0.30 | 100% | 354.00 | +76.00 | pass |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 1.94 | 1.99 | 100% | 376.00 | +98.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 28.32 | 32.17 | 100% | 278.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 197.31 | 231.58 | 100% | 5644.00 | +5366.00 | pass |

### Result Differences

- dataframe completion: result differences detected (181.00, 201.00, 225.00, 250.00).
- dataframe describe hover: result differences detected (3908.00, 4019.00, 4134.00, 8341.00).
- edit array then complete (edit+completion): result differences detected (0.00, 149.00, 167.00, 169.00).
- edit array then hover (edit+hover): result differences detected (278.00, 354.00, 376.00, 5644.00).

## Benchmark: django

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 770.23 | 1.50 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | no | 935.69 | 7.21 | 5 | 25 | 80% | 1 |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | no | 7394.26 | 20.18 | 5 | 25 | 80% | 1 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 6860.12 | 157.31 | 5 | 25 | 100% | 0 |

### queryset completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 4.88 | 8.20 | 100% | 237.00 | +218.20 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 7.11 | 14.12 | 100% | 18.80 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 34.04 | 134.38 | 100% | 38.00 | +19.20 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 262.12 | 607.72 | 100% | 2.00 | -16.80 | pass |

### queryset filter hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.21 | 0.23 | 100% | 46.00 | -11.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.27 | 0.30 | 100% | 298.00 | +241.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 0.57 | 0.64 | 100% | 57.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 173.24 | 174.02 | 100% | 57.00 | 0.00 | pass |

### model definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.17 | 0.19 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.21 | 0.22 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 0.43 | 0.49 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 1.08 | 1.13 | 100% | 1.00 | 0.00 | pass |

### edit queryset then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 1.23 | 1.29 | 100% | 23.00 | +23.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | no | 1.28 | 3.41 | 0% | 0.00 | 0.00 | fail (10) |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | no | 53.52 | 59.23 | 0% | 0.00 | 0.00 | fail (10) |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 152.50 | 154.47 | 100% | 94.00 | +94.00 | pass |

### edit queryset then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.25 | 0.32 | 100% | 21.00 | -7.00 | pass |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 1.01 | 1.04 | 100% | 7.00 | -21.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 39.26 | 44.14 | 100% | 28.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 197.62 | 200.84 | 100% | 49.00 | +21.00 | pass |

### Result Differences

- queryset completion: result differences detected (18.80, 2.00, 237.00, 38.00).
- queryset filter hover: result differences detected (298.00, 46.00, 57.00).
- edit queryset then complete (edit+completion): result differences detected (0.00, 23.00, 94.00).
- edit queryset then hover (edit+hover): result differences detected (21.00, 28.00, 49.00, 7.00).

## Benchmark: pandas

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 1352.31 | 6.16 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 1419.51 | 17.92 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 18844.07 | 111.75 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 8507.59 | 149.89 | 5 | 25 | 100% | 0 |

### report dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 17.03 | 21.72 | 100% | 1000.00 | +725.80 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 46.37 | 184.17 | 100% | 39.00 | -235.20 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 77.36 | 263.29 | 100% | 274.20 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 127.28 | 329.37 | 100% | 6.00 | -268.20 | pass |

### dataframe groupby hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.24 | 0.26 | 100% | 308.00 | -42.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 0.66 | 0.74 | 100% | 350.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 1.80 | 1.87 | 100% | 3120.00 | +2770.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 202.64 | 204.27 | 100% | 301.00 | -49.00 | pass |

### build report definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.20 | 0.20 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.37 | 0.51 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 0.47 | 0.55 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 1.44 | 1.52 | 100% | 1.00 | 0.00 | pass |

### edit dataframe then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 11.86 | 12.57 | 100% | 448.00 | +7.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 40.72 | 61.70 | 100% | 256.00 | -185.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 223.29 | 240.00 | 100% | 442.00 | +1.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 470.00 | 883.06 | 100% | 441.00 | 0.00 | pass |

### edit dataframe then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.35 | 0.58 | 100% | 328.00 | -3964.00 | pass |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 1.47 | 1.64 | 100% | 281.00 | -4011.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 10.26 | 11.53 | 100% | 4292.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 194.83 | 197.06 | 100% | 232.00 | -4060.00 | pass |

### Result Differences

- report dataframe completion: result differences detected (1000.00, 274.20, 39.00, 6.00).
- dataframe groupby hover: result differences detected (301.00, 308.00, 3120.00, 350.00).
- edit dataframe then complete (edit+completion): result differences detected (256.00, 441.00, 442.00, 448.00).
- edit dataframe then hover (edit+hover): result differences detected (232.00, 281.00, 328.00, 4292.00).

## Benchmark: sqlalchemy

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 846.31 | 1.67 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | no | 1450.62 | 18.04 | 5 | 25 | 80% | 1 |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 8375.06 | 43.65 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | no | 7594.66 | 96.19 | 5 | 25 | 60% | 2 |

### query completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 4.28 | 10.65 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 9.99 | 12.98 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 77.94 | 132.10 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 80.01 | 318.09 | 100% | 38.00 | +37.00 | pass |

### sessionmaker hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.38 | 0.42 | 100% | 10580.00 | +8.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 2.40 | 3.70 | 100% | 13682.00 | +3110.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 2.90 | 3.43 | 100% | 10572.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 345.67 | 364.66 | 100% | 10498.00 | -74.00 | pass |

### mapped class definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.25 | 0.34 | 100% | 2.00 | +1.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.77 | 2.40 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 1.02 | 1.13 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 1.06 | 1.08 | 100% | 1.00 | 0.00 | pass |

### edit query then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 1.92 | 2.10 | 100% | 23.00 | -16.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 6.73 | 11.39 | 100% | 17.00 | -22.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | no | 28.31 | 28.68 | 0% | 0.00 | -39.00 | fail (10) |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 119.39 | 154.13 | 100% | 39.00 | 0.00 | pass |

### edit session then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | no | 0.29 | 0.32 | 0% | 0.00 | -900.00 | fail (10) |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 1.54 | 1.59 | 100% | 304.00 | -596.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | no | 27.99 | 28.49 | 0% | 0.00 | -900.00 | fail (10) |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 84.94 | 99.47 | 100% | 900.00 | 0.00 | pass |

### Result Differences

- query completion: result differences detected (1.00, 38.00).
- sessionmaker hover: result differences detected (10498.00, 10572.00, 10580.00, 13682.00).
- mapped class definition: result differences detected (1.00, 2.00).
- edit query then complete (edit+completion): result differences detected (0.00, 17.00, 23.00, 39.00).
- edit session then hover (edit+hover): result differences detected (0.00, 304.00, 900.00).

## Benchmark: transformers

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 2186.52 | 3.71 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 3977.40 | 67.99 | 5 | 25 | 80% | 0 |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 33166.51 | 132.87 | 5 | 25 | 80% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | no | 221246.36 | 3033.49 | 5 | 25 | 40% | 2 |

### classifier pipeline completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 11.45 | 13.88 | 100% | 767.00 | +644.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 51.53 | 85.08 | 100% | 123.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 144.04 | 147.76 | 100% | 2.00 | -121.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 335.19 | 1339.36 | 100% | 38.00 | -85.00 | pass |

### pipeline hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.23 | 0.23 | 100% | 7.00 | -27.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.23 | 0.25 | 100% | 48.00 | +14.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 0.49 | 0.58 | 100% | 34.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | no | 2603.03 | 2680.10 | 0% | 0.00 | -34.00 | fail (10) |

### auto tokenizer definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.24 | 0.25 | 100% | 1.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.25 | 0.27 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 0.42 | 0.45 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 2297.29 | 2379.68 | 100% | 1.00 | 0.00 | pass |

### edit prediction then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 2.23 | 7.53 | 0% | 0.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 2.75 | 3.12 | 0% | 0.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 3.14 | 3.47 | 100% | 23.00 | +23.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 5.87 | 6.56 | 0% | 0.00 | 0.00 | pass |

### edit tokenizer then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 2.08 | 3.79 | 100% | 43.00 | +13.00 | pass |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 3.48 | 4.09 | 100% | 7.00 | -23.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 606.04 | 643.17 | 100% | 30.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | no | 10120.34 | 10276.12 | 0% | 0.00 | -30.00 | fail (10) |

### Result Differences

- classifier pipeline completion: result differences detected (123.00, 2.00, 38.00, 767.00).
- pipeline hover: result differences detected (0.00, 34.00, 48.00, 7.00).
- edit prediction then complete (edit+completion): result differences detected (0.00, 23.00).
- edit tokenizer then hover (edit+hover): result differences detected (0.00, 30.00, 43.00, 7.00).

## Benchmark: web

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 863.43 | 1.91 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 5920.48 | 7.55 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | no | 1448.46 | 10.89 | 5 | 25 | 80% | 1 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 4953.18 | 70.01 | 5 | 25 | 100% | 0 |

### request args completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 4.63 | 8.04 | 100% | 16.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 5.96 | 9.97 | 100% | 441.00 | +425.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 22.34 | 27.37 | 100% | 1.00 | -15.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 49.85 | 173.89 | 100% | 351.40 | +335.40 | pass |

### client session hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.22 | 0.24 | 100% | 7.00 | -19.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 0.58 | 0.70 | 100% | 26.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 3.62 | 11.64 | 100% | 314.00 | +288.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 20.38 | 40.66 | 100% | 359.00 | +333.00 | pass |

### client references

Method: `textDocument/references`

| Server | Success | Mean ms | P95 ms | Non-empty % | References found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.33 | 0.35 | 100% | 2.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.45 | 0.51 | 100% | 2.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 0.72 | 0.83 | 100% | 2.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 15.14 | 26.24 | 100% | 2.00 | 0.00 | pass |

### edit response then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | no | 0.41 | 0.44 | 0% | 0.00 | -205.00 | fail (10) |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 2.22 | 2.38 | 100% | 227.00 | +22.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 4.54 | 7.43 | 100% | 205.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 107.26 | 162.46 | 100% | 56.00 | -149.00 | pass |

### edit response then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T165043Z.json) | yes | 0.21 | 0.25 | 100% | 31.00 | -731.00 | pass |
| [Ty](latest-results/ty-20260323T165043Z.json) | yes | 0.72 | 0.75 | 100% | 304.00 | -458.00 | pass |
| [Pyright](latest-results/pyright-20260323T165043Z.json) | yes | 27.28 | 29.85 | 100% | 762.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T165043Z.json) | yes | 184.90 | 187.20 | 100% | 257.00 | -505.00 | pass |

### Result Differences

- request args completion: result differences detected (1.00, 16.00, 351.40, 441.00).
- client session hover: result differences detected (26.00, 314.00, 359.00, 7.00).
- edit response then complete (edit+completion): result differences detected (0.00, 205.00, 227.00, 56.00).
- edit response then hover (edit+hover): result differences detected (257.00, 304.00, 31.00, 762.00).
