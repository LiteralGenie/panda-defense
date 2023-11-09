from typing import ClassVar

import g
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.sidebar import Sidebar
from game.game_gui.status_list.build_timer_status import BuildTimerStatus
from game.game_gui.status_list.enemy_status import EnemyStatus
from game.game_gui.status_list.gold_status import GoldStatus
from game.game_gui.status_list.health_status import HealthStatus
from game.game_gui.status_list.round_status import RoundStatus
from game.game_gui.status_list.status_list import StatusList
from utils.gui_utils import get_h, get_w


class GameGui(BetterDirectFrame):
    # Percentage of viewport width
    SIDEBAR_WIDTH: ClassVar[float] = 0.1
    # Percentage of viewport width
    STATUS_WIDTH: ClassVar[float] = 0.07
    # Percentage of width per status in list
    STATUS_HEIGHT: ClassVar[float] = 0.35
    # Percentage of width
    STATUS_OFFSET: ClassVar[float] = 0.1
    # Percentage of status width
    INTER_STATUS_GAP: ClassVar[float] = 0.125

    sidebar: Sidebar
    basic_status: StatusList

    def __init__(self):
        super().__init__(
            g.aspect2d,
            frameColor=(0, 0, 0, 0),
        )

        self.sidebar = Sidebar(self)
        self.basic_status = StatusList(
            self,
            labels=[
                HealthStatus(self),
                GoldStatus(self),
            ],
        )

        self.wave_status = StatusList(
            self,
            labels=[
                RoundStatus(self),
                EnemyStatus(self),
                BuildTimerStatus(self),
            ],
        )

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
        self._layout_basic_status(self.sidebar)
        self._layout_wave_status(self.sidebar, self.basic_status)

    def _layout_sidebar(self):
        vw = get_w(self)
        vh = get_h(self)

        # Anchor sidebar to right edge
        w = self.SIDEBAR_WIDTH * vw

        self.sidebar.set_xy((vw - w, 0))
        self.sidebar.set_frame_size((w, -vh))
        self.sidebar.recalculate_layout()

    def _layout_basic_status(self, sidebar: Sidebar):
        vw = get_w(self)

        # Anchor status displays left of sidebar
        w = self.STATUS_WIDTH * vw
        h = self.STATUS_HEIGHT * w * len(self.basic_status.labels)

        offset = self.STATUS_OFFSET * w
        tl_x = sidebar.x - w - offset
        tl_y = -offset

        self.basic_status.set_xy((tl_x, tl_y))
        self.basic_status.set_frame_size((w, -h))
        self.basic_status.recalculate_layout()

    def _layout_wave_status(self, sidebar: Sidebar, basic_status: StatusList):
        vw = get_w(self)

        w = self.STATUS_WIDTH * vw
        h = self.STATUS_HEIGHT * w * len(self.wave_status.labels)

        # Anchor status displays left of sidebar
        offset_x = self.STATUS_OFFSET * w
        tl_x = sidebar.x - w - offset_x

        # Anchor underneath basic status list
        offset_y = self.INTER_STATUS_GAP * w
        tl_y = basic_status.y + basic_status.height - offset_y

        self.wave_status.set_xy((tl_x, tl_y))
        self.wave_status.set_frame_size((w, -h))
        self.wave_status.recalculate_layout()

    def delete(self):
        self.sidebar.delete()
        self.basic_status.delete()
