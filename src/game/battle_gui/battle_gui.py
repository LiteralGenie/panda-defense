from typing import ClassVar

from direct.gui.DirectGui import DGG, DirectFrame
from direct.showbase.DirectObject import DirectObject

import g
from game.battle_gui.tower_grid import TowerGrid
from utils.gui_utils import get_w, set_relative_frame_size


class BattleGui(DirectObject):
    sidebar: DirectFrame
    sidebar: DirectFrame
    tower_grid: TowerGrid

    # Percentage of viewport width
    ROOT_WIDTH: ClassVar[float] = 0.1
    TILE_COLS: ClassVar[int] = 2
    # Relative to side length of each tile
    TILE_GAP_PERCENT: ClassVar[float] = 0.05

    def __init__(self):
        self._init_nodes()
        self._recalculate_layout()

        self.accept("aspectRatioChanged", lambda: self._recalculate_layout())

    def _init_nodes(self):
        self.sidebar = DirectFrame(
            g.aspect2d,
            frameColor=(0, 1, 0, 0.5),
            state=DGG.NORMAL,
        )
        # self.root.bind(
        #     DGG.B1PRESS, lambda *args, **kwargs: print("root B1PRESS"), [self.root]
        # )
        # self.root.bind(
        #     DGG.B1RELEASE, lambda *args, **kwargs: print("root B1RELEASE"), [self.root]
        # )
        # self.root.bind(DGG.CURSORMOVE, lambda _: print("root CURSORMOVE"))
        # self.root.bind(DGG.WITHIN, lambda _: print("root WITHIN"))
        # self.root.bind(DGG.WITHOUT, lambda _: print("root WITHOUT"))

        self.tower_grid = TowerGrid(
            parent=self.sidebar,
            num_cols=self.TILE_COLS,
            gap_percent=self.TILE_GAP_PERCENT,
        )
        for _ in range(7):
            self.tower_grid.create_tile(
                recalculate_layout=False,
            )

    def delete(self):
        pass

    def _recalculate_layout(self):
        # Constants
        min_x = -g.base.get_aspect_ratio()
        max_x = -min_x
        vp_width = max_x - min_x

        min_y = -1
        max_y = 1
        vp_height = max_y - min_y

        vp_wh = (vp_width, vp_height)

        # Create invisible global layer for capturing events
        self.sidebar["frameSize"] = (min_x, max_x, min_y, max_y)

        # Create pane pinned to right, with origin at top-left
        set_relative_frame_size(self.sidebar, vp_wh, (0.1, -1))
        self.sidebar.set_pos((max_x - get_w(self.sidebar), 0, max_y))

        self.tower_grid.recalculate_layout()
