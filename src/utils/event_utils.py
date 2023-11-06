from typing import Any, Type, TypeVar

from utils.misc_utils import find

T = TypeVar("T")


def get_latest_event(ev_type: Type[T], evs: list[Any]) -> T | None:
    return find(
        evs,
        lambda ev: isinstance(ev, ev_type),
        reverse=True,
    )
