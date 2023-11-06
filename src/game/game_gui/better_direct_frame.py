from typing import Any

from direct.gui.DirectFrame import DirectFrame

from utils.gui_utils import get_h, get_w


class BetterDirectFrame(DirectFrame):
    def __init__(self, parent: DirectFrame, **kwargs: Any):
        super().__init__(parent, **kwargs)
        super().initialiseoptions(self.__class__)

    def set_xy(self, xy: tuple[float, float]):
        x, y = xy
        return self.set_pos((x, 0, y))

    def set_frame_size(self, wh: tuple[float, float]):
        w, h = wh
        self["frameSize"] = (0, w, 0, h)

    @property
    def width(self) -> float:
        return get_w(self)

    @property
    def height(self) -> float:
        return get_h(self)
