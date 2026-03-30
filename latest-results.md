# Python LSP Benchmark Comparison

Generated from `results/bench-servers/summary-20260330T063249Z.json`

- Generated at: 20260330T063249Z
- Config: `github-releases`
- Servers: pyright, ty, pyrefly, pylsp-mypy
- Baseline server: Pyright (pyright)
- Benchmarks: data_science, django, pandas, sqlalchemy, transformers, web

## Server Versions

| Server | Version | Source |
| --- | --- | --- |
| Pyright | 1.1.408 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/pyright/1.1.408/package/dist/pyright-langserver.js |
| Ty | 0.0.26 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/ty/0.0.26/ty-x86_64-unknown-linux-gnu/ty |
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
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 6 | 6701.66 | 3.20 | 150 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | no | 6 | 10446.62 | 23.41 | 150 | 90% | 2 |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 6 | 85140.94 | 60.00 | 150 | 97% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | no | 6 | 250462.15 | 584.95 | 150 | 80% | 5 |

*Wall clock ms includes server startup, warmup iterations, and shutdown — not just measured requests.*

## Benchmark: data_science

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 979.62 | 4.12 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 1494.68 | 14.67 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 14189.85 | 48.64 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | no | 8092.01 | 90.36 | 5 | 25 | 80% | 1 |

### dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 1.58 | 1.82 | 100% | 225.00 | +24.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 5.40 | 8.90 | 100% | 201.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 44.39 | 175.40 | 100% | 250.00 | +49.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 49.23 | 74.41 | 100% | 181.00 | -20.00 | pass |

### dataframe describe hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.27 | 0.29 | 100% | 3908.00 | -111.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 1.05 | 1.10 | 100% | 4019.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 4.23 | 12.61 | 100% | 8341.00 | +4322.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 203.72 | 241.47 | 100% | 4134.00 | +115.00 | pass |

### summarize definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.22 | 0.22 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 0.42 | 0.46 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.52 | 1.33 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 1.00 | 1.02 | 100% | 1.00 | 0.00 | pass |

### edit array then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | no | 4.66 | 4.77 | 0% | 0.00 | -169.00 | fail (10) |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 16.65 | 17.29 | 100% | 167.00 | -2.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 23.91 | 36.49 | 100% | 149.00 | -20.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 209.42 | 302.32 | 100% | 169.00 | 0.00 | pass |

### edit array then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.32 | 0.42 | 100% | 354.00 | +76.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 1.86 | 1.87 | 100% | 376.00 | +98.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 26.90 | 28.38 | 100% | 278.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 193.19 | 225.62 | 100% | 5644.00 | +5366.00 | pass |

### Result Differences

- dataframe completion: result differences detected (181.00, 201.00, 225.00, 250.00).
- dataframe describe hover: result differences detected (3908.00, 4019.00, 4134.00, 8341.00).
- edit array then complete (edit+completion): result differences detected (0.00, 149.00, 167.00, 169.00).
- edit array then hover (edit+hover): result differences detected (278.00, 354.00, 376.00, 5644.00).

## Benchmark: django

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 704.28 | 1.93 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 845.91 | 6.58 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 6889.23 | 14.45 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 8328.42 | 171.70 | 5 | 25 | 100% | 0 |

### queryset completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 4.84 | 7.10 | 100% | 10.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 5.07 | 8.46 | 100% | 254.00 | +244.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 29.70 | 117.50 | 100% | 38.00 | +28.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 207.78 | 607.24 | 100% | 2.00 | -8.00 | pass |

### queryset filter hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.22 | 0.23 | 100% | 298.00 | +241.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.24 | 0.28 | 100% | 46.00 | -11.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 0.53 | 0.58 | 100% | 57.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 171.00 | 173.15 | 100% | 57.00 | 0.00 | pass |

### model definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.20 | 0.20 | 100% | 1.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.21 | 0.21 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 0.43 | 0.47 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 1.08 | 1.16 | 100% | 1.00 | 0.00 | pass |

### edit queryset then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 2.52 | 5.75 | 100% | 83.00 | -22.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 2.69 | 2.80 | 100% | 104.00 | -1.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 23.90 | 26.12 | 100% | 105.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 279.54 | 282.23 | 100% | 143.00 | +38.00 | pass |

### edit queryset then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.24 | 0.27 | 100% | 144.00 | +61.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 1.43 | 1.47 | 100% | 100.00 | +17.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 42.54 | 47.10 | 100% | 83.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 199.12 | 200.51 | 100% | 71.00 | -12.00 | pass |

