# Performance Measurement Overview

This project includes a utility for measuring **execution time** and **peak memory usage** of algorithms during tests.

The measurement system is implemented in [`tests/utils/logger.py`](../tests/utils/logger.py) and is designed to:

- Work with **recursive functions** by measuring peak memory for the entire call tree.
- Log results to a CSV file for later analysis.
- Keep measurement logic in the **tests** directory so production code in `src/` remains clean.

## Memory Usage Measurement

Memory usage is measured using Python's built-in [`tracemalloc`](https://docs.python.org/3/library/tracemalloc.html) module. The measurement function:

- Starts `tracemalloc` before the target function runs.
- Tracks **peak memory usage** (in KiB) across the entire execution, including all recursive calls.
- Uses a global lock to prevent overlapping `tracemalloc.start()`/`stop()` calls, ensuring accuracy in recursive and concurrent scenarios.
- Stops `tracemalloc` immediately after the function completes to free resources.

The helper function `run_with_peak_memory(fn, *args, **kwargs)` returns a tuple:

```python
(result, peak_kib)
```

where `result` is the function's return value and `peak_kib` is the peak Python memory usage in kibibytes.

## Execution Time Measurement

Execution time is measured using UTC timestamps from Python's [`datetime`](https://docs.python.org/3/library/datetime.html) module.

- The start time is recorded immediately before calling the target function.
- The end time is recorded immediately after the function returns.
- Elapsed time is calculated in milliseconds:

```python
elapsed_ms = (end_time - start_time).total_seconds() * 1000.0
```

This provides high-resolution wall-clock timing suitable for performance tests.

## Usage Guide

To measure both execution time and memory usage, use the `@measure` decorator from `loggers.py`:

```python
from tests.utils.loggers import measure

@measure("logs/uncategorized/fibonacci_logs.csv")
def fib(n):
    return 1 if n < 2 else fib(n-1) + fib(n-2)
```

When run, the decorator will:

1. Measure the execution time and peak memory usage.
2. Log the results to the specified CSV file, creating it with headers if it does not exist.

**CSV log format:**

```csv
git_head,test_name,elapsed_ms,peak_kib
b6f5833,test_fib_10,0.181,0.234
```

- `git_head`: The short commit hash from `git rev-parse --short HEAD`.
- `test_name`: The name of the function being tested.
- `elapsed_ms`: Execution time in milliseconds.
- `peak_kib`: Peak memory usage in kibibytes.
