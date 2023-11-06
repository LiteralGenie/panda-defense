import time
from math import modf
from typing import ClassVar

from direct.actor.Actor import Actor
from direct.interval.Interval import Interval
from panda3d.core import NodePath

import g
from game.event_manager import TickEvents
from game.units.render_unit_events import (
    RenderUnitDeath,
    RenderUnitEvents,
    RenderUnitMovement,
    RenderUnitSpawn,
)
from game.view.game_view_globals import GameViewGlobals
from utils.event_utils import get_latest_event


class UnitView:
    model: ClassVar[Actor] = Actor(
        "data/assets/glTF-Sample-Models/2.0/BoomBox/glTF/BoomBox.gltf"
    )

    id: int
    pnode: Actor | None

    _intervals: "dict[str, Interval]"

    def __init__(self, id: int):
        self.id = id
        self.pnode = None

        self._intervals = dict()

    def _init_model(self) -> Actor:
        pnode = NodePath("")
        self.__class__.model.instanceTo(pnode)

        pnode.getChild(0).setScale(20)
        pnode.reparentTo(g.render)

        return pnode  # type: ignore

    def render(
        self,
        tick: TickEvents,
        globals: GameViewGlobals,
        events: list[RenderUnitEvents],
    ):
        unit = tick.state["units"][self.id]
        ppath = globals.cache.ppaths[unit["id_path"]]

        if not self.pnode:
            self.pnode = self._init_model()

        if get_latest_event(RenderUnitSpawn, events):
            dist = int(unit["dist"])
            pos = ppath.points[dist].pos
            self.pnode.setPos(pos[0], pos[1], 0)

        if get_latest_event(RenderUnitMovement, events):
            dist = unit["dist"]

            frac, idx = modf(dist)
            idx = int(idx)

            pt = ppath.points[idx]
            new_pos = (pt.pos[0] + frac * pt.dir[0], pt.pos[1] + frac * pt.dir[1])

            if ivl := self._intervals.get("pos"):
                ivl.pause()

            self._intervals["pos"] = self.pnode.posInterval(  # type: ignore
                (tick.tick_end - time.time() + 0.02),
                (new_pos[0], new_pos[1], 0),
            )
            self._intervals["pos"].start()  # type: ignore

        if get_latest_event(RenderUnitDeath, events):
            self.delete()

    def delete(self):
        if self.pnode:
            self.pnode.removeNode()
