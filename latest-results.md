# Python LSP Benchmark Comparison

Generated from `results/bench-servers/summary-20260408T175301Z.json`

- Generated at: 20260408T175301Z
- Config: `github-releases`
- Servers: pyrefly, pylsp-mypy
- Baseline server: Pyrefly (pyrefly)
- Benchmarks: data_science, django, pandas, sqlalchemy, transformers, web

## Server Versions

| Server | Version | Source |
| --- | --- | --- |
| Pyrefly | 0.60.0 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/pyrefly/venv/bin/pyrefly |
| pylsp-mypy | 1.14.0 | /home/runner/work/python-lsp-compare/python-lsp-compare/.python-lsp-compare/servers/pylsp-mypy/venv/bin/pylsp |

## Server Notes

- **Pyrefly**: Installed from PyPI into an isolated venv because GitHub release binaries are no longer published.
- **pylsp-mypy**: Uses python-lsp-server (pylsp) with the pylsp-mypy plugin.
- **pylsp-mypy**: LSP features like hover and completion are provided by pylsp/jedi, not mypy.
- **pylsp-mypy**: mypy contributes diagnostics only.


## Overview

| Server | Success | Benchmarks | Wall clock ms | Avg measured ms | Measured requests | Non-empty % | Failed points |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 6 | 60147.24 | 26.41 | 150 | 97% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | no | 6 | 213042.35 | 349.47 | 150 | 80% | 5 |

*Wall clock ms includes server startup, warmup iterations, and shutdown — not just measured requests.*

## Benchmark: data_science

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 11788.41 | 16.55 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | no | 8038.14 | 94.77 | 5 | 25 | 80% | 1 |

### dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 42.75 | 168.80 | 100% | 250.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 84.70 | 118.49 | 100% | 181.00 | -69.00 | pass |

### dataframe describe hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 8.80 | 18.53 | 100% | 3604.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 197.33 | 199.91 | 100% | 4134.00 | +530.00 | pass |

### summarize definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 1.04 | 1.07 | 100% | 1.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 1.14 | 2.76 | 100% | 1.00 | 0.00 | pass |

### edit array then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | no | 4.46 | 4.78 | 0% | 0.00 | -149.00 | fail (10) |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 29.16 | 33.96 | 100% | 149.00 | 0.00 | pass |

### edit array then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 0.90 | 1.03 | 100% | 2075.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 186.34 | 188.09 | 100% | 5644.00 | +3569.00 | pass |

### Result Differences

- dataframe completion: result differences detected (181.00, 250.00).
- dataframe describe hover: result differences detected (3604.00, 4134.00).
- edit array then complete (edit+completion): result differences detected (0.00, 149.00).
- edit array then hover (edit+hover): result differences detected (2075.00, 5644.00).

## Benchmark: django

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 5985.52 | 6.65 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 8548.60 | 179.95 | 5 | 25 | 100% | 0 |

### queryset completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 28.01 | 110.83 | 100% | 38.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 202.64 | 644.80 | 100% | 2.00 | -36.00 | pass |

### queryset filter hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 0.27 | 0.33 | 100% | 298.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 178.63 | 180.85 | 100% | 57.00 | -241.00 | pass |

### model definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 0.27 | 0.29 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 1.08 | 1.10 | 100% | 1.00 | 0.00 | pass |

### edit queryset then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 1.38 | 1.48 | 100% | 83.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 307.44 | 358.44 | 100% | 143.00 | +60.00 | pass |

### edit queryset then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 3.32 | 5.31 | 100% | 1190.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 209.93 | 216.33 | 100% | 71.00 | -1119.00 | pass |

### Result Differences

- queryset completion: result differences detected (2.00, 38.00).
- queryset filter hover: result differences detected (298.00, 57.00).
- edit queryset then complete (edit+completion): result differences detected (143.00, 83.00).
- edit queryset then hover (edit+hover): result differences detected (1190.00, 71.00).

## Benchmark: pandas

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 11756.35 | 20.23 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 8567.04 | 148.35 | 5 | 25 | 100% | 0 |

### report dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 46.89 | 185.99 | 100% | 39.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 91.77 | 275.17 | 100% | 6.00 | -33.00 | pass |

### dataframe groupby hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 2.05 | 2.23 | 100% | 3120.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 209.56 | 211.55 | 100% | 301.00 | -2819.00 | pass |

### build report definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 0.21 | 0.23 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 1.81 | 1.94 | 100% | 1.00 | 0.00 | pass |

### edit dataframe then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 42.07 | 55.17 | 100% | 256.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 235.66 | 239.53 | 100% | 442.00 | +186.00 | pass |

