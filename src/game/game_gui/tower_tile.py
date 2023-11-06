from dataclasses import dataclass
from typing import Any

from direct.gui.DirectGui import DirectFrame

from game.game_actions import BuyTowerAction
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.drag_and_drop import DragAndDrop, DragMoveState, DragState
from game.towers.basic.basic_tower_model import BasicTowerModel
from game.view.game_view_globals import GameViewGlobals
from utils.gui_utils import mpos_to_real_pos
from utils.types import Point2, Point2f


@dataclass
class _StartData:
    invalid_tiles: set[Point2]


@dataclass
class _MoveData:
    active_tile: Point2 | None


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
        invalid_tiles: set[Point2] = set()
        for tower in self.globals.state["towers"].values():
            invalid_tiles.add(tower["pos"])

        for path in self.globals.cache.ppaths.values():
            for point in path.points:
                invalid_tiles.add(point.pos)

        return _StartData(invalid_tiles=invalid_tiles)

    def _on_drag_move(
        self,
        pos: Point2f,
        time: float,
        prev: DragState[_StartData, _MoveData],
    ):
        # coordinates of map tile being hovered
        real_pos = mpos_to_real_pos(pos)
        active_tile = (int(real_pos[0]), int(real_pos[1]))

        if active_tile not in prev.start_data.invalid_tiles:
            return _MoveData(active_tile=active_tile)
        else:
            return _MoveData(active_tile=None)

    def _on_drag_end(
        self,
        state: DragMoveState[_StartData, _MoveData],
    ):
        if pos := state.move_data.active_tile:
            self.globals.event_pipe.send(
                BuyTowerAction(
                    BasicTowerModel,
                    kwargs=dict(pos=pos),
                )
            )

    def _on_drag_cancel(self):
        return
