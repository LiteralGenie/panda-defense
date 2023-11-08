import g
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.sidebar import Sidebar
from utils.gui_utils import set_frame_size


class GameGui(BetterDirectFrame):
    sidebar: Sidebar

    def __init__(self):
        super().__init__(g.aspect2d, frameColor=(0, 0, 0, 0))

        self.sidebar = Sidebar(self)

        self._recalculate_layout()
        self.accept("aspectRatioChanged", lambda: self._recalculate_layout())

    def _recalculate_layout(self):
        # Set origin to top-left and fill screen
        min_x = -g.base.get_aspect_ratio()
        max_x = g.base.get_aspect_ratio()
        w = max_x - min_x

        min_y = -1
        max_y = 1
        h = max_y - min_y

        self.set_pos((min_x, 0, min_y))
        set_frame_size(self, (w, h))

        self.sidebar.recalculate_layout()

    def delete(self):
        self.sidebar.delete()
