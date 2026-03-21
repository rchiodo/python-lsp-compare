# Python LSP Benchmark Comparison

Generated from `results/bench-servers/summary-20260321T001740Z.json`

- Generated at: 20260321T001740Z
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
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 6 | 7172.28 | 3.33 | 150 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | no | 6 | 10758.47 | 22.89 | 150 | 87% | 4 |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | no | 6 | 89895.60 | 63.35 | 150 | 93% | 2 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | no | 6 | 294801.59 | 623.09 | 150 | 80% | 6 |

*Wall clock ms includes server startup, warmup iterations, and shutdown — not just measured requests.*

## Benchmark: data_science

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 1039.96 | 4.31 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 1511.32 | 14.30 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 14937.38 | 55.19 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | no | 8419.01 | 93.00 | 5 | 25 | 80% | 1 |

### dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 1.72 | 2.13 | 100% | 225.00 | +24.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 6.02 | 10.53 | 100% | 201.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 41.25 | 162.97 | 100% | 250.00 | +49.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 54.68 | 62.67 | 100% | 181.00 | -20.00 | pass |

### dataframe describe hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.27 | 0.30 | 100% | 3908.00 | -111.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 1.13 | 1.20 | 100% | 4019.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 3.60 | 12.51 | 100% | 8341.00 | +4322.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 199.46 | 200.41 | 100% | 4134.00 | +115.00 | pass |

### summarize definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.20 | 0.22 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.27 | 0.30 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 0.40 | 0.47 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 1.06 | 1.10 | 100% | 1.00 | 0.00 | pass |

### edit array then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | no | 4.38 | 4.49 | 0% | 0.00 | -169.00 | fail (10) |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 17.41 | 18.22 | 100% | 167.00 | -2.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 26.06 | 35.91 | 100% | 149.00 | -20.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 237.23 | 358.56 | 100% | 169.00 | 0.00 | pass |

### edit array then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.30 | 0.32 | 100% | 354.00 | +76.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 1.96 | 2.03 | 100% | 376.00 | +98.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 31.17 | 33.88 | 100% | 278.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 205.43 | 247.51 | 100% | 5644.00 | +5366.00 | pass |

### Result Differences

- dataframe completion: result differences detected (181.00, 201.00, 225.00, 250.00).
- dataframe describe hover: result differences detected (3908.00, 4019.00, 4134.00, 8341.00).
- edit array then complete (edit+completion): result differences detected (0.00, 149.00, 167.00, 169.00).
- edit array then hover (edit+hover): result differences detected (278.00, 354.00, 376.00, 5644.00).

## Benchmark: django

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 778.45 | 1.94 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | no | 978.66 | 7.45 | 5 | 25 | 80% | 1 |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | no | 7444.83 | 20.46 | 5 | 25 | 80% | 1 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 7138.88 | 164.30 | 5 | 25 | 100% | 0 |

### queryset completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 6.90 | 12.27 | 100% | 237.00 | +218.20 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 7.37 | 14.76 | 100% | 18.80 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 33.92 | 134.35 | 100% | 38.00 | +19.20 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 280.27 | 538.97 | 100% | 2.00 | -16.80 | pass |

### queryset filter hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.23 | 0.24 | 100% | 298.00 | +241.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.24 | 0.26 | 100% | 46.00 | -11.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 0.68 | 0.78 | 100% | 57.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 181.66 | 183.28 | 100% | 57.00 | 0.00 | pass |

### model definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.21 | 0.23 | 100% | 1.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.23 | 0.26 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 0.49 | 0.57 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 1.07 | 1.13 | 100% | 1.00 | 0.00 | pass |

### edit queryset then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 1.37 | 1.45 | 100% | 23.00 | +23.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | no | 2.72 | 4.99 | 0% | 0.00 | 0.00 | fail (10) |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | no | 53.13 | 54.98 | 0% | 0.00 | 0.00 | fail (10) |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 155.85 | 158.68 | 100% | 94.00 | +94.00 | pass |

### edit queryset then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.20 | 0.21 | 100% | 21.00 | -7.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.97 | 0.99 | 100% | 7.00 | -21.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 40.62 | 44.15 | 100% | 28.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 202.64 | 204.49 | 100% | 49.00 | +21.00 | pass |

### Result Differences

