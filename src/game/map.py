from typing import TYPE_CHECKING

from game.renderable import Renderable

if TYPE_CHECKING:
    from panda3d.core import NodePath


class Map(Renderable[None, "NodePath"]):
    def __init__(self):
        super().__init__()

    def render(self, period_s: float):
        from panda3d.core import NodePath

        import g

        if not self.pnode:
            self.pnode = NodePath("")

            board = g.loader.loadModel("data/assets/board.gltf")
            for idx_row in range(-15, 15):
                for idx_col in range(-15, 15):
                    b = self.pnode.attachNewNode("")
                    b.setPos(idx_col * 2, idx_row * 2, 0)
                    board.instanceTo(b)

            self.pnode.reparentTo(g.render)
