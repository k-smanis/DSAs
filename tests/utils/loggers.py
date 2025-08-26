from datetime import datetime, timezone
import tracemalloc
import threading
import os
import csv
import functools
import subprocess
from typing import Any, Tuple, Callable


# Configs
CSV_LOG_PATH = "logs/uncategorized/fibonacci_logs.csv"

# Dependencies
_TRACEMALLOC_LOCK: threading.Lock = (
    threading.Lock()
)  # Prevents multiple overlapping uses of tracemalloc, to block overlapping start/stop commands mid-recursion.


# Readers
def read_time() -> datetime:
    return datetime.now(timezone.utc)


def read_git_HEAD() -> str:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except Exception:
        return ""


def run_with_peak_memory(
    fn: Callable[..., Any], /, *args: Any, **kwargs: Any
) -> Tuple[Any, float]:
    """
    Run `fn(*args, **kwargs)` and return (result, peak_kib).
    Uses tracemalloc; peak covers the entire call (incl. recursion).
    Not safe to call while tracemalloc is already tracing elsewhere.
    """
    if tracemalloc.is_tracing():
        raise RuntimeError(
            "run_with_peak_memory() cannot run because tracemalloc is already tracing somewhere else."
        )

    with _TRACEMALLOC_LOCK:
        tracemalloc.start()
        try:
            result = fn(*args, **kwargs)
            _, peak = tracemalloc.get_traced_memory()
            return result, (peak / 1024.0)
        finally:
            tracemalloc.stop()


# Logger
def measure(csv_path: str = "logs/uncategorized/logs.csv"):
    """
    Decorator to log:
      - test_nodeid (string identifying the test)
      - subject_algorithm (function name or label)
      - elapsed_ms (wall time in milliseconds)
      - peak_kib (peak Python memory in KiB, includes recursion)
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Define
            log_fields = ["git_head", "test_name", "elapsed_ms", "peak_kib"]

            # Measure
            time_start: datetime = read_time()
            result, peak_kib = run_with_peak_memory(func, *args, **kwargs)
            time_end: datetime = read_time()
            elapsed_ms: float = (time_end - time_start).total_seconds() * 1000.0

            # Log
            file_exists = os.path.exists(csv_path)
            os.makedirs(os.path.dirname(csv_path), exist_ok=True)
            with open(file=csv_path, mode="a", newline="") as f:
                dict_writer = csv.DictWriter(f, fieldnames=log_fields)
                if (not file_exists) or (f.tell() == 0):
                    dict_writer.writeheader()
                dict_writer.writerow(
                    {
                        "git_head": read_git_HEAD(),
                        "test_name": func.__name__,
                        "elapsed_ms": f"{elapsed_ms:.3f}",
                        "peak_kib": f"{peak_kib:.3f}",
                    }
                )

            return result

        return wrapper

    return decorator
