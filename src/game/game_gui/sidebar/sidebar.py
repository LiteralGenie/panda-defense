from typing import ClassVar

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.tower_grid import TowerGrid


class Sidebar(BetterDirectFrame):
    GRID_COLS: ClassVar[int] = 2

    tower_grid: TowerGrid

    def __init__(self, parent: BetterDirectFrame):
        super().__init__(
            parent,
            frameColor=(0, 0, 0, 0),
        )

        self.tower_grid = TowerGrid(
            self,
            num_cols=self.GRID_COLS,
        )
        for _ in range(7):
            self.tower_grid.create_tile(
                recalculate_layout=False,
            )

    def recalculate_layout(self):
        self.tower_grid.set_frame_size((self.width, self.height))
        self.tower_grid.recalculate_layout()

    def delete(self):
        self.tower_grid.delete()
