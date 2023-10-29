from direct.actor.Actor import Actor
from panda3d.core import NodePath

from renderable import Renderable


class Unit(Renderable):
    def __init__(self):
        super().__init__()

    def render(self, parent: NodePath):
        if not self.pnode:
            self.pnode = Actor(
                "data/assets/glTF-Sample-Models/2.0/BoomBox/glTF/BoomBox.gltf"
            )
            self.pnode.getChild(0).setPos(0, -0.25, 0)
            self.pnode.getChild(0).setScale(20)

            self.pnode.setPos(0, 4, 0)

            self.pnode.reparentTo(parent)