### Result Differences

- queryset completion: result differences detected (10.00, 2.00, 254.00, 38.00).
- queryset filter hover: result differences detected (298.00, 46.00, 57.00).
- edit queryset then complete (edit+completion): result differences detected (104.00, 105.00, 143.00, 83.00).
- edit queryset then hover (edit+hover): result differences detected (100.00, 144.00, 71.00, 83.00).

## Benchmark: pandas

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 1291.55 | 6.02 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 1372.95 | 16.40 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 18284.15 | 114.76 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 8223.14 | 146.99 | 5 | 25 | 100% | 0 |

### report dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 16.56 | 20.71 | 100% | 1000.00 | +725.80 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 52.65 | 208.83 | 100% | 39.00 | -235.20 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 76.72 | 261.24 | 100% | 274.20 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 125.11 | 350.34 | 100% | 6.00 | -268.20 | pass |

### dataframe groupby hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.28 | 0.31 | 100% | 308.00 | -42.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 0.66 | 0.76 | 100% | 350.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 1.86 | 1.97 | 100% | 3120.00 | +2770.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 201.72 | 205.73 | 100% | 301.00 | -49.00 | pass |

### build report definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.22 | 0.24 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 0.45 | 0.51 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.55 | 1.59 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 1.10 | 1.23 | 100% | 1.00 | 0.00 | pass |

### edit dataframe then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 11.65 | 12.55 | 100% | 448.00 | +7.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 26.67 | 52.38 | 100% | 256.00 | -185.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 214.33 | 217.03 | 100% | 442.00 | +1.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 484.90 | 916.34 | 100% | 441.00 | 0.00 | pass |

### edit dataframe then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.28 | 0.31 | 100% | 328.00 | -3964.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 1.36 | 1.40 | 100% | 281.00 | -4011.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 11.09 | 13.11 | 100% | 4292.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 192.69 | 193.86 | 100% | 232.00 | -4060.00 | pass |

### Result Differences

- report dataframe completion: result differences detected (1000.00, 274.20, 39.00, 6.00).
- dataframe groupby hover: result differences detected (301.00, 308.00, 3120.00, 350.00).
- edit dataframe then complete (edit+completion): result differences detected (256.00, 441.00, 442.00, 448.00).
- edit dataframe then hover (edit+hover): result differences detected (232.00, 281.00, 328.00, 4292.00).

## Benchmark: sqlalchemy

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 796.24 | 1.69 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | no | 1417.37 | 18.40 | 5 | 25 | 80% | 1 |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 8092.37 | 44.65 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | no | 7419.77 | 93.07 | 5 | 25 | 60% | 2 |

### query completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 4.22 | 10.40 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 6.34 | 11.85 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 66.29 | 112.39 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 83.87 | 331.62 | 100% | 38.00 | +37.00 | pass |

### sessionmaker hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.37 | 0.39 | 100% | 10580.00 | +8.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.78 | 0.92 | 100% | 13682.00 | +3110.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 1.47 | 1.74 | 100% | 10572.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 343.50 | 382.94 | 100% | 10498.00 | -74.00 | pass |

### mapped class definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.20 | 0.23 | 100% | 2.00 | +1.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.23 | 0.28 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 0.38 | 0.43 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 1.05 | 1.09 | 100% | 1.00 | 0.00 | pass |

### edit query then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 2.03 | 2.14 | 100% | 23.00 | -16.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 6.92 | 10.29 | 100% | 17.00 | -22.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | no | 28.39 | 29.38 | 0% | 0.00 | -39.00 | fail (10) |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 132.71 | 191.61 | 100% | 39.00 | 0.00 | pass |

### edit session then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | no | 0.22 | 0.24 | 0% | 0.00 | -900.00 | fail (10) |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 1.63 | 1.65 | 100% | 304.00 | -596.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | no | 26.13 | 26.28 | 0% | 0.00 | -900.00 | fail (10) |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 82.35 | 92.10 | 100% | 900.00 | 0.00 | pass |

### Result Differences

- query completion: result differences detected (1.00, 38.00).
- sessionmaker hover: result differences detected (10498.00, 10572.00, 10580.00, 13682.00).
- mapped class definition: result differences detected (1.00, 2.00).
- edit query then complete (edit+completion): result differences detected (0.00, 17.00, 23.00, 39.00).
- edit session then hover (edit+hover): result differences detected (0.00, 304.00, 900.00).

