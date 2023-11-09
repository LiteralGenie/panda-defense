from typing import ClassVar

from panda3d.core import TextNode

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.tower_tile import TowerTile
from game.towers.basic.basic_tower_model import BasicTowerModel
from game.towers.basic.basic_tower_view import BasicTowerView
from utils.gui_utils import get_w


class TowerGrid(BetterDirectFrame):
    """Grid of square tiles, filling top rows first"""

    # Relative to side length of each tile
    GAP_PERCENT: ClassVar[float] = 0.05

    cells: list[TowerTile]
    num_cols: int

    def __init__(
        self,
        parent: BetterDirectFrame,
        num_cols: int,
    ):
        super().__init__(
            parent,
            frameColor=(0, 0, 0, 0.95),
        )

        self.cells = []
        self.num_cols = num_cols

    def recalculate_layout(self):
        for i in range(len(self.cells)):
            self._recalculate_child_layout(i)

    def create_tile(self, recalculate_layout: bool = True):
        idx = len(self.cells)

        self.cells.append(
            TowerTile(
                self,
                BasicTowerModel,
                BasicTowerView,
                text=f"T{idx}",
                text_scale=0.05,
                text_align=TextNode.ACenter,
                text_pos=(0.0, 0.0),
            )
        )

        if recalculate_layout:
            self._recalculate_child_layout(idx)

    def delete(self):
        for child in self.cells:
            child.delete()

    def _recalculate_child_layout(self, idx: int):
        cell = self.cells[idx]
        row = int(idx / 2)
        col = idx % 2

        pad_l = (col + 1) * self._gap_length
        tl_x = col * self._side_length + pad_l

        pad_t = (row + 1) * self._gap_length
        tl_y = row * self._side_length + pad_t
        tl_y = -tl_y

        cell.set_xy((tl_x, tl_y))

        cell.set_frame_size(((self._side_length), -self._side_length))

        half_sl = (self._side_length) / 2
        cell["text_pos"] = (half_sl, -(half_sl + self._gap_length))
        cell["frameColor"] = (
            (idx + 3) / (len(self.cells) - 1 + 5),
            (idx + 3) / (len(self.cells) - 1 + 5),
            (idx + 3) / (len(self.cells) - 1 + 5),
            0.8,
        )

    @property
    def _side_length(self) -> float:
        cw = get_w(self)

        # Treat each gap as a partial tile
        gap_width_tiles = self.GAP_PERCENT * (self.num_cols + 1)
        total_width_tiles = self.num_cols + gap_width_tiles

        length = cw / total_width_tiles
        return length

    @property
    def _gap_length(self) -> float:
        result = self._side_length * self.GAP_PERCENT
        return result
