from dataclasses import dataclass
from typing import Any

from direct.gui.DirectGui import DirectFrame
from panda3d.core import NodePath

import g
from game.game_actions import BuyTowerAction
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.drag_and_drop import DragAndDrop, DragMoveState, DragState
from game.shared_globals import SG
from game.towers.basic.basic_tower_model import BasicTowerModel
from game.towers.tower_view import TowerView
from game.view.game_view_globals import GVG
from utils.gui_utils import mpos_to_real_pos
from utils.types import Point2, Point2f


@dataclass
class _StartData:
    invalid_tiles: set[Point2]
    placeholder: NodePath


@dataclass
class _MoveData:
    active_tile: Point2 | None


class TowerTile(BetterDirectFrame):
    dnd: DragAndDrop[_StartData, _MoveData]

    def __init__(self, parent: DirectFrame, **kwargs: Any):
        super().__init__(parent, **kwargs)

        self.dnd = DragAndDrop(
            target=self,
            on_drag_start=self._on_drag_start,
            on_drag_move=self._on_drag_move,
            on_drag_end=self._on_drag_end,
            on_drag_cancel=self._on_drag_cancel,
        )

    def delete(self):
        self.dnd.delete()

    def _on_drag_start(self, pos: Point2f, time: float):
        invalid_tiles: set[Point2] = set()
        for tower in SG.entities.data["TOWER"].values():
            invalid_tiles.add(tower["pos"])

        for path in GVG.cache.ppaths.values():
            for point in path.points:
                invalid_tiles.add(point.pos)

        placeholder = NodePath("")
        TowerView.actor.instance_to(placeholder)
        placeholder.set_pos((0, 0, -10))
        placeholder.reparent_to(g.render)

        return _StartData(invalid_tiles=invalid_tiles, placeholder=placeholder)

    def _on_drag_move(
        self,
        pos: Point2f,
        time: float,
        prev: DragState[_StartData, _MoveData],
    ):
        # coordinates of map tile being hovered
        real_pos = mpos_to_real_pos(pos)
        active_tile = (round(real_pos[0] + 0.0), round(real_pos[1] + 0.0))

        if active_tile not in prev.start_data.invalid_tiles:
            prev.start_data.placeholder.set_pos((active_tile[0], active_tile[1], 0))

            return _MoveData(active_tile=active_tile)
        else:
            return _MoveData(active_tile=None)

    def _on_drag_end(
        self,
        state: DragMoveState[_StartData, _MoveData],
    ):
        if pos := state.move_data.active_tile:
            GVG.event_pipe.send(
                BuyTowerAction(
                    BasicTowerModel,
                    kwargs=dict(pos=pos),
                )
            )

    def _on_drag_cancel(self, state: None | DragState[_StartData, _MoveData]):
        if state:
            state.start_data.placeholder.removeNode()
