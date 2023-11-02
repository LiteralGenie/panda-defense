import math

from direct.actor.Actor import Actor
from direct.interval.Interval import Interval
from panda3d.core import NodePath, Point3

from game.parameterized_path import ParameterizedPath
from game.stateful import Stateful, StatefulProp


class Unit(Stateful):
    pnode: Actor | None

    dist: float = StatefulProp()  # type: ignore
    speed: float  # todo: use Decimal

    _intervals: dict[str, Interval]

    def __init__(self, speed: float):
        super().__init__()
        self.pnode = None

        self.dist = 0
        self.speed = speed

        self._intervals = dict()

    def render(self, parent: NodePath, period_s: float, ppath: ParameterizedPath):
        if not self.pnode:
            self.pnode = Actor(
                "data/assets/glTF-Sample-Models/2.0/BoomBox/glTF/BoomBox.gltf"
            )

            self.pnode.getChild(0).setScale(20)

            start = ppath.points[0].pos
            self.pnode.setPos(start[0], start[1], 0)

            self.pnode.reparentTo(parent)

        if self.state["dist"].needs_check:
            frac, idx = math.modf(self.dist)
            idx = int(idx)

            pt = ppath.points[idx]
            new_pos = (pt.pos[0] + frac * pt.dir[0], pt.pos[1] + frac * pt.dir[1])

            if ivl := self._intervals.get("pos"):
                ivl.pause()

            self._intervals["pos"] = self.pnode.posInterval(
                period_s,
                Point3(new_pos[0], new_pos[1], 0),
            )
            self._intervals["pos"].start()

        super().save_props()

    def delete(self):
        if self.pnode:
            self.pnode.cleanup()
            self.pnode.removeNode()
