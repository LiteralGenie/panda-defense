from direct.gui.DirectGui import DirectFrame
from panda3d.core import TextNode

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.tower_tile import TowerTile
from utils.gui_utils import get_w


class TowerGrid:
    """Grid of square tiles, filling top rows first"""

    parent: DirectFrame
    grid_container: BetterDirectFrame
    children: list[TowerTile]

    gap_percent: float
    num_cols: int

    def __init__(
        self,
        parent: DirectFrame,
        num_cols: int,
        gap_percent: float,
    ):
        self.parent = parent
        self.grid_container = BetterDirectFrame(parent)
        self.children = []

        self.gap_percent = gap_percent
        self.num_cols = num_cols

    def recalculate_layout(self):
        for i in range(len(self.children)):
            self._recalculate_child_layout(i)

    def create_tile(self, recalculate_layout: bool = True):
        idx = len(self.children)
        self.children.append(
            TowerTile(
                parent=self.grid_container,
                text=f"T{idx}",
                text_scale=0.05,
                text_align=TextNode.ACenter,
                text_pos=(0.0, 0.0),
            )
        )

        if recalculate_layout:
            self._recalculate_child_layout(len(self.children) - 1)

    def delete(self):
        for child in self.children:
            child.delete()

    def _recalculate_child_layout(self, idx: int):
        child = self.children[idx]
        row = int(idx / 2)
        col = idx % 2

        pad_l = (col + 1) * self._gap_length
        tl_x = col * self._side_length + pad_l

        pad_t = (row + 1) * self._gap_length
        tl_y = row * self._side_length + pad_t
        tl_y = -tl_y

        child.set_xy((tl_x, tl_y))

        child.set_frame_size(((self._side_length), -self._side_length))

        half_sl = (self._side_length) / 2
        child["text_pos"] = (half_sl, -(half_sl + self._gap_length))
        child["frameColor"] = (
            idx / (len(self.children) - 1),
            0,
            0,
            0.5,
        )

    @property
    def _side_length(self) -> float:
        cw = get_w(self.parent)

        # Treat each gap as a partial tile
        gap_width_tiles = self.gap_percent * (self.num_cols + 1)
        total_width_tiles = self.num_cols + gap_width_tiles

        length = cw / total_width_tiles
        return length

    @property
    def _gap_length(self) -> float:
        result = self._side_length * self.gap_percent
        return result
