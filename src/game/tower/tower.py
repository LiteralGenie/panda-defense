from abc import ABC
from typing import TYPE_CHECKING

from game.range import Range
from game.renderable import Renderable
from game.scenario import Point
from game.tower.render_tower_events import RenderTowerEvents, RenderTowerPosition

if TYPE_CHECKING:
    from direct.actor.Actor import Actor


class Tower(Renderable[RenderTowerEvents, "Actor"], ABC):
    pos: Point
    range: Range

    def __init__(self, pos: Point, range: Range):
        super().__init__()
        self.pnode = None

        self.pos = pos
        self.range = range

    def render(self, period_s: float):
        from direct.actor.Actor import Actor

        import g

        if not self.pnode:
            self.pnode = Actor(
                "data/assets/glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf",
                dict(),
            )
            self.pnode.getChild(0).setScale(15)
            self.pnode.setH(-90)
            self.pnode.reparentTo(g.render)

        if self.get_latest_event(RenderTowerPosition):
            self.pnode.setPos(self.pos[0], self.pos[1], 0)
