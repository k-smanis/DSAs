from utils.loggers import benchmark_logger, clear_previous_benchmarks
from algorithms.fibonacci import fibonacci


def benchmark_fibonacci():
    clear_previous_benchmarks(fn=fibonacci)
    for n in range(40):
        for variant in ["iterative", "recursive"]:
            benchmark_logger(fibonacci, N=n, variant=variant)


if __name__ == "__main__":
    benchmark_fibonacci()
