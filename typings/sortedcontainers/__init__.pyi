from typing import Callable, Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")
Key = TypeVar("Key")

class SortedKeyList(Generic[T, Key]):
    def __init__(
        self,
        xs: Iterable[T] | None = None,
        key: Callable[[T], Key] | None = None,
    ) -> None: ...
    def add(self, item: T) -> None: ...
    def remove(self, item: T) -> None: ...
    def __iter__(self) -> Iterator[T]: ...
