from abc import ABC

from direct.actor.Actor import Actor
from panda3d.core import NodePath

from game.range import PyramidalRange, Range
from game.scenario import Point
from game.stateful import Stateful, StatefulProp


class Tower(Stateful, ABC):
    pnode: Actor | None

    pos: Point = StatefulProp()  # type: ignore
    range: Range

    def __init__(self, pos: Point):
        super().__init__()
        self.pnode = None

        self.pos = pos
        self.range = PyramidalRange(2)

    def render(self, parent: NodePath, period_s: float):
        if not self.pnode:
            self.pnode = Actor(
                "data/assets/glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf",
                dict(),
            )
            self.pnode.getChild(0).setScale(15)
            self.pnode.setH(-90)
            self.pnode.reparentTo(parent)

        if self.state["pos"].needs_check:
            self.pnode.setPos(self.pos[0], self.pos[1], 0)

        super().save_props()
