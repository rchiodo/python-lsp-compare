# Python LSP Benchmark Comparison

Generated from `results/bench-servers/summary-20260323T194605Z.json`

- Generated at: 20260323T194605Z
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
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 6 | 7012.64 | 3.40 | 150 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | no | 6 | 10722.76 | 23.32 | 150 | 90% | 2 |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 6 | 88161.28 | 58.19 | 150 | 97% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | no | 6 | 266173.03 | 609.97 | 150 | 80% | 5 |

*Wall clock ms includes server startup, warmup iterations, and shutdown — not just measured requests.*

## Benchmark: data_science

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 1067.96 | 5.26 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 1471.71 | 14.95 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 14774.14 | 55.52 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | no | 7907.75 | 93.01 | 5 | 25 | 80% | 1 |

### dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 1.66 | 1.97 | 100% | 225.00 | +24.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 5.94 | 10.04 | 100% | 201.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 40.62 | 160.42 | 100% | 250.00 | +49.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 47.29 | 56.26 | 100% | 181.00 | -20.00 | pass |

### dataframe describe hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.25 | 0.26 | 100% | 3908.00 | -111.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 1.17 | 1.45 | 100% | 4019.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 3.00 | 10.18 | 100% | 8341.00 | +4322.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 206.64 | 242.02 | 100% | 4134.00 | +115.00 | pass |

### summarize definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.20 | 0.20 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.27 | 0.33 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 0.38 | 0.43 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 1.05 | 1.07 | 100% | 1.00 | 0.00 | pass |

### edit array then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | no | 4.61 | 4.79 | 0% | 0.00 | -169.00 | fail (10) |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 21.85 | 24.22 | 100% | 167.00 | -2.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 30.03 | 38.76 | 100% | 149.00 | -20.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 240.26 | 336.63 | 100% | 169.00 | 0.00 | pass |

### edit array then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.85 | 2.51 | 100% | 354.00 | +76.00 | pass |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 2.32 | 2.64 | 100% | 376.00 | +98.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 29.84 | 34.63 | 100% | 278.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 205.46 | 240.36 | 100% | 5644.00 | +5366.00 | pass |

### Result Differences

- dataframe completion: result differences detected (181.00, 201.00, 225.00, 250.00).
- dataframe describe hover: result differences detected (3908.00, 4019.00, 4134.00, 8341.00).
- edit array then complete (edit+completion): result differences detected (0.00, 149.00, 167.00, 169.00).
- edit array then hover (edit+hover): result differences detected (278.00, 354.00, 376.00, 5644.00).

## Benchmark: django

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 742.82 | 1.81 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 955.66 | 7.27 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 7254.44 | 15.32 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 8788.44 | 185.30 | 5 | 25 | 100% | 0 |

### queryset completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 4.83 | 7.88 | 100% | 254.00 | +244.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 5.71 | 8.22 | 100% | 10.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 31.42 | 123.94 | 100% | 38.00 | +28.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 236.33 | 703.65 | 100% | 2.00 | -8.00 | pass |

### queryset filter hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.21 | 0.22 | 100% | 46.00 | -11.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.24 | 0.25 | 100% | 298.00 | +241.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 0.51 | 0.58 | 100% | 57.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 180.12 | 181.72 | 100% | 57.00 | 0.00 | pass |

### model definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.18 | 0.20 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.21 | 0.22 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 0.38 | 0.40 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 1.10 | 1.16 | 100% | 1.00 | 0.00 | pass |

### edit queryset then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 2.55 | 2.71 | 100% | 104.00 | -1.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 4.25 | 6.55 | 100% | 83.00 | -22.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 24.81 | 27.70 | 100% | 105.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 302.73 | 342.98 | 100% | 143.00 | +38.00 | pass |

### edit queryset then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.25 | 0.26 | 100% | 144.00 | +61.00 | pass |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 1.30 | 1.32 | 100% | 100.00 | +17.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 45.19 | 52.36 | 100% | 83.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 206.24 | 208.45 | 100% | 71.00 | -12.00 | pass |

### Result Differences

- queryset completion: result differences detected (10.00, 2.00, 254.00, 38.00).
- queryset filter hover: result differences detected (298.00, 46.00, 57.00).
- edit queryset then complete (edit+completion): result differences detected (104.00, 105.00, 143.00, 83.00).
- edit queryset then hover (edit+hover): result differences detected (100.00, 144.00, 71.00, 83.00).

