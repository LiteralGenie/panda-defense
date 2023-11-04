from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, ClassVar, Generic, Type, TypeVar

from utils.misc_utils import find

if TYPE_CHECKING:
    from panda3d.core import NodePath

RenderEventType = TypeVar("RenderEventType")
NodeType = TypeVar("NodeType")
T = TypeVar("T")


class Renderable(Generic[RenderEventType, NodeType], ABC):
    model: "ClassVar[NodeType | None]" = None  # type: ignore
    pnode: "NodeType | None"
    render_queue: list[RenderEventType]

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
        )  # type: ignore
