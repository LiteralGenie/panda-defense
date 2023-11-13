from hsluv import hsluv_to_rgb
from panda3d.core import NodePath

from game.view.game_view_globals import GVG
from game.view.procgen.square import build_rect
from utils.types import Point2


class MapView:
    pnode: NodePath

    def __init__(self):
        super().__init__()

        self.pnode = self._init_model()

    def _init_model(self):
        pnode = NodePath("")
        pnode.reparent_to(render)

        ppaths: list[list[Point2]] = []
        for ppath in GVG.data.ppaths.values():
            ppaths.append([pt.pos for pt in ppath.points])

        tiles = [
            self.load_tile((0.60, 0.60, 0.60, 1)),
            self.load_tile((0.06, 0.06, 0.06, 1)),
        ]

        size = 61
        half = size // 2

        # Draw map tiles
        for r in range(size):
            idx_row = r - half
            for c in range(size):
                idx_col = c - half

                is_path_tile = any((idx_col, idx_row) in path for path in ppaths)
                if is_path_tile:
                    continue

                i = r * size + c

                idx_tile = i % len(tiles)
                tile = tiles[idx_tile]

                t = pnode.attachNewNode("")
                t.setPos(idx_col, idx_row, 0)
                tile.instance_to(t)

        # Draw path tiles
        base_color = (25, 40, 66)
        sat_step = (100 - base_color[1]) / (len(ppaths))
        lum_step = -0.5

        for i, ppath in enumerate(ppaths):
            for j, pos in enumerate(ppath):
                tile_color = (
                    base_color[0],
                    base_color[1] + i * sat_step,
                    base_color[2] + j * lum_step,
                )
                tile_color_rgb = hsluv_to_rgb(list(tile_color)) + (0.75,)  # type: ignore
                tile = self.load_tile(tile_color_rgb)

                t = pnode.attachNewNode("")
                t.setPos(pos + (0,))
                tile.instance_to(t)

        return pnode

    @classmethod
    def load_tile(cls, color: tuple[float, float, float, float]):
        def factory():
            square = build_rect(color)
            return square

        return GVG.resource_mgr.load_or_register(f"map_tile_{color}", factory)
