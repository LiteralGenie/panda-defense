from typing import ClassVar

from panda3d.core import NodePath

from game.view.game_view_globals import GVG
from game.view.procgen.square import build_rect


class MapView:
    model: ClassVar[NodePath] = loader.loadModel("data/assets/board.gltf")

    pnode: NodePath

    def __init__(self):
        super().__init__()

        self.pnode = self._init_model()

    def _init_model(self):
        pnode = NodePath("")

        tiles = [
            self.load_tile((0.60, 0.60, 0.60, 1)),
            self.load_tile((0.06, 0.06, 0.06, 1)),
        ]

        size = 61
        half = size // 2

        for r in range(size):
            idx_row = r - half
            for c in range(size):
                idx_col = c - half

                idx = r * size + c

                idx_tile = idx % len(tiles)
                tile = tiles[idx_tile]

                t = pnode.attachNewNode("")
                t.setPos(idx_col, idx_row, 0)
                tile.instance_to(t)

        pnode.reparent_to(render)

        return pnode

    @classmethod
    def load_tile(cls, color: tuple[float, float, float, float]):
        def factory():
            square = build_rect(color)
            return square

        return GVG.resource_mgr.load_or_register(f"map_tile_{color}", factory)