## Benchmark: transformers

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 2120.25 | 3.52 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 3947.44 | 73.14 | 5 | 25 | 80% | 0 |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 32220.21 | 129.62 | 5 | 25 | 80% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | no | 213595.04 | 2939.59 | 5 | 25 | 40% | 2 |

### classifier pipeline completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 11.19 | 13.43 | 100% | 767.00 | +644.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 51.42 | 87.49 | 100% | 123.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 139.11 | 145.74 | 100% | 2.00 | -121.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 336.13 | 1343.12 | 100% | 38.00 | -85.00 | pass |

### pipeline hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.21 | 0.23 | 100% | 7.00 | -27.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.23 | 0.24 | 100% | 48.00 | +14.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 0.45 | 0.55 | 100% | 34.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | no | 2542.40 | 2594.95 | 0% | 0.00 | -34.00 | fail (10) |

### auto tokenizer definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.25 | 0.27 | 100% | 1.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.25 | 0.28 | 100% | 1.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 0.89 | 2.39 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 2226.82 | 2306.88 | 100% | 1.00 | 0.00 | pass |

### edit prediction then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 2.63 | 3.17 | 0% | 0.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 3.13 | 3.36 | 100% | 23.00 | +23.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 6.07 | 6.77 | 0% | 0.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 26.51 | 87.33 | 0% | 0.00 | 0.00 | pass |

### edit tokenizer then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 2.59 | 3.85 | 100% | 43.00 | +13.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 2.80 | 2.93 | 100% | 7.00 | -23.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 589.28 | 607.58 | 100% | 30.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | no | 9786.99 | 9936.82 | 0% | 0.00 | -30.00 | fail (10) |

### Result Differences

- classifier pipeline completion: result differences detected (123.00, 2.00, 38.00, 767.00).
- pipeline hover: result differences detected (0.00, 34.00, 48.00, 7.00).
- edit prediction then complete (edit+completion): result differences detected (0.00, 23.00).
- edit tokenizer then hover (edit+hover): result differences detected (0.00, 30.00, 43.00, 7.00).

## Benchmark: web

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 809.72 | 1.90 | 5 | 25 | 100% | 0 |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 5465.13 | 7.89 | 5 | 25 | 100% | 0 |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | no | 1368.27 | 11.24 | 5 | 25 | 80% | 1 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 4803.76 | 68.01 | 5 | 25 | 100% | 0 |

### request args completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 5.29 | 9.75 | 100% | 16.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 5.80 | 9.77 | 100% | 441.00 | +425.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 22.20 | 26.51 | 100% | 1.00 | -15.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 51.97 | 185.62 | 100% | 351.40 | +335.40 | pass |

### client session hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.21 | 0.23 | 100% | 7.00 | -19.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 0.57 | 0.68 | 100% | 26.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 3.29 | 10.57 | 100% | 314.00 | +288.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 16.87 | 26.94 | 100% | 359.00 | +333.00 | pass |

### client references

Method: `textDocument/references`

| Server | Success | Mean ms | P95 ms | Non-empty % | References found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.35 | 0.37 | 100% | 2.00 | 0.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.45 | 0.54 | 100% | 2.00 | 0.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 0.86 | 0.94 | 100% | 2.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 17.20 | 36.67 | 100% | 2.00 | 0.00 | pass |

### edit response then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | no | 0.38 | 0.41 | 0% | 0.00 | -205.00 | fail (10) |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 2.27 | 2.42 | 100% | 227.00 | +22.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 3.84 | 5.13 | 100% | 205.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 107.63 | 166.08 | 100% | 56.00 | -149.00 | pass |

### edit response then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyright | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260330T063249Z.json) | yes | 0.21 | 0.22 | 100% | 31.00 | -731.00 | pass |
| [Ty](latest-results/ty-20260330T063249Z.json) | yes | 0.78 | 0.83 | 100% | 304.00 | -458.00 | pass |
| [Pyright](latest-results/pyright-20260330T063249Z.json) | yes | 28.90 | 31.87 | 100% | 762.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260330T063249Z.json) | yes | 176.16 | 176.90 | 100% | 257.00 | -505.00 | pass |

### Result Differences

- request args completion: result differences detected (1.00, 16.00, 351.40, 441.00).
- client session hover: result differences detected (26.00, 314.00, 359.00, 7.00).
- edit response then complete (edit+completion): result differences detected (0.00, 205.00, 227.00, 56.00).
- edit response then hover (edit+hover): result differences detected (257.00, 304.00, 31.00, 762.00).
