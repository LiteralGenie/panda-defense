import time
from dataclasses import dataclass
from typing import Any, Callable, ClassVar, Generic, TypedDict, TypeVar, Unpack
from uuid import uuid4

from direct.gui.DirectGui import DGG
from direct.gui.DirectGuiBase import DirectGuiWidget
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from panda3d.core import MouseWatcherParameter

from utils.gui_utils import get_mouse_pos
from utils.types import Point2f

_StartData = TypeVar("_StartData")
_MoveData = TypeVar("_MoveData")


@dataclass
class DragStartState(Generic[_StartData]):
    start_pos: Point2f
    end_pos: None

    start_time: float
    end_time: None

    start_data: _StartData
    move_data: None
    _poller: Any


@dataclass
class DragMoveState(Generic[_StartData, _MoveData]):
    start_pos: Point2f
    end_pos: Point2f

    start_time: float
    end_time: float

    start_data: _StartData
    move_data: _MoveData
    _poller: Task


DragState = DragStartState[_StartData] | DragMoveState[_StartData, _MoveData]


class DragListeners(Generic[_StartData, _MoveData], TypedDict):
    # (start pos / time) -> (start data)
    on_drag_start: Callable[[Point2f, float], _StartData]
    # (current pos / time, previous start or move data) -> (move data)
    on_drag_move: Callable[
        [Point2f, float, DragState[_StartData, _MoveData]], _MoveData
    ]
    # (move data) -> (None)
    on_drag_end: Callable[[DragMoveState[_StartData, _MoveData]], None]
    # (last state or None) -> (None)
    # this is called called if...
    #    multiple drag_starts (probably mobile)
    #    cancel() was invoked
    #    the mousedown to mouseup period was too short for the poller to invoke mousemove
    on_drag_cancel: Callable[[DragState[_StartData, _MoveData] | None], None]


class DragAndDrop(Generic[_StartData, _MoveData], DirectObject):
    """
    Attaches drag start / move / end / cancel callbacks to a GUI widget

    On mousedown, the start cb will be invoked
    Afterwards, the move cb will be invoked at regular intervals until mouseup
    On mouseup, the end cb will be invoked
    If cancel() is called (or another mousedown somehow occurs) before mouseup, the cancel cb will be invoked instead
    """

    POLL_FREQ_S: ClassVar[float] = 0.05

    listeners: DragListeners[_StartData, _MoveData]
    state: DragState[_StartData, _MoveData] | None
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
            return self.drag_cancel()

        start_pos = get_mouse_pos()
        if not start_pos:
            # Ignore locations outside viewport
            return

        start_time = time.time()

        start_data = self.listeners["on_drag_start"](start_pos, start_time)

        _poller = base.task_mgr.doMethodLater(
            self.POLL_FREQ_S, self.drag_move, f"drag_and_drop_{uuid4()}"
        )

        self.state = DragStartState(
            start_pos=start_pos,
            end_pos=None,
            start_time=time.time(),
            end_time=None,
            start_data=start_data,
            move_data=None,
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

        move_data = self.listeners["on_drag_move"](end_pos, end_time, self.state)
        self.state = DragMoveState(
            end_pos=end_pos,
            end_time=end_time,
            move_data=move_data,
            start_pos=self.state.start_pos,
            start_time=self.state.start_time,
            start_data=self.state.start_data,
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
        self.listeners["on_drag_cancel"](self.state)
        self._deleteState()

    def delete(self):
        self.ignore_all()
        self._deleteState()

    def cancel(self):
        if self.state:
            self.drag_cancel()

    def _deleteState(self):
        if self.state:
            self.state._poller.cancel()  # type: ignore
            self.state = None
