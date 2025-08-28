from typing import Dict

memo: Dict[int, int] = {0: 0, 1: 1}


# def reset_fibonacci_memo() -> None:
#     memo.clear()
#     memo.update({0: 0, 1: 1})


def fibonacci(
    N: int, variant: str = "recursive", memo: Dict[int, int] | None = None
) -> int:
    # Recursive Solution
    if variant == "recursive":
        if memo is None:
            memo = {0: 0, 1: 1}

        if N in memo:
            return memo[N]
        else:
            memo[N] = fibonacci(N=N - 1, variant="recursive", memo=memo) + fibonacci(
                N=N - 2, variant="recursive", memo=memo
            )
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
