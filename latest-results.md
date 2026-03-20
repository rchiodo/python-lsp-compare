# Python LSP Benchmark Comparison

Generated from `results\bench-servers\summary-20260320T172613Z.json`

- Generated at: 20260320T172613Z
- Config: `C:\Users\rchiodo\source\repos\python-lsp-compare\.python-lsp-compare\lsp_servers.json`
- Servers: pylance, ty, pyrefly
- Baseline server: Pylance (pylance)
- Benchmarks: data_science, django, pandas, sqlalchemy, transformers, web

## Server Versions

| Server | Version | Commit | Source |
| --- | --- | --- | --- |
| Pylance | af14f3725d68 | af14f3725d68 | C:\Users\rchiodo\source\repos\pyrx\packages\pylance-server\dist\server.js |
| Ty | af14f3725d68 | af14f3725d68 | C:\Users\rchiodo\source\repos\pyrx\packages\ruff\target\release\ty.exe |
| Pyrefly | 54df45a1c642 | 54df45a1c642 | C:\Users\rchiodo\source\repos\pyrefly\target\release\pyrefly.exe |


## Overview

| Server | Success | Benchmarks | Total ms | Avg measured ms | Measured requests | Non-empty % | Failed points |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Pyrefly | yes | 6 | 18396.09 | 1.97 | 90 | 100% | 0 |
| Ty | yes | 6 | 7390.26 | 5.59 | 90 | 100% | 0 |
| Pylance | yes | 6 | 43388.42 | 189.91 | 90 | 100% | 0 |

## Benchmark: data_science

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ty | yes | 442.47 | 0.93 | 3 | 15 | 100% | 0 |
| Pyrefly | yes | 2432.31 | 1.33 | 3 | 15 | 100% | 0 |
| Pylance | yes | 2283.85 | 20.90 | 3 | 15 | 100% | 0 |

### dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 1.40 | 2.39 | 100% | 252.00 | +49.00 | pass |
| Ty | yes | 2.14 | 2.36 | 100% | 226.00 | +23.00 | pass |
| Pylance | yes | 13.66 | 16.68 | 100% | 203.00 | 0.00 | pass |

### dataframe describe hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.35 | 0.38 | 100% | 3908.00 | -210.00 | pass |
| Pyrefly | yes | 2.24 | 2.49 | 100% | 4417.00 | +299.00 | pass |
| Pylance | yes | 48.20 | 52.57 | 100% | 4118.00 | 0.00 | pass |

### summarize definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.30 | 0.33 | 100% | 1.00 | 0.00 | pass |
| Pyrefly | yes | 0.34 | 0.37 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 0.83 | 0.90 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- dataframe completion: result differences detected (203.00, 226.00, 252.00).
- dataframe describe hover: result differences detected (3908.00, 4118.00, 4417.00).

## Benchmark: django

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pyrefly | yes | 1801.85 | 0.58 | 3 | 15 | 100% | 0 |
| Ty | yes | 597.04 | 6.31 | 3 | 15 | 100% | 0 |
| Pylance | yes | 1442.09 | 19.30 | 3 | 15 | 100% | 0 |

### queryset completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.83 | 1.64 | 100% | 38.00 | +22.00 | pass |
| Ty | yes | 18.35 | 23.35 | 100% | 237.00 | +221.00 | pass |
| Pylance | yes | 55.92 | 95.72 | 100% | 16.00 | 0.00 | pass |

### queryset filter hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.30 | 0.33 | 100% | 46.00 | -11.00 | pass |
| Pyrefly | yes | 0.50 | 0.55 | 100% | 324.00 | +267.00 | pass |
| Pylance | yes | 1.15 | 1.50 | 100% | 57.00 | 0.00 | pass |

### model definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.28 | 0.30 | 100% | 1.00 | 0.00 | pass |
| Pyrefly | yes | 0.43 | 0.50 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 0.83 | 1.05 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- queryset completion: result differences detected (16.00, 237.00, 38.00).
- queryset filter hover: result differences detected (324.00, 46.00, 57.00).

## Benchmark: pandas

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pyrefly | yes | 1995.41 | 3.50 | 3 | 15 | 100% | 0 |
| Ty | yes | 898.91 | 9.97 | 3 | 15 | 100% | 0 |
| Pylance | yes | 2783.74 | 67.90 | 3 | 15 | 100% | 0 |

### report dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.49 | 0.53 | 100% | 39.00 | -120.00 | pass |
| Ty | yes | 29.30 | 34.74 | 100% | 1000.00 | +841.00 | pass |
| Pylance | yes | 200.96 | 473.34 | 100% | 159.00 | 0.00 | pass |

