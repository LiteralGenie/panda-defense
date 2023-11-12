from typing import ClassVar

from direct.gui.DirectGui import DGG
from direct.interval.LerpInterval import LerpFunc

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.sidebar import Sidebar
from game.game_gui.tower_details_pane import TowerDetailsPane
from utils.gui_utils import get_h, get_w
from utils.types import IntervalDict


class GameGui(BetterDirectFrame):
    # Percentage of viewport width
    DETAILS_WIDTH: ClassVar[float] = 0.15
    # Percentage of viewport width
    SIDEBAR_WIDTH: ClassVar[float] = 0.20

    details_pane: TowerDetailsPane
    sidebar: Sidebar

    _intervals: IntervalDict
    _sidebar_visible: bool

    def __init__(self):
        super().__init__(
            aspect2d,  # type: ignore
            state=DGG.NORMAL,
        )

        self.sidebar = Sidebar(self)
        self.details_pane = TowerDetailsPane(self)

        self._intervals = dict()

        # On window resize, reposition / resize everything
        self.accept("aspectRatioChanged", lambda: self.recalculate_layout())

        # When a tower is clicked, swap out the sidebar with the tower description
        self._sidebar_visible = True
        self.accept(
            "showTowerDetails",
            lambda: [
                self._hide_sidebar(),
                self._show_tower_details(),
            ],
        )
        self.accept(
            "hideTowerDetails",
            lambda: [
                self._hide_tower_details(),
                self._show_sidebar(),
            ],
        )

    def recalculate_layout(self):
        """Set origin to top-left and fill screen"""

        min_x = base.a2dLeft
        max_x = base.a2dRight
        vw = max_x - min_x

        min_y = base.a2dBottom
        max_y = base.a2dTop
        vh = max_y - min_y

        self.set_pos((min_x, 0, max_y))
        self.set_frame_size((vw, -vh))

        self._layout_sidebar()
        self._layout_details_pane()

    def _layout_sidebar(self):
        """Anchor sidebar to right edge"""

        vw = get_w(self)
        vh = get_h(self)

        w = self.SIDEBAR_WIDTH * vw
        h = vh

        self.sidebar.set_frame_size((w, h))
        self.sidebar.recalculate_layout()

        if self._sidebar_visible:
            self._show_sidebar(animate=False)
        else:
            self._hide_sidebar(animate=False)

    def _layout_details_pane(self):
        vw = get_w(self)
        vh = get_h(self)

        w = self.DETAILS_WIDTH * vw
        h = vh

        self.details_pane.set_frame_size((w, h))
        self.details_pane.recalculate_layout()

        if not self._sidebar_visible:
            self._show_tower_details(animate=False)
        else:
            self._hide_tower_details(animate=False)

    def _show_sidebar(self, animate: bool = True):
        self._sidebar_visible = True

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

    def _hide_sidebar(self, animate: bool = True):
        self._sidebar_visible = False

        def cb():
            start_x = self.sidebar.get_pos()[0]
            start_y = self.sidebar.get_pos()[2]
            end_x = get_w(self)
            width = end_x - start_x

            def inner(t: float):
                current_x = start_x + width * t
                self.sidebar.set_pos((current_x, 0, start_y))

            return inner

        LerpFunc(
            cb(),
            duration=0.2 if animate else 0,
            fromData=0,
            toData=1,
            blendType="easeInOut",
        ).start()

    def _show_tower_details(self, animate: bool = True):
        print("_show_tower_details()")

        def cb():
            vw = get_w(self)
            w = self.DETAILS_WIDTH * vw
            start_x = vw
            start_y = 0

            self.details_pane.set_xy((start_x, start_y))

            def inner(t: float):
                current_x = vw - w * t
                self.details_pane.set_pos((current_x, 0, start_y))

            return inner

        LerpFunc(
            cb(),
            duration=0.2 if animate else 0,
            fromData=0,
            toData=1,
            blendType="easeInOut",
        ).start()

    def _hide_tower_details(self, animate: bool = True):
        print("_hide_tower_details()")

        def cb():
            start_x = self.details_pane.get_pos()[0]
            start_y = self.details_pane.get_pos()[2]
            end_x = get_w(self)
            width = end_x - start_x

            def inner(t: float):
                current_x = start_x + width * t
                self.details_pane.set_pos((current_x, 0, start_y))

            return inner

        LerpFunc(
            cb(),
            duration=0.2 if animate else 0,
            fromData=0,
            toData=1,
            blendType="easeInOut",
        ).start()

    def delete(self):
        super().delete()
        self.sidebar.delete()
