from typing import Any, Callable, TypeVar

T = TypeVar("T")


def find(xs: list[T], is_match: Callable[[T], bool], reverse: bool = False) -> T | None:
    idx = find_index(xs, is_match, reverse=reverse)
    if idx is None:
        return None
    return xs[idx]


def find_or_throw(
    xs: list[T], is_match: Callable[[T], bool], reverse: bool = False
) -> T:
    idx = find_index(xs, is_match, reverse=reverse)
    if idx is None:
        raise Exception("Not found")
    return xs[idx]


def find_index(
    xs: list[T],
    is_match: Callable[[T], bool],
    reverse: bool = False,
) -> int | None:
    """Find smallest index that satisfies is_match()"""

    if len(xs) == 0:
        return None

    it = range(0, len(xs), 1) if not reverse else range(len(xs) - 1, -1, -1)

    for idx in it:
        x = xs[idx]
        if is_match(x):
            return idx

    return None


def find_index_sorted(
    xs: list[T],
    target: Any,
    key: Callable[[T], Any],
    return_largest_idx: bool = False,
) -> int | None:
    """
    Find smallest index that holds target

    xs should already be sorted in ascending order
    values returned by key(x) should support the comparison operators (<, >, ==)

    key(a, b) should return:
        -1 if a < b
         0 if a == b
         1 if a > b
    """

    def _find(vals: list[Any]) -> int | None:
        n = len(vals)
        if n == 0:
            return None

        idx_pivot = n // 2
        pivot = xs[idx_pivot]

        check_left = lambda: _find(xs[:idx_pivot]) if pivot >= target else None
        check_pivot = lambda: idx_pivot if pivot == target else None
        check_right = lambda: _find(xs[idx_pivot + 1 :]) if pivot <= target else None

        if return_largest_idx:
            return check_right() or check_pivot() or check_left()
        else:
            return check_left() or check_pivot() or check_right()

    vals = [key(x) for x in xs]
    return _find(vals)


def find_insertion_index(
    xs_sorted: list[T],
    target: T,
    return_largest_idx: bool = False,
) -> int:
    """
    Find index such that (target > items_before_index) and (target <= items_at_or_after_index)

    xs_sorted should be sorted in ascending order and items should be comparable

    if return_smallest_idx is false, the returned index will satisfy
    (target >= items_before_index) and (target < items_at_or_after_index)
    ie the equals sign will be moved to the other condition
    """

    idx_mn = 0
    idx_mx = len(xs_sorted) - 1

    def lt(a: T, b: T, eq: bool) -> bool:
        if eq:
            return a <= b
        else:
            return a < b

    while (idx_mx - idx_mn) > 1:
        idx_pivot = idx_mn + (idx_mx - idx_mn) // 2
        pivot = xs_sorted[idx_pivot]

        if lt(target, pivot, eq=not return_largest_idx):
            idx_mx = idx_pivot
        else:
            idx_mn = idx_pivot

    result = idx_mx
    if return_largest_idx:
        result += 1

    return result


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


def first_in_dict(data: dict[Any, T]) -> T:
    first_key = next(iter(data))
    return data[first_key]
