from dataclasses import dataclass
from typing import Any, ClassVar, Type

from panda3d.core import NodePath
from reactivex.abc import DisposableBase

import g
from game.events.event_manager import GameEvent
from game.events.game_actions import BuyTowerAction
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.drag_and_drop import DragAndDrop, DragMoveState, DragState
from game.state.game_state import StateCreated, StateDeleted
from game.towers.tower_model import TowerModel
from game.towers.tower_view import TowerView
from game.view.game_view_globals import GVG
from game.view.procgen.square import build_rect
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
    TowerModelCls: Type[TowerModel]
    TowerViewCls: Type[TowerView]

    def __init__(
        self,
        parent: BetterDirectFrame,
        TowerModelCls: Type[TowerModel],
        TowerViewCls: Type[TowerView],
        **kwargs: Any,
    ):
        super().__init__(parent, **kwargs)

        self.dnd = DragAndDrop(
            target=self,
            on_drag_start=self._on_drag_start,
            on_drag_move=self._on_drag_move,
            on_drag_end=self._on_drag_end,
            on_drag_cancel=self._on_drag_cancel,
        )
        self.TowerModelCls = TowerModelCls
        self.TowerViewCls = TowerViewCls

        # todo: conditionally preload on hover or availability
        TowerViewCls.preload_actor()
        TowerViewCls.preload_placeholder()

        self._sub_invalid_tiles()

    def _sub_invalid_tiles(self):
        if not self.__class__._tile_sub:
            tiles: set[Point2] = set()

            for tower in GVG.data.models.towers.values():
                tiles.add(tower.pos)

            for path in GVG.data.ppaths.values():
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
        return _StartData(placeholder=self._load_placeholder())

    def _on_drag_move(
        self,
        pos: Point2f,
        time: float,
        prev: DragState[_StartData, _MoveData],
    ):
        # coordinates of map tile being hovered
        real_pos = mpos_to_real_pos(pos)
        active_tile = (round(real_pos[0]), round(real_pos[1]))

        if active_tile not in self._invalid_tiles:
            prev.start_data.placeholder.show()
            prev.start_data.placeholder.set_pos((active_tile[0], active_tile[1], 0))

            return _MoveData(active_tile=active_tile)
        else:
            prev.start_data.placeholder.hide()
            return _MoveData(active_tile=None)

    def _on_drag_end(
        self,
        state: DragMoveState[_StartData, _MoveData],
    ):
        state.start_data.placeholder.removeNode()

        if pos := state.move_data.active_tile:
            GVG.event_pipe.send(
                BuyTowerAction(
                    TowerCls=self.TowerModelCls,
                    kwargs=dict(pos=pos),
                )
            )

    def _on_drag_cancel(self, state: None | DragState[_StartData, _MoveData]):
        if state:
            state.start_data.placeholder.removeNode()

    def _load_placeholder(self):
        placeholder = NodePath("")
        self.TowerViewCls.placeholder.instance_to(placeholder)
        placeholder.reparent_to(g.render)
        placeholder.set_pos((0, 0, -10))

        tile = build_rect((0, 0, 0.2, 0.9))
        for pos in self.TowerModelCls.default_range.points:
            t = NodePath("")
            tile.instance_to(t)
            t.reparent_to(placeholder)
            t.set_pos(pos + (0.001,))

        return placeholder
