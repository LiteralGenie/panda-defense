from dataclasses import dataclass
from typing import Callable, Generic, Iterable, TypedDict, TypeVar, Unpack

from direct.gui.DirectGui import DGG, DirectFrame
from direct.showbase.DirectObject import DirectObject

from utils.gui_utils import get_mouse_pos

_Point2d = tuple[float, float]

Extras = TypeVar("Extras")


@dataclass
class DragStartState:
    data: None
    start: _Point2d
    end: None


@dataclass
class DragMoveState(Generic[Extras]):
    data: Extras
    start: _Point2d
    end: _Point2d


_DragState = DragStartState | DragMoveState[Extras]


class DragListeners(Generic[Extras], TypedDict):
    on_drag_move: Callable[[Extras | None, _Point2d, _Point2d], DragMoveState[Extras]]
    on_drag_end: Callable[[_DragState[Extras]], None]
    on_drag_cancel: Callable[[_DragState[Extras]], None]


class DragAndDrop(Generic[Extras], DirectObject):
    drag_area: DirectFrame
    listeners: DragListeners[Extras]
    state: _DragState[Extras] | None

    def __init__(
        self,
        drag_area: DirectFrame,
        drag_start_events: Iterable[str],
        **listeners: Unpack[DragListeners[Extras]]
    ):
        self.drag_area = drag_area
        self.listeners = listeners
        self.state = None

        for ev in drag_start_events:
            self.accept(ev, lambda: self.drag_start())
        for ev in (DGG.CURSORMOVE,):
            self.drag_area.bind(ev, self.drag_move)
        for ev in (DGG.B1RELEASE,):
            self.drag_area.bind(ev, self.drag_end)
        for ev in (
            DGG.B1PRESS,
            DGG.WITHOUT,
        ):
            self.drag_area.bind(ev, self.drag_cancel)

    def drag_start(self):
        print("drag start")
        if self.state is not None:
            print("drag start ignored")
            return

        start = get_mouse_pos()
        if not start:
            return

        self.state = DragStartState(start=start, end=None, data=None)

    def drag_move(self):
        print("drag_move")
        if not isinstance(self.state, (DragStartState, DragMoveState)):
            return

        end = get_mouse_pos()
        if not end:
            return

        self.state = self.listeners["on_drag_move"](
            self.state.data,
            self.state.start,
            end,
        )

    def drag_end(self):
        print("drag_end")
        if not isinstance(self.state, (DragStartState, DragMoveState)):
            return

        self.listeners["on_drag_end"](self.state)
        self.state = None

    def drag_cancel(self):
        print("drag_cancel")
        if not isinstance(self.state, (DragStartState, DragMoveState)):
            return

        self.listeners["on_drag_cancel"](self.state)
        self.state = None

    def delete(self):
        self.ignore_all()
