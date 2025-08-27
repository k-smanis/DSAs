# Project README

&#x20;

## Overview

This repository contains clean, from-scratch implementations of classic algorithms and data structures, written for clarity, testability, and reusability.
It also includes lightweight benchmarking utilities that measure and log algorithm performance — both runtime and memory usage — without third-party dependencies.

## Features

- **Algorithms**: Implemented from scratch without high-level shortcuts.
- **Data Structures**: Stacks, queues, linked lists, trees, graphs, and more (organized under `src/`).
- **Benchmarking Utilities** (CSV Logging)
  - Execution time (ms)
  - Peak memory (KiB) covering the entire call (including recursion)
  - Algorithm's Input Parameters (captured from function signature)

## Example Benchmark

```python
from utils.loggers import benchmark_logger
from algorithms.fibonacci import fibonacci, reset_fibonacci_memo


def benchmark_fibonacci():
    for n in range(40):
        for variant in ["iterative", "recursive"]:
            reset_fibonacci_memo()
            benchmark_logger(fibonacci, N=n, variant=variant)


if __name__ == "__main__":
    benchmark_fibonacci()
```

## License

This project is licensed under the MIT License.
