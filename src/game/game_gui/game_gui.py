from typing import ClassVar

from direct.interval.LerpInterval import LerpFunc

import g
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.sidebar import Sidebar
from game.towers.tower_view import TowerView
from utils.gui_utils import get_h, get_w
from utils.types import IntervalDict


class GameGui(BetterDirectFrame):
    # Percentage of viewport width
    SIDEBAR_WIDTH: ClassVar[float] = 0.20

    sidebar: Sidebar

    _intervals: IntervalDict
    _sidebar_visible: bool

    def __init__(self):
        super().__init__(g.aspect2d)

        self.sidebar = Sidebar(self)

        self._intervals = dict()
        self._sidebar_visible = True

        self.recalculate_layout()
        self.accept("aspectRatioChanged", lambda: self.recalculate_layout())

        self.accept("showTowerDetails", lambda: self.recalculate_layout())
        self.accept("hideTowerDetails", lambda: self.recalculate_layout())

    def recalculate_layout(self):
        """Set origin to top-left and fill screen"""

        min_x = g.base.a2dLeft
        max_x = g.base.a2dRight
        vw = max_x - min_x

        min_y = g.base.a2dBottom
        max_y = g.base.a2dTop
        vh = max_y - min_y

        self.set_pos((min_x, 0, max_y))
        self.set_frame_size((vw, vh))

        self._layout_sidebar()

    def _layout_sidebar(self):
        """Anchor sidebar to right edge"""

        vw = get_w(self)
        vh = get_h(self)

        w = self.SIDEBAR_WIDTH * vw
        h = -vh

        self.sidebar.set_frame_size((w, h))
        self.sidebar.recalculate_layout()

        if self._sidebar_visible:
            self._show_sidebar(animate=False)
        else:
            self._hide_sidebar()

    def _show_sidebar(self, animate: bool = True):
        def cb():
            vw = get_w(self)
            w = self.SIDEBAR_WIDTH * vw
            start_x = vw
            start_y = 0

            self.sidebar.set_xy((start_x, start_y))

            def inner(t: float):
                current_x = vw - w * t
                self.sidebar.set_pos((current_x, 0, start_y))

            return inner

        LerpFunc(
            cb(),
            duration=0.2 if animate else 0,
            fromData=0,
            toData=1,
            blendType="easeInOut",
        ).start()

    def _hide_sidebar(self):
        def cb():
            start_x = self.sidebar.get_pos()[0]
            start_y = self.sidebar.get_pos()[2]
            width = self.sidebar.width

            def inner(t: float):
                current_x = start_x + width * t
                self.sidebar.set_pos((current_x, 0, start_y))

            return inner

        LerpFunc(
            cb(),
            duration=0.2,
            fromData=0,
            toData=1,
            blendType="easeInOut",
        ).start()

    def _show_tower_details(self, view: TowerView):
        self._hide_sidebar()

    def _hide_tower_details(self):
        self._show_sidebar()

    def delete(self):
        self.sidebar.delete()
