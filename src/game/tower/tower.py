from abc import ABC
from typing import TYPE_CHECKING

from game.range import Range
from game.renderable import Renderable
from game.tower.render_tower_events import (
    RenderTowerAttack,
    RenderTowerEvents,
    RenderTowerPosition,
)
from utils.types import Point2

if TYPE_CHECKING:
    from panda3d.core import NodePath


class Tower(Renderable[RenderTowerEvents, "NodePath"], ABC):
    pos: Point2
    range: Range

    def __init__(self, pos: Point2, range: Range):
        super().__init__()
        self.pnode = None

        self.pos = pos
        self.range = range

    def render(self, period_s: float):
        from direct.actor.Actor import Actor
        from panda3d.core import NodePath

        import g

        if not self.__class__.model:
            self.__class__.model = Actor(
                "data/assets/glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf",
            )

        if not self.pnode:
            self.pnode = NodePath("")
            self.__class__.model.instanceTo(self.pnode)

            self.pnode.getChild(0).setScale(15)
            self.pnode.setH(-90)
            self.pnode.reparentTo(g.render)

        if self.get_latest_event(RenderTowerPosition):
            self.pnode.setPos(self.pos[0], self.pos[1], 0)

        if self.get_latest_event(RenderTowerAttack):
            pass
