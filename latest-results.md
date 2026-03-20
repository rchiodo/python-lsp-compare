# Python LSP Benchmark Comparison

Generated from `results\bench-servers\summary-20260320T002319Z.json`

- Generated at: 20260320T002319Z
- Config: `C:\Users\rchiodo\source\repos\python-lsp-compare\configs\local\lsp_servers.json`
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
| Pylance | no | 6 | 24333.98 | 26.00 | 85 | 100% | 0 |
| Ty | no | 6 | 6239.37 | 2.65 | 90 | 100% | 1 |
| Pyrefly | no | 6 | 17850.73 | 5.56 | 90 | 83% | 3 |

## Benchmark: data_science

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pylance | yes | 2309.79 | 21.12 | 3 | 15 | 100% | 0 |
| Ty | yes | 391.18 | 0.86 | 3 | 15 | 100% | 0 |
| Pyrefly | no | 1765.80 | 3.57 | 3 | 15 | 67% | 1 |

### dataframe completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 13.51 | 16.01 | 100% | 203.00 | 0.00 | pass |
| Ty | yes | 2.05 | 2.33 | 100% | 226.00 | +23.00 | pass |
| Pyrefly | yes | 0.74 | 0.83 | 100% | 252.00 | +49.00 | pass |

### dataframe describe hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 49.04 | 56.91 | 100% | 4118.00 | 0.00 | pass |
| Ty | yes | 0.32 | 0.33 | 100% | 3908.00 | -210.00 | pass |
| Pyrefly | yes | 9.61 | 28.91 | 100% | 4417.00 | +299.00 | pass |

### module symbols

Method: `textDocument/documentSymbol`

| Server | Success | Mean ms | P95 ms | Non-empty % | Symbols found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 0.82 | 0.99 | 100% | 5.00 | 0.00 | pass |
| Ty | yes | 0.21 | 0.22 | 100% | 2.00 | -3.00 | pass |
| Pyrefly | no | 0.35 | 0.39 | 0% | 0.00 | -5.00 | fail (10) |

### Result Differences

- dataframe completion: result differences detected (203.00, 226.00, 252.00).
- dataframe describe hover: result differences detected (3908.00, 4118.00, 4417.00).
- module symbols: result differences detected (0.00, 2.00, 5.00).

## Benchmark: django

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pylance | yes | 1444.84 | 19.00 | 3 | 15 | 100% | 0 |
| Ty | yes | 570.49 | 4.22 | 3 | 15 | 100% | 0 |
| Pyrefly | yes | 1848.88 | 0.60 | 3 | 15 | 100% | 0 |

### queryset completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 54.92 | 92.21 | 100% | 16.00 | 0.00 | pass |
| Ty | yes | 11.98 | 17.94 | 100% | 237.00 | +221.00 | pass |
| Pyrefly | yes | 0.97 | 2.06 | 100% | 38.00 | +22.00 | pass |

### queryset filter hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 1.08 | 1.22 | 100% | 57.00 | 0.00 | pass |
| Ty | yes | 0.32 | 0.35 | 100% | 46.00 | -11.00 | pass |
| Pyrefly | yes | 0.45 | 0.53 | 100% | 324.00 | +267.00 | pass |

### model definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 1.00 | 1.34 | 100% | 1.00 | 0.00 | pass |
| Ty | yes | 0.37 | 0.40 | 100% | 1.00 | 0.00 | pass |
| Pyrefly | yes | 0.36 | 0.39 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- queryset completion: result differences detected (16.00, 237.00, 38.00).
- queryset filter hover: result differences detected (324.00, 46.00, 57.00).

## Benchmark: pandas

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pylance | yes | 1937.01 | 5.56 | 3 | 15 | 100% | 0 |
| Ty | yes | 423.54 | 0.94 | 3 | 15 | 100% | 0 |
| Pyrefly | no | 2014.38 | 3.10 | 3 | 15 | 33% | 2 |

### series completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 14.04 | 18.54 | 100% | 203.00 | 0.00 | pass |
| Ty | yes | 2.13 | 2.57 | 100% | 226.00 | +23.00 | pass |
| Pyrefly | no | 0.24 | 0.27 | 0% | 0.00 | -203.00 | fail (10) |

### dataframe groupby hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 1.80 | 2.41 | 100% | 7371.00 | 0.00 | pass |
| Ty | yes | 0.40 | 0.58 | 100% | 308.00 | -7063.00 | pass |
| Pyrefly | yes | 8.71 | 26.50 | 100% | 3577.00 | -3794.00 | pass |

### module symbols

Method: `textDocument/documentSymbol`

| Server | Success | Mean ms | P95 ms | Non-empty % | Symbols found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 0.84 | 1.15 | 100% | 5.00 | 0.00 | pass |
| Ty | yes | 0.29 | 0.33 | 100% | 3.00 | -2.00 | pass |
| Pyrefly | no | 0.35 | 0.37 | 0% | 0.00 | -5.00 | fail (10) |

