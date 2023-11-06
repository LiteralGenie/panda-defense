from typing import ClassVar

from panda3d.core import NodePath

import g


class MapView:
    model: ClassVar[NodePath] = g.loader.loadModel("data/assets/board.gltf")

    pnode: NodePath

    def __init__(self):
        super().__init__()

        self.pnode = self._init_model()

    def _init_model(self):
        pnode = NodePath("")

        for idx_row in range(-15, 15):
            for idx_col in range(-15, 15):
                b = pnode.attachNewNode("")
                b.setPos(idx_col * 2 - 0.5, idx_row * 2 - 0.5, 0)
                self.model.instance_to(b)

        pnode.reparent_to(g.render)

        return pnode

    def render(self, *_):
        pass
