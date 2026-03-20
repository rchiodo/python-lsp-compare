# Python LSP Benchmark Comparison

Generated from `results\bench-servers\summary-20260320T180038Z.json`

- Generated at: 20260320T180038Z
- Config: `C:\Users\rchiodo\source\repos\python-lsp-compare\.python-lsp-compare\lsp_servers.json`
- Servers: pylance, ty, pyrefly
- Baseline server: Pylance (pylance)
- Benchmarks: data_science, django, pandas, sqlalchemy, transformers, web

## Server Versions

| Server | Version | Commit | Source |
| --- | --- | --- | --- |
| Pylance | af14f3725d68 | af14f3725d68 | C:\Users\rchiodo\source\repos\pyrx\packages\pylance-server\dist\server.js |
| Ty | f9324a5bf669 | f9324a5bf669 | C:\Users\rchiodo\source\repos\ruff\target\release\ty.exe |
| Pyrefly | 54df45a1c642 | 54df45a1c642 | C:\Users\rchiodo\source\repos\pyrefly\target\release\pyrefly.exe |


## Overview

| Server | Success | Benchmarks | Total ms | Avg measured ms | Measured requests | Non-empty % | Failed points |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Pyrefly | yes | 6 | 17837.74 | 3.15 | 90 | 100% | 0 |
| Ty | yes | 6 | 8009.11 | 5.57 | 90 | 100% | 0 |
| Pylance | yes | 6 | 43391.68 | 195.65 | 90 | 100% | 0 |

## Benchmark: data_science

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ty | yes | 717.82 | 1.16 | 3 | 15 | 100% | 0 |
| Pyrefly | yes | 1997.60 | 3.79 | 3 | 15 | 100% | 0 |
| Pylance | yes | 2563.06 | 28.54 | 3 | 15 | 100% | 0 |

### dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.82 | 0.88 | 100% | 252.00 | +49.00 | pass |
| Ty | yes | 2.85 | 3.53 | 100% | 226.00 | +23.00 | pass |
| Pylance | yes | 17.92 | 21.97 | 100% | 203.00 | 0.00 | pass |

### dataframe describe hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.36 | 0.39 | 100% | 3908.00 | -210.00 | pass |
| Pyrefly | yes | 10.13 | 29.94 | 100% | 4417.00 | +299.00 | pass |
| Pylance | yes | 66.89 | 75.48 | 100% | 4118.00 | 0.00 | pass |

### summarize definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.29 | 0.32 | 100% | 1.00 | 0.00 | pass |
| Pyrefly | yes | 0.43 | 0.48 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 0.80 | 0.86 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- dataframe completion: result differences detected (203.00, 226.00, 252.00).
- dataframe describe hover: result differences detected (3908.00, 4118.00, 4417.00).

## Benchmark: django

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pyrefly | yes | 1612.57 | 0.40 | 3 | 15 | 100% | 0 |
| Ty | yes | 662.66 | 3.95 | 3 | 15 | 100% | 0 |
| Pylance | yes | 1602.67 | 23.60 | 3 | 15 | 100% | 0 |

### queryset completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.53 | 0.57 | 100% | 38.00 | +22.00 | pass |
| Ty | yes | 11.02 | 13.98 | 100% | 237.00 | +221.00 | pass |
| Pylance | yes | 68.06 | 117.90 | 100% | 16.00 | 0.00 | pass |

### queryset filter hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.37 | 0.45 | 100% | 324.00 | +267.00 | pass |
| Ty | yes | 0.51 | 0.76 | 100% | 46.00 | -11.00 | pass |
| Pylance | yes | 1.14 | 1.36 | 100% | 57.00 | 0.00 | pass |

### model definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.31 | 0.34 | 100% | 1.00 | 0.00 | pass |
| Ty | yes | 0.33 | 0.38 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 1.61 | 2.07 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- queryset completion: result differences detected (16.00, 237.00, 38.00).
- queryset filter hover: result differences detected (324.00, 46.00, 57.00).

## Benchmark: pandas

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pyrefly | yes | 2121.61 | 5.80 | 3 | 15 | 100% | 0 |
| Ty | yes | 1040.06 | 11.38 | 3 | 15 | 100% | 0 |
| Pylance | yes | 3087.37 | 80.74 | 3 | 15 | 100% | 0 |

### report dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.47 | 0.49 | 100% | 39.00 | -120.00 | pass |
| Ty | yes | 33.49 | 47.37 | 100% | 1000.00 | +841.00 | pass |
| Pylance | yes | 238.60 | 511.87 | 100% | 159.00 | 0.00 | pass |

