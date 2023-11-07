from dataclasses import dataclass
from typing import Any, ClassVar

from direct.gui.DirectGui import DirectFrame
from panda3d.core import NodePath
from reactivex.abc import DisposableBase

import g
from game.events.event_manager import GameEvent
from game.game_actions import BuyTowerAction
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.drag_and_drop import DragAndDrop, DragMoveState, DragState
from game.shared_globals import SG
from game.state import StateCreated, StateDeleted
from game.towers.basic.basic_tower_model import BasicTowerModel
from game.towers.tower_view import TowerView
from game.view.game_view_globals import GVG
from utils.gui_utils import mpos_to_real_pos
from utils.types import Point2, Point2f


@dataclass
class _StartData:
    placeholder: NodePath


@dataclass
class _MoveData:
    active_tile: Point2 | None


class TowerTile(BetterDirectFrame):
    _invalid_tiles: ClassVar[set[Point2]] = set()
    _tile_sub: ClassVar[DisposableBase | None] = None

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

        self._sub_invalid_tiles()

    def _sub_invalid_tiles(self):
        if not self.__class__._tile_sub:
            tiles: set[Point2] = set()

            for tower in SG.entities.data["TOWER"].values():
                tiles.add(tower["pos"])

            for path in GVG.cache.ppaths.values():
                for point in path.points:
                    tiles.add(point.pos)

            self.__class__._invalid_tiles = tiles

            def on_next(ev: GameEvent):
                match ev:
                    case StateCreated(category="TOWER"):
                        self.__class__._invalid_tiles.add(ev.data["pos"])
                    case StateDeleted(category="TOWER"):
                        self.__class__._invalid_tiles.remove(ev.data["pos"])
                    case _:
                        pass

            self.__class__._tile_sub = GVG.event_subj.subscribe(on_next=on_next)

    def delete(self):
        self.dnd.delete()

    def _on_drag_start(self, pos: Point2f, time: float):
        placeholder = NodePath("")
        TowerView.actor.instance_to(placeholder)
        placeholder.set_pos((0, 0, -10))
        placeholder.reparent_to(g.render)

        return _StartData(placeholder=placeholder)

    def _on_drag_move(
        self,
        pos: Point2f,
        time: float,
        prev: DragState[_StartData, _MoveData],
    ):
        # coordinates of map tile being hovered
        real_pos = mpos_to_real_pos(pos)
        active_tile = (round(real_pos[0] + 0.0), round(real_pos[1] + 0.0))

        if active_tile not in self._invalid_tiles:
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
