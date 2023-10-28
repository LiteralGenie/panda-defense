from typing import ClassVar

from panda3d.core import PandaNode

from g import render


class Renderable:
    pnode_factory: ClassVar[PandaNode]

    pnode: PandaNode | None

    def __init__(self):
        self.pnode = None

        if True:
            self.pnode = self.pnode_factory()
            render.addChild(self.pnode)
