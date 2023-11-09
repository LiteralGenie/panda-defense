from typing import Any

from direct.gui.DirectFrame import DirectFrame

from utils.gui_utils import get_h, get_w


class BetterDirectFrame(DirectFrame):
    parent_frame: DirectFrame

    def __init__(
        self,
        parent: "BetterDirectFrame",
        frameColor: tuple[float, float, float, float] = (0, 0, 0, 0),
        **kwargs: Any,
    ):
        super().__init__(parent, frameColor=frameColor, **kwargs)
        super().initialiseoptions(self.__class__)

        # Because self.parent is the parent arg wrapped into a NodePath
        self.parent_frame = parent

        # So that self['frameSize'] always exists
        self.set_frame_size((0, 0))

    def set_xy(self, xy: tuple[float, float]):
        x, y = xy
        return self.set_pos((x, 0, y))

    def set_frame_size(self, wh: tuple[float, float]):
        w, h = wh
        self["frameSize"] = (0, w, 0, h)

    @property
    def x(self) -> float:
        return self.get_pos()[0]

    @property
    def y(self) -> float:
        return self.get_pos()[2]

    @property
    def width(self) -> float:
        return get_w(self)

    @property
    def height(self) -> float:
        return get_h(self)
