import time
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Generic, TypedDict, TypeVar, Unpack
from uuid import uuid4

from direct.gui.DirectGui import DGG
from direct.gui.DirectGuiBase import DirectGuiWidget
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from panda3d.core import MouseWatcherParameter

import g
from utils.gui_utils import get_mouse_pos

_Point2d = tuple[float, float]
_StartData = TypeVar("_StartData")
_MoveData = TypeVar("_MoveData")


@dataclass
class DragStartState(Generic[_StartData]):
    start_pos: _Point2d
    end_pos: None

    start_time: float
    end_time: None

    data: _StartData
    _poller: Any


@dataclass
class DragMoveState(Generic[_MoveData]):
    start_pos: _Point2d
    end_pos: _Point2d

    start_time: float
    end_time: float

    data: _MoveData
    _poller: Task


_DragState = DragStartState[_StartData] | DragMoveState[_MoveData]


class DragListeners(Generic[_StartData, _MoveData], TypedDict):
    # (start pos / time) -> (start data)
    on_drag_start: Callable[[_Point2d, float], _StartData]
    # (current pos / time, previous start or move data) -> (move data)
    on_drag_move: Callable[
        [_Point2d, float, _DragState[_StartData, _MoveData]], _MoveData
    ]
    # (move data) -> (None)
    on_drag_end: Callable[[DragMoveState[_MoveData]], None]
    # (start data) -> (None)
    # called if there was a drag_start but never a drag_move (ie a click)
    on_drag_cancel: Callable[[DragStartState[_StartData]], None]


class DragAndDrop(Generic[_StartData, _MoveData], DirectObject):
    """
    When the target element receives a mousedown event, the on_drag_start() callback will be invoked.

    After that callback finishes, the on_drag_move() callback will be invoked periodically
        (via a mouse location poller, no such thing as mousemove events in panda3d)

    And finally on mouseup, the on_drag_end() callback will be invoked
        (or alternatively the on_drag_cancel() if it was a really fast click.
         but the on_drag_end() callback should still check the distance / duration
         if it's important to avoid click events)
    """

    POLL_FREQ_S: ClassVar[float] = 0.1

    listeners: DragListeners[_StartData, _MoveData]
    state: _DragState[_StartData, _MoveData] | None
    target: DirectGuiWidget

    def __init__(
        self,
        target: DirectGuiWidget,
        **listeners: Unpack[DragListeners[_StartData, _MoveData]],
    ):
        self.listeners = listeners
        self.target = target
        self.state = None

        target["state"] = DGG.NORMAL  # todo: reset state?
        for ev in (DGG.B1PRESS,):
            self.target.bind(ev, self.drag_start)
        for ev in (DGG.B1RELEASE,):
            self.target.bind(ev, self.drag_end)

    def drag_start(self, param: MouseWatcherParameter):
        if self.state is not None:
            return

        start_pos = get_mouse_pos()
        if not start_pos:
            # Ignore locations outside viewport
            return

        start_time = time.time()

        data = self.listeners["on_drag_start"](start_pos, start_time)

        _poller = g.base.task_mgr.doMethodLater(
            self.POLL_FREQ_S, self.drag_move, f"drag_and_drop_{uuid4()}"
        )

        self.state = DragStartState(
            start_pos=start_pos,
            end_pos=None,
            start_time=time.time(),
            end_time=None,
            data=data,
            _poller=_poller,
        )

    def drag_move(self, task: Task):
        if not isinstance(self.state, (DragStartState, DragMoveState)):
            print("drag_move() called without state (leaky poller?!)")
            return

        end_pos = get_mouse_pos()
        if not end_pos:
            # Ignore locations outside viewport
            return task.again

        end_time = time.time()

        data = self.listeners["on_drag_move"](end_pos, end_time, self.state)
        self.state = DragMoveState(
            end_pos=end_pos,
            end_time=end_time,
            data=data,
            start_pos=self.state.start_pos,
            start_time=self.state.start_time,
            _poller=self.state._poller,  # type: ignore
        )

        return task.again

    def drag_end(self, param: MouseWatcherParameter):
        if not isinstance(self.state, (DragStartState, DragMoveState)):
            return

        if isinstance(self.state, DragStartState):
            return self.drag_cancel()

        self.listeners["on_drag_end"](self.state)
        self._deleteState()

    def drag_cancel(self):
        if not isinstance(self.state, (DragStartState)):
            return

        self.listeners["on_drag_cancel"](self.state)
        self._deleteState()

    def delete(self):
        self.ignore_all()
        self._deleteState()

    def _deleteState(self):
        if self.state:
            self.state._poller.cancel()  # type: ignore
            self.state = None
