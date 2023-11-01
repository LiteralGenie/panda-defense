from direct.actor.Actor import Actor
from panda3d.core import NodePath, Point3

from game.parameterized_path import ParameterizedPath
from game.renderable import Renderable, StatefulProp


class Unit(Renderable):
    dist: int = StatefulProp()
    intervals: dict
    path: ParameterizedPath
    speed: int

    def __init__(self, path: ParameterizedPath, speed: int):
        super().__init__()

        self.dist = 0
        self.path = path
        self.intervals = dict()
        self.speed = speed

    def render(self, parent: NodePath, period_s: float):
        if not self.pnode:
            self.pnode = Actor(
                "data/assets/glTF-Sample-Models/2.0/BoomBox/glTF/BoomBox.gltf"
            )
            self.pnode.getChild(0).setScale(20)
            self.pnode.reparentTo(parent)

        if self.state["dist"].needs_check:
            coords = self.path.points[self.dist]

            if ivl := self.intervals.get("pos"):
                ivl.pause()

            self.intervals["pos"] = self.pnode.posInterval(
                period_s,
                Point3(coords[0], coords[1], 0),
            )
            self.intervals["pos"].start()

        super().save_props()

    def delete(self):
        self.pnode.cleanup()
        self.pnode.removeNode()
