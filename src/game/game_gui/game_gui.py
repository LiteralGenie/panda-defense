from typing import ClassVar

import g
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.sidebar import Sidebar


class GameGui(BetterDirectFrame):
    # Percentage of viewport width
    SIDEBAR_WIDTH: ClassVar[float] = 0.1

    sidebar: Sidebar

    def __init__(self):
        super().__init__(
            g.aspect2d,
            frameColor=(0, 0, 0, 0),
        )

        self.sidebar = Sidebar(self)

        self.recalculate_layout()
        self.accept("aspectRatioChanged", lambda: self.recalculate_layout())

    def recalculate_layout(self):
        min_x = -g.base.get_aspect_ratio()
        max_x = g.base.get_aspect_ratio()
        w = max_x - min_x

        min_y = -1
        max_y = 1
        h = max_y - min_y

        # Set origin to top-left and fill screen
        self.set_pos((min_x, 0, max_y))
        self.set_frame_size((w, h))

        # Anchor sidebar to right edge
        sw = self.SIDEBAR_WIDTH * w
        self.sidebar.set_xy((w - sw, 0))
        self.sidebar.set_frame_size((sw, -h))
        self.sidebar.recalculate_layout()

    def delete(self):
        self.sidebar.delete()
