from typing import Dict

memo: Dict[int, int] = {0: 0, 1: 1}


def reset_fibonacci_memo() -> None:
    memo.clear()
    memo.update({0: 0, 1: 1})


def fibonacci(N: int, variant: str = "recursive") -> int:
    # Recursive Solution
    if variant == "recursive":
        if N in memo:
            return memo[N]
        else:
            memo[N] = fibonacci(N - 1) + fibonacci(N - 2)
            return memo[N]

    # Iterative Solution
    elif variant == "iterative":
        current: int = 0
        next: int = 1

        for iter in range(N):
            next, current = next + current, next

        return current

    # Handling Invalid Modes
    else:
        raise ValueError(f"Unknown mode: {variant}")
