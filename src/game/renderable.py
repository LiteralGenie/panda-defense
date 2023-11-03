from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, Type, TypeVar

from utils.misc_utils import find

if TYPE_CHECKING:
    from panda3d.core import NodePath

Events = TypeVar("Events")
NodeType = TypeVar("NodeType", bound="NodePath")
T = TypeVar("T")


class Renderable(Generic[Events, NodeType], ABC):
    pnode: "NodeType | None"
    render_queue: list[Events]

    def __init__(self):
        self.pnode = None
        self.render_queue = []

    @abstractmethod
    def render(self, period_s: float) -> None:
        ...

    def get_latest_event(self, ev_type: Type[T]) -> T | None:
        return find(
            self.render_queue,
            lambda ev: isinstance(ev, ev_type),
            reverse=True,
        )
