from direct.actor.Actor import Actor
from panda3d.core import NodePath

from renderable import Renderable


class Tower(Renderable):
    def __init__(self):
        super().__init__()

    def render(self, parent: NodePath):
        if not self.pnode:
            self.pnode = Actor(
                "data/assets/glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf",
                dict(),
            )
            self.pnode.getChild(0).setScale(15)

            self.pnode.setPos(1, 1, 0)
            self.pnode.setH(-90)

            self.pnode.reparentTo(parent)
