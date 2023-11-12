from typing import ClassVar

from direct.gui.DirectGui import DGG

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.sidebar import Sidebar
from game.game_gui.tower_details.tower_details_pane import TowerDetailsPane
from utils.gui_utils import get_h, get_w
from utils.types import IntervalDict


class GameGui(BetterDirectFrame):
    # Percentage of viewport width
    DETAILS_WIDTH: ClassVar[float] = 0.27
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
        self.recalculate_layout()
        self.accept("aspectRatioChanged", lambda: self.recalculate_layout())

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

        tl_x = vw - w
        tl_y = 0

        self.sidebar.set_xy((tl_x, tl_y))
        self.sidebar.set_frame_size((w, h))
        self.sidebar.recalculate_layout()

    def _layout_details_pane(self):
        vw = get_w(self)
        vh = get_h(self)

        w = self.DETAILS_WIDTH * vw
        h = vh

        tl_x = vw - w
        tl_y = 0

        self.details_pane.set_xy((tl_x, tl_y))
        self.details_pane.set_frame_size((w, h))
        self.details_pane.recalculate_layout()

    def delete(self):
        super().delete()
        self.sidebar.delete()