### Result Differences

- series completion: result differences detected (0.00, 203.00, 226.00).
- dataframe groupby hover: result differences detected (308.00, 3577.00, 7371.00).
- module symbols: result differences detected (0.00, 3.00, 5.00).

## Benchmark: sqlalchemy

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pylance | yes | 3914.52 | 83.34 | 3 | 15 | 100% | 0 |
| Ty | yes | 645.30 | 4.16 | 3 | 15 | 100% | 0 |
| Pyrefly | yes | 2393.05 | 0.80 | 3 | 15 | 100% | 0 |

### query completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 247.42 | 306.03 | 100% | 1.00 | 0.00 | pass |
| Ty | yes | 11.69 | 24.31 | 100% | 1.00 | 0.00 | pass |
| Pyrefly | yes | 0.88 | 1.92 | 100% | 38.00 | +37.00 | pass |

### sessionmaker hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 1.79 | 2.15 | 100% | 10572.00 | 0.00 | pass |
| Ty | yes | 0.49 | 0.54 | 100% | 10580.00 | +8.00 | pass |
| Pyrefly | yes | 1.10 | 1.19 | 100% | 13706.00 | +3134.00 | pass |

### mapped class definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 0.81 | 0.97 | 100% | 1.00 | 0.00 | pass |
| Ty | yes | 0.29 | 0.31 | 100% | 2.00 | +1.00 | pass |
| Pyrefly | yes | 0.40 | 0.45 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- query completion: result differences detected (1.00, 38.00).
- sessionmaker hover: result differences detected (10572.00, 10580.00, 13706.00).
- mapped class definition: result differences detected (1.00, 2.00).

## Benchmark: transformers

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pylance | no | 13281.56 | 5.47 | 3 | 10 | 100% | 0 |
| Ty | no | 3602.62 | 0.71 | 3 | 15 | 100% | 1 |
| Pyrefly | yes | 7685.07 | 19.56 | 3 | 15 | 100% | 0 |

### tokenizer factory completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | no | n/a | n/a | n/a | n/a | n/a | pass |
| Ty | no | 0.24 | 0.28 | n/a | n/a | n/a | fail (10) |
| Pyrefly | yes | 0.35 | 0.40 | 100% | 3.00 | n/a | pass |

### pipeline hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 9.99 | 13.23 | 100% | 39126.00 | 0.00 | pass |
| Ty | yes | 1.60 | 1.76 | 100% | 38387.00 | -739.00 | pass |
| Pyrefly | yes | 57.84 | 218.65 | 100% | 35605.00 | -3521.00 | pass |

### auto tokenizer definition

Method: `textDocument/definition`

| Server | Success | Mean ms | P95 ms | Non-empty % | Definitions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 0.96 | 1.13 | 100% | 1.00 | 0.00 | pass |
| Ty | yes | 0.29 | 0.31 | 100% | 1.00 | 0.00 | pass |
| Pyrefly | yes | 0.49 | 0.59 | 100% | 1.00 | 0.00 | pass |

### Result Differences

- pipeline hover: result differences detected (35605.00, 38387.00, 39126.00).

## Benchmark: web

| Server | Success | Total ms | Avg measured ms | Points | Measured requests | Non-empty % | Failed points |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Pylance | yes | 1446.26 | 14.68 | 3 | 15 | 100% | 0 |
| Ty | yes | 606.25 | 5.00 | 3 | 15 | 100% | 0 |
| Pyrefly | yes | 2143.55 | 5.74 | 3 | 15 | 100% | 0 |

### request args completion

Method: `textDocument/completion`

| Server | Success | Mean ms | P95 ms | Non-empty % | Completions found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 41.98 | 65.57 | 100% | 12.00 | 0.00 | pass |
| Ty | yes | 14.07 | 19.20 | 100% | 437.00 | +425.00 | pass |
| Pyrefly | yes | 9.41 | 16.53 | 100% | 356.20 | +344.20 | pass |

### client session hover

Method: `textDocument/hover`

| Server | Success | Mean ms | P95 ms | Non-empty % | Hover length | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 0.90 | 1.19 | 100% | 26.00 | 0.00 | pass |
| Ty | yes | 0.25 | 0.28 | 100% | 7.00 | -19.00 | pass |
| Pyrefly | yes | 7.35 | 18.09 | 100% | 340.00 | +314.00 | pass |

### client references

Method: `textDocument/references`

| Server | Success | Mean ms | P95 ms | Non-empty % | References found | Delta vs Pylance | Validation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Pylance | yes | 1.16 | 1.73 | 100% | 2.00 | 0.00 | pass |
| Ty | yes | 0.66 | 0.78 | 100% | 2.00 | 0.00 | pass |
| Pyrefly | yes | 0.47 | 0.49 | 100% | 2.00 | 0.00 | pass |

### Result Differences

- request args completion: result differences detected (12.00, 356.20, 437.00).
- client session hover: result differences detected (26.00, 340.00, 7.00).
