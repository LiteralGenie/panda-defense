from enum import Enum
from math import modf
from typing import TYPE_CHECKING, ClassVar

from game.parameterized_path import ParameterizedPath
from game.renderable import Renderable
from game.unit.render_unit_events import (
    RenderUnitDeath,
    RenderUnitEvents,
    RenderUnitMovement,
    RenderUnitPosition,
)

if TYPE_CHECKING:
    from direct.interval.Interval import Interval
    from panda3d.core import NodePath


class UnitStatus(Enum):
    PRESPAWN = "PRESPAWN"
    ALIVE = "ALIVE"
    DEAD = "DEAD"


class Unit(Renderable[RenderUnitEvents, "NodePath"]):
    _id_counter: ClassVar[int] = 0

    id: int
    id_wave: int

    dist: float
    health: int
    ppath: ParameterizedPath
    speed: float  # todo: use Decimal
    status: UnitStatus

    _intervals: dict[str, "Interval"]

    def __init__(self, id_wave: int, ppath: ParameterizedPath, speed: float):
        super().__init__()
        self.pnode = None

        self.__class__._id_counter += 1
        self.id = self._id_counter
        self.id_wave = id_wave

        self.dist = 0
        self.health = 100
        self.ppath = ppath
        self.speed = speed
        self.status = UnitStatus.PRESPAWN

        self._intervals = dict()

    def render(self, period_s: float):
        from direct.actor.Actor import Actor
        from panda3d.core import NodePath, Point3

        import g

        # Don't spawn units after death
        if not self.render_queue:
            return

        if not self.__class__.model:
            self.__class__.model = Actor(
                "data/assets/glTF-Sample-Models/2.0/BoomBox/glTF/BoomBox.gltf"
            )

        if not self.pnode:
            self.pnode = NodePath("")
            self.__class__.model.instanceTo(self.pnode)

            self.pnode.getChild(0).setScale(20)
            self.pnode.reparentTo(g.render)

        if self.get_latest_event(RenderUnitPosition):
            pos = self.ppath.points[int(self.dist)].pos
            self.pnode.setPos(pos[0], pos[1], 0)

        if self.get_latest_event(RenderUnitMovement):
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

        if self.get_latest_event(RenderUnitDeath):
            self.delete()

    def delete(self):
        if self.pnode:
            self.pnode.removeNode()
            self.pnode = None
