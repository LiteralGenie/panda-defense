from typing import ClassVar

import g
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.sidebar import Sidebar
from utils.gui_utils import get_h, get_w
from utils.types import IntervalDict


class GameGui(BetterDirectFrame):
    # Percentage of viewport width
    SIDEBAR_WIDTH: ClassVar[float] = 0.20

    sidebar: Sidebar

    _intervals: IntervalDict

    def __init__(self):
        super().__init__(g.aspect2d)

        self.sidebar = Sidebar(self)

        self._intervals = dict()

        self.recalculate_layout()
        self.accept("aspectRatioChanged", lambda: self.recalculate_layout())

    def recalculate_layout(self):
        min_x = g.base.a2dLeft
        max_x = g.base.a2dRight
        vw = max_x - min_x

        min_y = g.base.a2dBottom
        max_y = g.base.a2dTop
        vh = max_y - min_y

        # Set origin to top-left and fill screen
        self.set_pos((min_x, 0, max_y))
        self.set_frame_size((vw, vh))

        self._layout_sidebar()

    def _layout_sidebar(self):
        # Anchor sidebar to right edge
        vw = get_w(self)
        vh = get_h(self)

        w = self.SIDEBAR_WIDTH * vw

        self.sidebar.set_xy((vw - w, 0))
        self.sidebar.set_frame_size((w, -vh))
        self.sidebar.recalculate_layout()

    def delete(self):
        self.sidebar.delete()