### dataframe groupby hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.35 | 0.38 | 100% | 308.00 | -7063.00 | pass |
| Pylance | yes | 2.29 | 3.14 | 100% | 7371.00 | 0.00 | pass |
| Pyrefly | yes | 16.51 | 54.10 | 100% | 3577.00 | -3794.00 | pass |

### build report definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.28 | 0.31 | 100% | 1.00 | 0.00 | pass |
| Pyrefly | yes | 0.41 | 0.44 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 1.33 | 1.78 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- report dataframe completion: result differences detected (1000.00, 159.00, 39.00).
- dataframe groupby hover: result differences detected (308.00, 3577.00, 7371.00).

## Benchmark: sqlalchemy

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pyrefly | yes | 2461.50 | 1.15 | 3 | 15 | 100% | 0 |
| Ty | yes | 699.00 | 3.38 | 3 | 15 | 100% | 0 |
| Pylance | yes | 4109.45 | 92.59 | 3 | 15 | 100% | 0 |

### query completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.99 | 1.90 | 100% | 38.00 | +37.00 | pass |
| Ty | yes | 9.10 | 17.18 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 273.86 | 355.52 | 100% | 1.00 | 0.00 | pass |

### sessionmaker hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.51 | 0.55 | 100% | 10580.00 | +8.00 | pass |
| Pyrefly | yes | 1.12 | 1.21 | 100% | 13706.00 | +3134.00 | pass |
| Pylance | yes | 3.02 | 3.80 | 100% | 10572.00 | 0.00 | pass |

### mapped class definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.54 | 0.68 | 100% | 2.00 | +1.00 | pass |
| Pylance | yes | 0.88 | 1.02 | 100% | 1.00 | 0.00 | pass |
| Pyrefly | yes | 1.34 | 3.58 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- query completion: result differences detected (1.00, 38.00).
- sessionmaker hover: result differences detected (10572.00, 10580.00, 13706.00).
- mapped class definition: result differences detected (1.00, 2.00).

## Benchmark: transformers

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pyrefly | yes | 7311.32 | 0.48 | 3 | 15 | 100% | 0 |
| Ty | yes | 4200.36 | 9.42 | 3 | 15 | 100% | 0 |
| Pylance | yes | 30430.23 | 928.73 | 3 | 15 | 100% | 0 |

### classifier pipeline completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.50 | 0.52 | 100% | 38.00 | -46.00 | pass |
| Ty | yes | 27.31 | 30.26 | 100% | 767.00 | +683.00 | pass |
| Pylance | yes | 2783.43 | 3333.16 | 100% | 84.00 | 0.00 | pass |

### pipeline hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.30 | 0.32 | 100% | 7.00 | -27.00 | pass |
| Pyrefly | yes | 0.32 | 0.35 | 100% | 48.00 | +14.00 | pass |
| Pylance | yes | 1.87 | 2.27 | 100% | 34.00 | 0.00 | pass |

### auto tokenizer definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pyrefly | yes | 0.61 | 0.67 | 100% | 1.00 | 0.00 | pass |
| Ty | yes | 0.64 | 0.75 | 100% | 1.00 | 0.00 | pass |
| Pylance | yes | 0.89 | 1.16 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- classifier pipeline completion: result differences detected (38.00, 767.00, 84.00).
- pipeline hover: result differences detected (34.00, 48.00, 7.00).

## Benchmark: web

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ty | yes | 689.20 | 4.13 | 3 | 15 | 100% | 0 |
| Pyrefly | yes | 2333.14 | 7.32 | 3 | 15 | 100% | 0 |
| Pylance | yes | 1598.90 | 19.67 | 3 | 15 | 100% | 0 |

### request args completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 11.49 | 16.73 | 100% | 439.00 | +427.00 | pass |
| Pyrefly | yes | 11.56 | 19.36 | 100% | 356.20 | +344.20 | pass |
| Pylance | yes | 56.56 | 92.76 | 100% | 12.00 | 0.00 | pass |

### client session hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.32 | 0.37 | 100% | 7.00 | -19.00 | pass |
| Pylance | yes | 1.43 | 2.81 | 100% | 26.00 | 0.00 | pass |
| Pyrefly | yes | 9.28 | 24.13 | 100% | 340.00 | +314.00 | pass |

### client references

Method: `textDocument/references`

| Server | Success | Mean ms | P95 ms | Non-empty % | References found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Ty | yes | 0.59 | 0.72 | 100% | 2.00 | 0.00 | pass |
| Pylance | yes | 1.03 | 1.20 | 100% | 2.00 | 0.00 | pass |
| Pyrefly | yes | 1.11 | 1.34 | 100% | 2.00 | 0.00 | pass |

### Result Differences

- request args completion: result differences detected (12.00, 356.20, 439.00).
- client session hover: result differences detected (26.00, 340.00, 7.00).