- queryset completion: result differences detected (18.80, 2.00, 237.00, 38.00).
- queryset filter hover: result differences detected (298.00, 46.00, 57.00).
- edit queryset then complete (edit+completion): result differences detected (0.00, 23.00, 94.00).
- edit queryset then hover (edit+hover): result differences detected (21.00, 28.00, 49.00, 7.00).

## Benchmark: pandas

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 1357.65 | 6.13 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 1439.47 | 17.36 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 18932.86 | 114.70 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 8699.66 | 153.65 | 5 | 25 | 100% | 0 |

### report dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 16.84 | 21.27 | 100% | 1000.00 | +725.80 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 50.32 | 199.97 | 100% | 39.00 | -235.20 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 77.50 | 257.36 | 100% | 274.20 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 122.17 | 331.20 | 100% | 6.00 | -268.20 | pass |

### dataframe groupby hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.24 | 0.26 | 100% | 308.00 | -42.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 0.68 | 0.81 | 100% | 350.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 2.54 | 3.12 | 100% | 3120.00 | +2770.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 209.36 | 212.64 | 100% | 301.00 | -49.00 | pass |

### build report definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.21 | 0.23 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.21 | 0.23 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 0.47 | 0.54 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 1.07 | 1.10 | 100% | 1.00 | 0.00 | pass |

### edit dataframe then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 12.03 | 12.85 | 100% | 448.00 | +7.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 33.33 | 50.95 | 100% | 256.00 | -185.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 233.16 | 239.93 | 100% | 442.00 | +1.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 485.29 | 912.43 | 100% | 441.00 | 0.00 | pass |

### edit dataframe then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.40 | 0.44 | 100% | 328.00 | -3964.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 1.34 | 1.37 | 100% | 281.00 | -4011.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 9.55 | 11.14 | 100% | 4292.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 202.48 | 204.59 | 100% | 232.00 | -4060.00 | pass |

### Result Differences

- report dataframe completion: result differences detected (1000.00, 274.20, 39.00, 6.00).
- dataframe groupby hover: result differences detected (301.00, 308.00, 3120.00, 350.00).
- edit dataframe then complete (edit+completion): result differences detected (256.00, 441.00, 442.00, 448.00).
- edit dataframe then hover (edit+hover): result differences detected (232.00, 281.00, 328.00, 4292.00).

## Benchmark: sqlalchemy

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 894.78 | 1.75 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | no | 1439.93 | 17.35 | 5 | 25 | 80% | 1 |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 8442.20 | 44.26 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | no | 7779.03 | 97.26 | 5 | 25 | 60% | 2 |

### query completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 4.62 | 11.12 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 9.64 | 12.97 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 71.18 | 125.54 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 83.04 | 326.35 | 100% | 38.00 | +37.00 | pass |

### sessionmaker hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.39 | 0.41 | 100% | 10580.00 | +8.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.71 | 0.75 | 100% | 13682.00 | +3110.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 2.60 | 2.83 | 100% | 10572.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 354.32 | 392.54 | 100% | 10498.00 | -74.00 | pass |

### mapped class definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.24 | 0.28 | 100% | 1.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.25 | 0.26 | 100% | 2.00 | +1.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 0.99 | 1.08 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 1.07 | 1.11 | 100% | 1.00 | 0.00 | pass |

### edit query then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 1.95 | 2.20 | 100% | 23.00 | -16.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 2.50 | 7.25 | 100% | 17.00 | -22.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | no | 30.67 | 32.48 | 0% | 0.00 | -39.00 | fail (10) |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 125.63 | 158.40 | 100% | 39.00 | 0.00 | pass |

### edit session then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | no | 0.24 | 0.29 | 0% | 0.00 | -900.00 | fail (10) |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 1.52 | 1.54 | 100% | 304.00 | -596.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | no | 29.05 | 30.10 | 0% | 0.00 | -900.00 | fail (10) |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 82.45 | 89.62 | 100% | 900.00 | 0.00 | pass |

### Result Differences

- query completion: result differences detected (1.00, 38.00).
- sessionmaker hover: result differences detected (10498.00, 10572.00, 10580.00, 13682.00).
- mapped class definition: result differences detected (1.00, 2.00).
- edit query then complete (edit+completion): result differences detected (0.00, 17.00, 23.00, 39.00).
- edit session then hover (edit+hover): result differences detected (0.00, 304.00, 900.00).

