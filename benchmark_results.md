# Benchmark Results

This document contains the results of benchmarking AVL and B-Tree operations, including time and memory usage.

## Summary Table
| Size | AVL Insert (s) | AVL Insert (MB) | AVL Search (s) | AVL Search (MB) | AVL Delete (s) | AVL Delete (MB) | B-Tree Insert (s) | B-Tree Insert (MB) | B-Tree Search (s) | B-Tree Search (MB) | B-Tree Delete (s) | B-Tree Delete (MB) |
|------|----------------|-----------------|----------------|-----------------|----------------|-----------------|------------------|------------------|------------------|------------------|------------------|------------------|
| 1000 | 0.0063 | 0.0039 | 0.0001 | 0.0000 | 0.0015 | 0.0000 | 0.0080 | 0.1094 | 0.0008 | 0.0000 | 0.0003 | 0.0000 |
| 5000 | 0.0185 | 0.0000 | 0.0004 | 0.0000 | 0.0019 | 0.0000 | 0.0156 | 0.5000 | 0.0009 | 0.0000 | 0.0006 | 0.0000 |
| 10000 | 0.0420 | 0.0000 | 0.0003 | 0.0000 | 0.0009 | 0.0000 | 0.0304 | 1.0273 | 0.0003 | 0.0000 | 0.0005 | 0.0000 |
| 50000 | 0.2530 | 0.0000 | 0.0006 | 0.0000 | 0.0008 | 0.0000 | 0.1405 | 5.1094 | 0.0004 | 0.0000 | 0.0013 | 0.0000 |
| 100000 | 0.5197 | 0.0000 | 0.0005 | 0.0000 | 0.0020 | 0.0000 | 0.3536 | 9.9375 | 0.0004 | 0.0000 | 0.0008 | 0.0000 |
| 500000 | 3.7554 | 12.9492 | 0.0007 | 0.0000 | 0.0008 | 0.0000 | 2.6851 | 58.3633 | 0.0010 | 0.0000 | 0.0026 | 0.0000 |

## Key Metrics
- **Time** is measured in seconds.
- **Memory** is measured in megabytes (MB).

## Visualization
Refer to the generated plots in the `/plots` folder for a visual comparison of the results.