## Benchmark: pandas

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 1339.90 | 6.21 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 1498.73 | 19.01 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 18184.95 | 89.49 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 8681.20 | 149.55 | 5 | 25 | 100% | 0 |

### report dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 17.00 | 21.49 | 100% | 1000.00 | +725.80 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 51.78 | 205.75 | 100% | 39.00 | -235.20 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 78.29 | 263.65 | 100% | 274.20 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 111.74 | 290.04 | 100% | 6.00 | -268.20 | pass |

### dataframe groupby hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.25 | 0.26 | 100% | 308.00 | -42.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 0.79 | 0.92 | 100% | 350.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 1.89 | 2.03 | 100% | 3120.00 | +2770.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 211.00 | 214.86 | 100% | 301.00 | -49.00 | pass |

### build report definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.21 | 0.22 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.40 | 0.78 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 0.43 | 0.55 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 1.53 | 1.74 | 100% | 1.00 | 0.00 | pass |

### edit dataframe then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 12.22 | 12.85 | 100% | 448.00 | +7.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 40.69 | 57.47 | 100% | 256.00 | -185.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 223.82 | 227.26 | 100% | 442.00 | +1.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 357.96 | 771.43 | 100% | 441.00 | 0.00 | pass |

### edit dataframe then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.29 | 0.33 | 100% | 328.00 | -3964.00 | pass |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 1.36 | 1.43 | 100% | 281.00 | -4011.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 9.98 | 11.99 | 100% | 4292.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 199.67 | 201.13 | 100% | 232.00 | -4060.00 | pass |

### Result Differences

- report dataframe completion: result differences detected (1000.00, 274.20, 39.00, 6.00).
- dataframe groupby hover: result differences detected (301.00, 308.00, 3120.00, 350.00).
- edit dataframe then complete (edit+completion): result differences detected (256.00, 441.00, 442.00, 448.00).
- edit dataframe then hover (edit+hover): result differences detected (232.00, 281.00, 328.00, 4292.00).

## Benchmark: sqlalchemy

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 843.40 | 1.64 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | no | 1422.84 | 16.78 | 5 | 25 | 80% | 1 |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 8291.40 | 43.92 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | no | 7658.78 | 93.79 | 5 | 25 | 60% | 2 |

### query completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 4.26 | 10.52 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 9.88 | 12.93 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 69.34 | 124.88 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 81.68 | 322.47 | 100% | 38.00 | +37.00 | pass |

### sessionmaker hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.36 | 0.37 | 100% | 10580.00 | +8.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.76 | 0.78 | 100% | 13682.00 | +3110.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 2.92 | 3.55 | 100% | 10572.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 342.51 | 369.58 | 100% | 10498.00 | -74.00 | pass |

### mapped class definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.19 | 0.20 | 100% | 2.00 | +1.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.26 | 0.28 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 1.00 | 1.04 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 1.07 | 1.13 | 100% | 1.00 | 0.00 | pass |

### edit query then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.95 | 1.04 | 100% | 17.00 | -22.00 | pass |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 1.91 | 2.12 | 100% | 23.00 | -16.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | no | 28.86 | 29.63 | 0% | 0.00 | -39.00 | fail (10) |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 120.57 | 153.83 | 100% | 39.00 | 0.00 | pass |

### edit session then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | no | 0.23 | 0.26 | 0% | 0.00 | -900.00 | fail (10) |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 1.48 | 1.49 | 100% | 304.00 | -596.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | no | 27.17 | 27.76 | 0% | 0.00 | -900.00 | fail (10) |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 85.23 | 98.45 | 100% | 900.00 | 0.00 | pass |

### Result Differences

- query completion: result differences detected (1.00, 38.00).
- sessionmaker hover: result differences detected (10498.00, 10572.00, 10580.00, 13682.00).
- mapped class definition: result differences detected (1.00, 2.00).
- edit query then complete (edit+completion): result differences detected (0.00, 17.00, 23.00, 39.00).
- edit session then hover (edit+hover): result differences detected (0.00, 304.00, 900.00).

