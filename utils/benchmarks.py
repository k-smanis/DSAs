from utils.loggers import benchmark_logger
from algorithms.fibonacci import fibonacci, reset_fibonacci_memo


def benchmark_fibonacci():
    for n in range(40):
        for variant in ["iterative", "recursive"]:
            reset_fibonacci_memo()
            benchmark_logger(fibonacci, N=n, variant=variant)


if __name__ == "__main__":
    benchmark_fibonacci()
