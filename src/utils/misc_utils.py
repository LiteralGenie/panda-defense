from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def find_index(xs: Iterable[T], key: Callable[[T], bool]) -> int | None:
    for i, x in enumerate(xs):
        if key(x):
            return i
    return None


def split_with_lookback(
    xs: list[T], should_split: Callable[[T, T], bool]
) -> list[list[T]]:
    if len(xs) == 0:
        return []

    buffer = [xs[0]]
    result: list[list[T]] = []
    for i in range(1, len(xs)):
        prev = xs[i - 1]
        curr = xs[i]

        if should_split(prev, curr):
            result.append(buffer)
            buffer = [curr]
        else:
            buffer.append(curr)

    if len(buffer):
        result.append(buffer)

    return result
