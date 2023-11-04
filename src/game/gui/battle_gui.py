from typing import Any, ClassVar

from direct.gui.DirectGui import DirectFrame
from direct.showbase import DirectObject
from panda3d.core import NodePath, TextNode

import g
from game.gui.nested_direct_frame import NestedDirectFrame
from utils.gui_utils import get_w, set_relative_frame_size


class BattleGui(DirectObject.DirectObject):
    root: NodePath
    tower_grid: "TowerGrid"

    # Percentage of viewport width
    ROOT_WIDTH: ClassVar[float] = 0.1
    TILE_COLS: ClassVar[int] = 2
    # Relative to side length of each tile
    TILE_GAP_PERCENT: ClassVar[float] = 0.05

    def __init__(self):
        self._init_nodes()
        self.recalculate_layout()

        self.accept("aspectRatioChanged", lambda: self.recalculate_layout())

    def _init_nodes(self):
        self.root = DirectFrame(
            g.aspect2d,
            frameColor=(0, 1, 0, 0.5),
        )

        self.tower_grid = TowerGrid(
            gap_percent=self.TILE_GAP_PERCENT,
            num_cols=self.TILE_COLS,
            parent=self.root,
        )
        for _ in range(7):
            self.tower_grid.create_tile(
                recalculate_layout=False,
            )

    def delete(self):
        pass

    def recalculate_layout(self):
        # Constants
        min_x = -g.base.get_aspect_ratio()
        max_x = -min_x
        vp_width = max_x - min_x

        min_y = -1
        max_y = 1
        vp_height = max_y - min_y

        vp_wh = (vp_width, vp_height)

        # Create pane pinned to right, with origin at top-left
        set_relative_frame_size(self.root, vp_wh, (0.1, -1))
        self.root.set_pos((max_x - get_w(self.root), 0, max_y))

        self.tower_grid.recalculate_layout()


class TowerGrid:
    """Grid of square tiles, filling top rows first"""

    parent: DirectFrame
    grid_container: NestedDirectFrame
    children: list[NestedDirectFrame]

    gap_percent: float
    num_cols: int

    def __init__(
        self,
        parent: DirectFrame,
        num_cols: int,
        gap_percent: float,
    ):
        self.parent = parent
        self.grid_container = NestedDirectFrame(parent)
        self.children = []

        self.gap_percent = gap_percent
        self.num_cols = num_cols

    def recalculate_layout(self):
        for i in range(len(self.children)):
            self._recalculate_child_layout(i)

    def create_tile(self, recalculate_layout: bool = True, **kwargs: Any):
        idx = len(self.children)
        self.children.append(
            NestedDirectFrame(
                self.grid_container,
                text=f"T{idx}",
                text_scale=0.05,
                text_align=TextNode.ACenter,
                text_pos=(0.0, 0.0),
                **kwargs,
            )
        )

        if recalculate_layout:
            self._recalculate_child_layout(len(self.children) - 1)

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
        child.inner_frame["text_pos"] = (half_sl, -(half_sl + self._gap_length))
        child.inner_frame["frameColor"] = (idx / (len(self.children) - 1), 0, 0, 0.5)

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