### dataframe groupby hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.35 | 0.37 | 100% | 308.00 | -7063.00 | pass |
| Pylance | yes | 1.95 | 2.42 | 100% | 7371.00 | 0.00 | pass |
| Pyrefly | yes | 9.59 | 28.21 | 100% | 3577.00 | -3794.00 | pass |

### build report definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.26 | 0.26 | 100% | 1.00 | 0.00 | pass |
| Pyrefly | yes | 0.43 | 0.57 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 0.80 | 0.87 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- report dataframe completion: result differences detected (1000.00, 159.00, 39.00).
- dataframe groupby hover: result differences detected (308.00, 3577.00, 7371.00).

## Benchmark: sqlalchemy

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pyrefly | yes | 2403.98 | 0.87 | 3 | 15 | 100% | 0 |
| Ty | yes | 640.08 | 4.20 | 3 | 15 | 100% | 0 |
| Pylance | yes | 4025.94 | 86.99 | 3 | 15 | 100% | 0 |

### query completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.94 | 1.78 | 100% | 38.00 | +37.00 | pass |
| Ty | yes | 11.79 | 16.41 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 257.21 | 306.69 | 100% | 1.00 | 0.00 | pass |

### sessionmaker hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.50 | 0.56 | 100% | 10580.00 | +8.00 | pass |
| Pyrefly | yes | 1.20 | 1.34 | 100% | 13706.00 | +3134.00 | pass |
| Pylance | yes | 2.66 | 3.30 | 100% | 10572.00 | 0.00 | pass |

### mapped class definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.29 | 0.32 | 100% | 2.00 | +1.00 | pass |
| Pyrefly | yes | 0.45 | 0.52 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 1.10 | 1.35 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- query completion: result differences detected (1.00, 38.00).
- sessionmaker hover: result differences detected (10572.00, 10580.00, 13706.00).
- mapped class definition: result differences detected (1.00, 2.00).

## Benchmark: transformers

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pyrefly | yes | 7414.10 | 0.51 | 3 | 15 | 100% | 0 |
| Ty | yes | 4217.50 | 8.20 | 3 | 15 | 100% | 0 |
| Pylance | yes | 31377.77 | 929.46 | 3 | 15 | 100% | 0 |

### classifier pipeline completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.91 | 2.04 | 100% | 38.00 | -46.00 | pass |
| Ty | yes | 23.86 | 25.77 | 100% | 767.00 | +683.00 | pass |
| Pylance | yes | 2785.70 | 3423.90 | 100% | 84.00 | 0.00 | pass |

### pipeline hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.30 | 0.37 | 100% | 48.00 | +14.00 | pass |
| Ty | yes | 0.35 | 0.38 | 100% | 7.00 | -27.00 | pass |
| Pylance | yes | 0.92 | 1.06 | 100% | 34.00 | 0.00 | pass |

### auto tokenizer definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.31 | 0.34 | 100% | 1.00 | 0.00 | pass |
| Ty | yes | 0.40 | 0.47 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 1.75 | 3.91 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- classifier pipeline completion: result differences detected (38.00, 767.00, 84.00).
- pipeline hover: result differences detected (34.00, 48.00, 7.00).

## Benchmark: web

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ty | yes | 594.26 | 3.95 | 3 | 15 | 100% | 0 |
| Pyrefly | yes | 2348.43 | 5.05 | 3 | 15 | 100% | 0 |
| Pylance | yes | 1475.02 | 14.93 | 3 | 15 | 100% | 0 |

### request args completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 6.96 | 7.85 | 100% | 357.00 | +345.00 | pass |
| Ty | yes | 10.96 | 17.35 | 100% | 439.00 | +427.00 | pass |
| Pylance | yes | 40.85 | 60.83 | 100% | 12.00 | 0.00 | pass |

### client session hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.28 | 0.30 | 100% | 7.00 | -19.00 | pass |
| Pylance | yes | 1.62 | 3.02 | 100% | 26.00 | 0.00 | pass |
| Pyrefly | yes | 7.64 | 18.71 | 100% | 340.00 | +314.00 | pass |

### client references

Method: `textDocument/references`

| Server | Success | Mean ms | P95 ms | Non-empty % | References found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.54 | 0.63 | 100% | 2.00 | 0.00 | pass |
| Ty | yes | 0.60 | 0.77 | 100% | 2.00 | 0.00 | pass |
| Pylance | yes | 2.33 | 5.02 | 100% | 2.00 | 0.00 | pass |

### Result Differences

- request args completion: result differences detected (12.00, 357.00, 439.00).
- client session hover: result differences detected (26.00, 340.00, 7.00).
