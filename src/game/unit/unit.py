from math import modf
from typing import TYPE_CHECKING

from game.parameterized_path import ParameterizedPath
from game.renderable import Renderable
from game.unit.render_unit_events import (
    RenderUnitEvents,
    RenderUnitMovement,
    RenderUnitPosition,
)

if TYPE_CHECKING:
    from direct.actor.Actor import Actor
    from direct.interval.Interval import Interval


class Unit(Renderable[RenderUnitEvents, "Actor"]):
    dist: float
    health: int
    ppath: ParameterizedPath
    speed: float  # todo: use Decimal

    _intervals: dict[str, "Interval"]

    def __init__(self, ppath: ParameterizedPath, speed: float):
        super().__init__()
        self.pnode = None

        self.dist = 0
        self.health = 100
        self.ppath = ppath
        self.speed = speed

        self._intervals = dict()

    def render(self, period_s: float):
        from direct.actor.Actor import Actor
        from panda3d.core import Point3

        import g

        if not self.pnode:
            self.pnode = Actor(
                "data/assets/glTF-Sample-Models/2.0/BoomBox/glTF/BoomBox.gltf"
            )
            self.pnode.getChild(0).setScale(20)
            self.pnode.reparentTo(g.render)

        if self.get_latest_render(RenderUnitPosition):
            pos = self.ppath.points[int(self.dist)].pos
            self.pnode.setPos(pos[0], pos[1], 0)

        if self.get_latest_render(RenderUnitMovement):
            pos = self.ppath.points[int(self.dist)].pos

            frac, idx = modf(self.dist)
            idx = int(idx)

            pt = self.ppath.points[idx]
            new_pos = (pt.pos[0] + frac * pt.dir[0], pt.pos[1] + frac * pt.dir[1])

            if ivl := self._intervals.get("pos"):
                ivl.pause()

            self._intervals["pos"] = self.pnode.posInterval(
                period_s,
                Point3(new_pos[0], new_pos[1], 0),
            )
            self._intervals["pos"].start()

    def delete(self):
        if self.pnode:
            self.pnode.cleanup()
            self.pnode.removeNode()