## Benchmark: transformers

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 2232.62 | 3.87 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | no | 3986.31 | 70.63 | 5 | 25 | 80% | 1 |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | no | 34234.67 | 137.38 | 5 | 25 | 80% | 1 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | no | 257605.24 | 3159.71 | 5 | 25 | 40% | 3 |

### classifier pipeline completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 12.67 | 14.84 | 100% | 767.00 | +644.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 58.15 | 93.72 | 100% | 123.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 153.64 | 154.61 | 100% | 2.00 | -121.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 350.67 | 1352.37 | 100% | 38.00 | -85.00 | pass |

### pipeline hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.21 | 0.23 | 100% | 7.00 | -27.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.25 | 0.26 | 100% | 48.00 | +14.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 0.55 | 0.67 | 100% | 34.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | no | 2661.25 | 2712.82 | 0% | 0.00 | -34.00 | fail (10) |

### auto tokenizer definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.25 | 0.26 | 100% | 1.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.27 | 0.32 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 0.42 | 0.49 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 2310.06 | 2357.69 | 100% | 1.00 | 0.00 | pass |

### edit prediction then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | no | 0.69 | 0.78 | 0% | 0.00 | 0.00 | fail (10) |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | no | 2.65 | 2.84 | 0% | 0.00 | 0.00 | fail (10) |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 3.32 | 3.67 | 100% | 23.00 | +23.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | no | 6.17 | 6.63 | 0% | 0.00 | 0.00 | fail (10) |

### edit tokenizer then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 1.29 | 1.35 | 100% | 43.00 | +13.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 2.89 | 3.37 | 100% | 7.00 | -23.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 621.59 | 637.03 | 100% | 30.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | no | 10670.94 | 10775.29 | 0% | 0.00 | -30.00 | fail (10) |

### Result Differences

- classifier pipeline completion: result differences detected (123.00, 2.00, 38.00, 767.00).
- pipeline hover: result differences detected (0.00, 34.00, 48.00, 7.00).
- edit prediction then complete (edit+completion): result differences detected (0.00, 23.00).
- edit tokenizer then hover (edit+hover): result differences detected (0.00, 30.00, 43.00, 7.00).

## Benchmark: web

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 868.83 | 1.97 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 5903.67 | 8.10 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | no | 1402.77 | 10.25 | 5 | 25 | 80% | 1 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 5159.78 | 70.61 | 5 | 25 | 100% | 0 |

### request args completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 5.25 | 10.38 | 100% | 16.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 6.18 | 9.64 | 100% | 441.00 | +425.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 24.35 | 31.42 | 100% | 1.00 | -15.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 46.49 | 160.43 | 100% | 351.40 | +335.40 | pass |

### client session hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.20 | 0.22 | 100% | 7.00 | -19.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 0.52 | 0.59 | 100% | 26.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 3.80 | 12.39 | 100% | 314.00 | +288.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 23.47 | 37.07 | 100% | 359.00 | +333.00 | pass |

### client references

Method: `textDocument/references`

| Server | Success | Mean ms | P95 ms | Non-empty % | References found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.39 | 0.40 | 100% | 2.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.43 | 0.49 | 100% | 2.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 0.76 | 0.88 | 100% | 2.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 29.37 | 55.62 | 100% | 2.00 | 0.00 | pass |

### edit response then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | no | 0.40 | 0.42 | 0% | 0.00 | -205.00 | fail (10) |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 2.30 | 2.65 | 100% | 227.00 | +22.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 4.82 | 7.07 | 100% | 205.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 89.71 | 97.29 | 100% | 56.00 | -149.00 | pass |

### edit response then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260321T001740Z.json) | yes | 0.19 | 0.21 | 100% | 31.00 | -731.00 | pass |
| [Ty](latest-results/ty-20260321T001740Z.json) | yes | 0.71 | 0.73 | 100% | 304.00 | -458.00 | pass |
| [Pyright](latest-results/pyright-20260321T001740Z.json) | yes | 29.17 | 35.29 | 100% | 762.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260321T001740Z.json) | yes | 186.17 | 188.09 | 100% | 257.00 | -505.00 | pass |

### Result Differences

- request args completion: result differences detected (1.00, 16.00, 351.40, 441.00).
- client session hover: result differences detected (26.00, 314.00, 359.00, 7.00).
- edit response then complete (edit+completion): result differences detected (0.00, 205.00, 227.00, 56.00).
- edit response then hover (edit+hover): result differences detected (257.00, 304.00, 31.00, 762.00).
