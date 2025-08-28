from datetime import datetime, timezone
import time
import tracemalloc
import threading
import os
import csv
import inspect

from typing import Any, Tuple, Callable


# Thread-Based Metadata Storage
call_metadata = threading.local()  # Thread-local storage to track recursion level


# Helpers
def clear_previous_benchmarks(fn: Callable) -> None:
    """
    Clear the CSV benchmarks file for `fn`.

    Args:
        fn: The function whose benchmark CSV should be cleared.
        keep_header: If True, rewrites the header row. If False, truncates to empty.
    """
    # Prep CSV Directory
    CSV_BENCHMARK_PATH = f"benchmarks/{fn.__name__}_benchmarks.csv"
    folder = os.path.dirname(CSV_BENCHMARK_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)

    # Truncate File
    open(CSV_BENCHMARK_PATH, "w").close()


def read_time() -> datetime:
    return datetime.now(timezone.utc)


def run_with_measurements(
    fn: Callable, *args, **kwargs
) -> Tuple[Any, float, float, bool]:
    """
    Runs `fn` and returns (result, elapsed_ms, peak_kib, is_intermediate_call).
    Measures only the outermost call in this thread, but includes
    time and memory from all nested calls (e.g., recursion).
    """
    if not hasattr(call_metadata, "depth"):
        call_metadata.depth = 0

    # Nested call → skip measuring but still return a 3-tuple so the outer decorator's unpacking (result, elapsed_ms, peak_kib) works.
    if call_metadata.depth > 0:
        return fn(*args, **kwargs), 0.0, 0.0, True

    call_metadata.depth += 1
    try:
        tracemalloc.start()
        t0 = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        _, peak = tracemalloc.get_traced_memory()
        return result, elapsed_ms, (peak / 1024.0), False
    finally:
        tracemalloc.stop()
        call_metadata.depth -= 1


# Logger
def benchmark_logger(fn: Callable, /, *args, **kwargs):
    """
    Function to benchmark an algorithm's performance in a CSV file.

    Logs the following columns:
    - algorithm: Name of the decorated function.
    - algorithm args: Depends on the algorithm (variant, size, etc.)
    - elapsed_ms: Wall-clock execution time in milliseconds.
    - peak_kib: Peak Python memory usage in KiB (measured with tracemalloc, includes recursion).
    """
    # Config Column Presets (columns to not benchmark, mostly because their purpose is only assistive)
    dull_columns = {"memo"}

    # Prep CSV Directory
    CSV_BENCHMARK_PATH = f"benchmarks/{fn.__name__}_benchmarks.csv"
    folder = os.path.dirname(CSV_BENCHMARK_PATH)
    if folder:
        os.makedirs(folder, exist_ok=True)

    # Bind args to parameter names
    sig = inspect.signature(fn)
    bound = sig.bind(*args, **kwargs)  # raises if invalid call -> good
    bound.apply_defaults()

    # Run + Measure
    result, elapsed_ms, peak_kib, is_intermediate_call = run_with_measurements(
        fn, *args, **kwargs
    )
    if is_intermediate_call:
        return result  # skip logging for recursive/nested calls

    # Prep CSV File
    param_names = list(sig.parameters.keys())
    # Skip Dull Columns
    for i, param_name in enumerate(param_names):
        if param_name in dull_columns:
            param_names.pop(i)

    fields = ["algorithm", *param_names, "elapsed_ms", "peak_kib"]
    row = {"algorithm": fn.__name__}
    for param_name in param_names:
        # Skip Dull Columns
        if param_name in dull_columns:
            continue
        row[param_name] = str(bound.arguments.get(param_name))
    row["elapsed_ms"] = f"{elapsed_ms:.3f}"
    row["peak_kib"] = f"{peak_kib:.3f}"

    # Write once per outer call
    with open(CSV_BENCHMARK_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if f.tell() == 0:
            writer.writeheader()
        writer.writerow(row)

    return result
