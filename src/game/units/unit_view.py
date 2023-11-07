import time
from math import modf
from typing import Any, ClassVar

from direct.actor.Actor import Actor
from direct.interval.Interval import Interval
from panda3d.core import NodePath
from reactivex import operators as ops
from reactivex.abc import DisposableBase

import g
from game.events.event_manager import GameEvent
from game.events.render_event import RenderTowerAttack
from game.shared_globals import SG
from game.state import StateUpdated
from game.units.unit_model import UnitModel, UnitStatus
from game.view.game_view_globals import GVG


class UnitView:
    actor: ClassVar[Actor] = Actor(
        "data/assets/glTF-Sample-Models/2.0/BoomBox/glTF/BoomBox.gltf"
    )

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
        data = SG.entities.data["UNIT"][self.id]["data"]
        ppath = GVG.cache.ppaths[data["id_path"]]
        return UnitModel.load(self.id, ppath=ppath)

    def _init_pnode(self) -> Actor:
        pnode = NodePath("")
        self.__class__.actor.instance_to(pnode)

        dist = int(self.model.dist)
        pos = self.model.ppath.points[dist].pos
        pnode.set_pos(pos + (0,))

        pnode.get_child(0).set_scale(20)

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

        def on_next(ev: Any):
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
        if ivl := self._intervals.get("pos"):
            ivl.pause()

        frac, idx = modf(self.model.dist)
        idx = int(idx)

        pt = self.model.ppath.points[idx]

        new_pos = (
            pt.pos[0] + frac * pt.dir[0],
            pt.pos[1] + frac * pt.dir[1],
        )

        self._intervals["pos"] = self.pnode.posInterval(  # type: ignore
            (GVG.meta.tick_end - time.time()),
            new_pos + (0,),
        )
        self._intervals["pos"].start()  # type: ignore

    def delete(self):
        self._event_sub.dispose()

        if self.pnode:
            self.pnode.removeNode()
