from dataclasses import dataclass
from typing import Any

from direct.gui.DirectGui import DirectFrame

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.drag_and_drop import DragAndDrop, DragState
from game.view.game_view_globals import GameViewGlobals
from utils.gui_utils import mpos_to_real_pos
from utils.types import Point2, Point2f


@dataclass
class _StartData:
    invalid_tiles: set[Point2]


@dataclass
class _MoveData:
    invalid_tiles: set[Point2]
    active_tile: Point2


_DndState = DragState[_StartData, _MoveData]


class TowerTile(BetterDirectFrame):
    dnd: DragAndDrop[_StartData, _MoveData]
    globals: GameViewGlobals

    def __init__(self, parent: DirectFrame, globals: GameViewGlobals, **kwargs: Any):
        super().__init__(parent, **kwargs)

        self.dnd = DragAndDrop(
            target=self,
            on_drag_start=self._on_drag_start,
            on_drag_move=self._on_drag_move,
            on_drag_end=self._on_drag_end,
            on_drag_cancel=self._on_drag_cancel,
        )
        self.globals = globals

    def delete(self):
        self.dnd.delete()

    def _on_drag_start(self, pos: Point2f, time: float):
        print("on_drag_start cb")

        invalid_tiles: set[Point2] = set()
        for tower in self.globals.state["towers"].values():
            invalid_tiles.add(tower["pos"])

        for path in self.globals.cache.ppaths.values():
            for point in path.points:
                invalid_tiles.add(point.pos)

    def _on_drag_move(self, pos: Point2f, time: float, prev: _DndState):
        print("on_drag_move cb")

        # coordinates of map tile being hovered
        real_pos = mpos_to_real_pos(pos)

    def _on_drag_end(self, *args: Any):
        print("on_drag_end cb", args)

    def _on_drag_cancel(self, *args: Any):
        print("on_drag_cancel cb", args)
