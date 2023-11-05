from typing import Any, ClassVar

from direct.gui.DirectGui import DirectFrame

from game.battle_gui.drag_and_drop import DragAndDrop
from game.battle_gui.nested_direct_frame import NestedDirectFrame


class TowerTile:
    """A frame with an invisible button to capture clicks"""

    _id_counter: ClassVar[int] = 0
    id: int

    parent: DirectFrame
    content: NestedDirectFrame

    dnd: DragAndDrop[None, None]

    _click_event: str

    def __init__(self, parent: DirectFrame, **kwargs: Any):
        self.__class__._id_counter += 1
        self.id = self.__class__._id_counter
        self._click_event = f"click-tower-tile-{self.id}"

        self.parent = parent
        self.content = NestedDirectFrame(self.parent, **kwargs)

        self.dnd = DragAndDrop(
            target=self.content.inner_frame,
            on_drag_start=self._on_drag_start,
            on_drag_move=self._on_drag_move,
            on_drag_end=self._on_drag_end,
            on_drag_cancel=self._on_drag_cancel,
        )

    def set_xy(self, xy: tuple[float, float]):
        x, y = xy
        self.content.set_pos((x, 0, y))

    def set_frame_size(self, wh: tuple[float, float]):
        self.content.set_frame_size(wh)

    def delete(self):
        self.dnd.delete()

    def _on_drag_start(self, *wtf: Any):
        print("on_drag_down cb", wtf)

    def _on_drag_move(self, *wtf: Any):
        print("on_drag_move cb", wtf)

    def _on_drag_end(self, *wtf: Any):
        print("on_drag_end cb", wtf)

    def _on_drag_cancel(self, *wtf: Any):
        print("on_drag_cancel cb", wtf)
