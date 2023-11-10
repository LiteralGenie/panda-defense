import time
from math import modf

from direct.actor.Actor import Actor
from direct.interval.Interval import Interval
from panda3d.core import NodePath
from reactivex import operators as ops
from reactivex.abc import DisposableBase

import g
from game.events.event_manager import GameEvent
from game.events.render_event import RenderTowerAttack
from game.shared_globals import SG
from game.state.game_state import StateUpdated
from game.units.unit_model import UnitModel, UnitStatus
from game.view.game_view_globals import GVG
from utils.types import Point2f


class UnitView:
    id: int
    model: UnitModel
    pnode: Actor | None

    _intervals: "dict[str, Interval]"
    _event_sub: DisposableBase

    def __init__(self, id: int):
        self.id = id
        self.model = self._init_model()
        self.pnode = None

        self._intervals = dict()
        self._event_sub = self._subscribe_events()

    def _init_model(self):
        data = SG.state.data["UNIT"][self.id]["data"]
        ppath = GVG.data.ppaths[data["id_path"]]
        return UnitModel.load(self.id, ppath=ppath)

    def _init_pnode(self) -> Actor:
        pnode = NodePath("")
        self.__class__.actor.instance_to(pnode)

        dist = int(self.model.dist)
        pos = self.model.ppath.points[dist].pos
        pnode.set_pos(pos + (0,))

        pnode.reparent_to(g.render)

        return pnode  # type: ignore

    def _subscribe_events(self):
        def filter(ev: GameEvent):
            match ev:
                case RenderTowerAttack():
                    return self.id in ev.id_targets
                case StateUpdated():
                    return ev.id == self.id
                case _:
                    return False

        def on_next(ev: GameEvent):
            match ev:
                case StateUpdated(_, _, key, value):
                    match key:
                        case UnitModel.dist.key:  # type: ignore
                            self._render_pos()
                        case UnitModel.status.key:  # type: ignore
                            if value == UnitStatus.ALIVE:
                                self.pnode = self._init_pnode()
                            elif value == UnitStatus.DEAD:
                                self.delete()
                        case _:
                            pass
                case _:
                    pass

        return GVG.event_subj.pipe(
            ops.filter(filter),
        ).subscribe(on_next=on_next)

    def _render_pos(self):
        self._intervals["pos"] = self.pnode.posInterval(  # type: ignore
            (GVG.data.meta.tick_end - time.time()),
            self.interpolated_pos + (0,),
        )
        self._intervals["pos"].start()  # type: ignore

    def delete(self):
        self._event_sub.dispose()

        if self.pnode:
            self.pnode.removeNode()

    @classmethod
    @property
    def actor(cls):
        pnode = GVG.resource_mgr.load_actor(
            "glTF-Sample-Models/2.0/BoomBox/glTF/BoomBox.gltf"
        )

        pnode.getChild(0).setScale(20)
        return pnode

    @property
    def interpolated_pos(self) -> Point2f:
        if ivl := self._intervals.get("pos"):
            ivl.pause()

        frac, idx = modf(self.model.dist)
        idx = int(idx)

        pt = self.model.ppath.points[idx]

        new_pos = (
            pt.pos[0] + frac * pt.dir[0],
            pt.pos[1] + frac * pt.dir[1],
        )
        return new_pos
