from typing import ClassVar

import g
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.sidebar import Sidebar
from game.game_gui.status_box.status_list import StatusList


class GameGui(BetterDirectFrame):
    # Percentage of viewport width
    SIDEBAR_WIDTH: ClassVar[float] = 0.1
    # Percentage of viewport width
    STATUS_WIDTH: ClassVar[float] = 0.07
    # Percentage of width
    STATUS_HEIGHT: ClassVar[float] = 1.05
    # Percentage of width
    STATUS_OFFSET: ClassVar[float] = 0.1

    sidebar: Sidebar
    status_list: StatusList

    def __init__(self):
        super().__init__(
            g.aspect2d,
            frameColor=(0, 0, 0, 0),
        )

        self.sidebar = Sidebar(self)
        self.status_list = StatusList(self)

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

        # Track right edge
        curr_x = vw

        # Anchor sidebar to right edge
        sw = self.SIDEBAR_WIDTH * vw
        curr_x -= sw

        self.sidebar.set_xy((curr_x, 0))
        self.sidebar.set_frame_size((sw, -vh))
        self.sidebar.recalculate_layout()

        # Anchor status displays left of sidebar
        sw = self.STATUS_WIDTH * vw
        sh = self.STATUS_HEIGHT * sw
        curr_x -= sw

        offset = self.STATUS_OFFSET * sw
        curr_x -= offset

        self.status_list.set_xy((curr_x, -offset))
        self.status_list.set_frame_size((sw, -sh))
        self.status_list.recalculate_layout()

    def delete(self):
        self.sidebar.delete()
        self.status_list.delete()