### edit dataframe then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 9.94 | 16.16 | 100% | 2481.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 202.95 | 205.25 | 100% | 232.00 | -2249.00 | pass |

### Result Differences

- report dataframe completion: result differences detected (39.00, 6.00).
- dataframe groupby hover: result differences detected (301.00, 3120.00).
- edit dataframe then complete (edit+completion): result differences detected (256.00, 442.00).
- edit dataframe then hover (edit+hover): result differences detected (232.00, 2481.00).

## Benchmark: sqlalchemy

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 5852.29 | 20.80 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | no | 7562.64 | 95.19 | 5 | 25 | 60% | 2 |

### query completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 71.52 | 116.17 | 100% | 1.00 | -37.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 86.82 | 344.35 | 100% | 38.00 | 0.00 | pass |

### sessionmaker hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 0.78 | 0.81 | 100% | 13682.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 343.20 | 351.13 | 100% | 10498.00 | -3184.00 | pass |

### mapped class definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 0.23 | 0.27 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 1.17 | 1.42 | 100% | 1.00 | 0.00 | pass |

### edit query then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 8.67 | 16.07 | 100% | 17.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | no | 30.37 | 30.86 | 0% | 0.00 | -17.00 | fail (10) |

### edit session then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 7.50 | 9.94 | 100% | 1689.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | no | 29.67 | 30.78 | 0% | 0.00 | -1689.00 | fail (10) |

### Result Differences

- query completion: result differences detected (1.00, 38.00).
- sessionmaker hover: result differences detected (10498.00, 13682.00).
- edit query then complete (edit+completion): result differences detected (0.00, 17.00).
- edit session then hover (edit+hover): result differences detected (0.00, 1689.00).

## Benchmark: transformers

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 19668.04 | 82.85 | 5 | 25 | 80% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | no | 175488.19 | 1510.01 | 5 | 25 | 40% | 2 |

### classifier pipeline completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 140.17 | 141.17 | 100% | 2.00 | -36.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 405.28 | 1619.90 | 100% | 38.00 | 0.00 | pass |

### pipeline hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 0.20 | 0.20 | 100% | 48.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | no | 2552.22 | 2596.86 | 0% | 0.00 | -48.00 | fail (10) |

### auto tokenizer definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 0.22 | 0.25 | 100% | 1.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 2252.05 | 2345.56 | 100% | 1.00 | 0.00 | pass |

### edit prediction then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 2.52 | 2.61 | 0% | 0.00 | 0.00 | pass |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 3.28 | 11.58 | 0% | 0.00 | 0.00 | pass |

### edit tokenizer then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 5.24 | 12.62 | 100% | 33.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | no | 2603.09 | 2652.71 | 0% | 0.00 | -33.00 | fail (10) |

### Result Differences

- classifier pipeline completion: result differences detected (2.00, 38.00).
- pipeline hover: result differences detected (0.00, 48.00).
- edit tokenizer then hover (edit+hover): result differences detected (0.00, 33.00).

## Benchmark: web

| Server | Success | Wall clock ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 5096.62 | 11.39 | 5 | 25 | 100% | 0 |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 4837.74 | 68.58 | 5 | 25 | 100% | 0 |

### request args completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 24.97 | 32.61 | 100% | 1.00 | -350.40 | pass |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 47.91 | 168.05 | 100% | 351.40 | 0.00 | pass |

### client session hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 4.17 | 11.46 | 100% | 314.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 20.85 | 43.03 | 100% | 359.00 | +45.00 | pass |

### client references

Method: `textDocument/references`

| Server | Success | Mean ms | P95 ms | Non-empty % | References found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 0.35 | 0.37 | 100% | 2.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 25.88 | 49.02 | 100% | 2.00 | 0.00 | pass |

### edit response then complete (edit+completion)

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 1.40 | 3.84 | 100% | 32.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 88.45 | 90.27 | 100% | 56.00 | +24.00 | pass |

### edit response then hover (edit+hover)

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pyrefly | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| [Pyrefly](latest-results/pyrefly-20260408T175301Z.json) | yes | 3.14 | 5.61 | 100% | 3486.00 | 0.00 | pass |
| [pylsp-mypy](latest-results/pylsp-mypy-20260408T175301Z.json) | yes | 182.75 | 184.62 | 100% | 257.00 | -3229.00 | pass |

### Result Differences

- request args completion: result differences detected (1.00, 351.40).
- client session hover: result differences detected (314.00, 359.00).
- edit response then complete (edit+completion): result differences detected (32.00, 56.00).
- edit response then hover (edit+hover): result differences detected (257.00, 3486.00).
