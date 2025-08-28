import pytest
from algorithms.fibonacci import fibonacci

CSV_LOG_PATH = "logs/fibonacci/fibonacci_logs.csv"


@pytest.fixture
def fibonacci_map():
    return {
        0: 0,
        1: 1,
        5: 5,
        10: 55,
        15: 610,
        20: 6765,
        38: 39088169,
    }


def test_fibonacci_recursive(fibonacci_map):
    for N, expected in fibonacci_map.items():
        assert fibonacci(N) == expected


def test_fibonacci_iterative(fibonacci_map):
    for N, expected in fibonacci_map.items():
        assert fibonacci(N, variant="iterative") == expected


def test_fibonacci_invalid_mode(fibonacci_map):
    with pytest.raises(ValueError):
        fibonacci(5, variant="random")
