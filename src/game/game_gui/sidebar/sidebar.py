from typing import ClassVar

from direct.gui.DirectFrame import DirectFrame
from direct.gui.DirectGui import DGG, DirectFrame

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.tower_grid import TowerGrid
from utils.gui_utils import get_h, get_w


class Sidebar(BetterDirectFrame):
    # Percentage of viewport width
    SIDEBAR_WIDTH: ClassVar[float] = 0.1
    TILE_COLS: ClassVar[int] = 2
    # Relative to side length of each tile
    TILE_GAP_PERCENT: ClassVar[float] = 0.05

    tower_grid: TowerGrid

    def __init__(self, parent: DirectFrame):
        super().__init__(
            parent,
            frameColor=(0, 1, 0, 0.5),
            state=DGG.NORMAL,
        )

        self.tower_grid = TowerGrid(
            self,
            num_cols=self.TILE_COLS,
            gap_percent=self.TILE_GAP_PERCENT,
        )
        for _ in range(7):
            self.tower_grid.create_tile(
                recalculate_layout=False,
            )

    def recalculate_layout(self):
        cw = get_w(self.parent_frame)
        ch = get_h(self.parent_frame)

        actual_width = self.SIDEBAR_WIDTH * cw

        # Create rectangular pane on right edge, with origin at top-left
        tl_x = cw - actual_width
        tl_y = ch
        self.set_xy((tl_x, tl_y))

        w = actual_width
        h = -ch
        self.set_frame_size((w, h))

        self.tower_grid.recalculate_layout()

    def delete(self):
        self.tower_grid.delete()
