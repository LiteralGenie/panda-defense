from typing import Any

from direct.gui.DirectFrame import DirectFrame
from panda3d.core import NodePath

from utils.gui_utils import get_h, get_w, set_frame_size

_FrameColor = tuple[float, float, float, float]


class NestedDirectFrame(DirectFrame):
    """
    DirectFrame with a DirectFrame child
    The outer frame controls position (via set_xy())
    The inner frame controls size (via set_frame_size())
    """

    inner_frame: DirectFrame

    def __init__(
        self, parent: NodePath, frameColor: _FrameColor = (0, 0, 0, 0), **kwargs: Any
    ) -> None:
        super().__init__(parent)

        self.inner_frame = DirectFrame(self, frameColor=frameColor, **kwargs)

    def set_xy(self, xy: tuple[float, float]):
        x, y = xy
        return super().set_pos((x, 0, y))

    def set_frame_size(self, wh: tuple[float, float]):
        set_frame_size(self.inner_frame, wh)

    @property
    def width(self) -> float:
        return get_w(self.inner_frame)

    @property
    def height(self) -> float:
        return get_h(self.inner_frame)