## Benchmark: transformers

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 2177.35 | 3.66 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 3974.60 | 71.56 | 5 | 25 | 80% | 0 |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 33871.96 | 136.80 | 5 | 25 | 80% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | no | 228144.81 | 3067.56 | 5 | 25 | 40% | 2 |

### classifier pipeline completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 11.85 | 14.32 | 100% | 767.00 | +644.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 53.54 | 84.74 | 100% | 123.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 141.64 | 143.67 | 100% | 2.00 | -121.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 348.61 | 1341.91 | 100% | 38.00 | -85.00 | pass |

### pipeline hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.21 | 0.23 | 100% | 7.00 | -27.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.25 | 0.29 | 100% | 48.00 | +14.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 0.47 | 0.58 | 100% | 34.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | no | 2656.27 | 2754.98 | 0% | 0.00 | -34.00 | fail (10) |

### auto tokenizer definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.25 | 0.27 | 100% | 1.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.26 | 0.29 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 0.40 | 0.45 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 2323.88 | 2397.10 | 100% | 1.00 | 0.00 | pass |

### edit prediction then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 2.62 | 2.77 | 0% | 0.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 3.16 | 3.54 | 100% | 23.00 | +23.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 6.77 | 9.52 | 0% | 0.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 6.78 | 15.09 | 0% | 0.00 | 0.00 | pass |

### edit tokenizer then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 1.90 | 3.26 | 100% | 43.00 | +13.00 | pass |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 2.83 | 2.99 | 100% | 7.00 | -23.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 622.84 | 643.88 | 100% | 30.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | no | 10213.39 | 10405.25 | 0% | 0.00 | -30.00 | fail (10) |

### Result Differences

- classifier pipeline completion: result differences detected (123.00, 2.00, 38.00, 767.00).
- pipeline hover: result differences detected (0.00, 34.00, 48.00, 7.00).
- edit prediction then complete (edit+completion): result differences detected (0.00, 23.00).
- edit tokenizer then hover (edit+hover): result differences detected (0.00, 30.00, 43.00, 7.00).

## Benchmark: web

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 841.19 | 1.83 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 5784.39 | 8.06 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | no | 1399.23 | 10.38 | 5 | 25 | 80% | 1 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 4992.06 | 70.64 | 5 | 25 | 100% | 0 |

### request args completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 5.03 | 9.86 | 100% | 16.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 5.79 | 9.36 | 100% | 441.00 | +425.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 23.63 | 30.13 | 100% | 1.00 | -15.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 45.06 | 156.14 | 100% | 351.40 | +335.40 | pass |

### client session hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.19 | 0.20 | 100% | 7.00 | -19.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 0.48 | 0.57 | 100% | 26.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 3.43 | 11.02 | 100% | 314.00 | +288.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 25.37 | 44.85 | 100% | 359.00 | +333.00 | pass |

### client references

Method: `textDocument/references`

| Server | Success | Mean ms | P95 ms | Non-empty % | References found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.35 | 0.36 | 100% | 2.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.42 | 0.48 | 100% | 2.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 0.69 | 0.76 | 100% | 2.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 24.72 | 39.57 | 100% | 2.00 | 0.00 | pass |

### edit response then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 2.10 | 2.28 | 100% | 227.00 | +22.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | no | 2.83 | 4.49 | 0% | 0.00 | -205.00 | fail (10) |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 4.98 | 7.23 | 100% | 205.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 97.23 | 130.52 | 100% | 56.00 | -149.00 | pass |

### edit response then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260323T194605Z.json) | yes | 0.21 | 0.23 | 100% | 31.00 | -731.00 | pass |
| [Ty](latest-results/ty-20260323T194605Z.json) | yes | 0.65 | 0.67 | 100% | 304.00 | -458.00 | pass |
| [Pyright](latest-results/pyright-20260323T194605Z.json) | yes | 29.11 | 32.95 | 100% | 762.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260323T194605Z.json) | yes | 182.24 | 185.52 | 100% | 257.00 | -505.00 | pass |

### Result Differences

- request args completion: result differences detected (1.00, 16.00, 351.40, 441.00).
- client session hover: result differences detected (26.00, 314.00, 359.00, 7.00).
- edit response then complete (edit+completion): result differences detected (0.00, 205.00, 227.00, 56.00).
- edit response then hover (edit+hover): result differences detected (257.00, 304.00, 31.00, 762.00).
