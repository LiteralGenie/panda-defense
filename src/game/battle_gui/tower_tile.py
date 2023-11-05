from typing import Any, ClassVar

from direct.gui.DirectGui import DGG, DirectFrame

import g
from game.battle_gui.drag_and_drop import DragAndDrop, DragMoveState
from game.battle_gui.nested_direct_frame import NestedDirectFrame


class TowerTile:
    """A frame with an invisible button to capture clicks"""

    _id_counter: ClassVar[int] = 0
    id: int

    root: DirectFrame
    parent: DirectFrame
    content: NestedDirectFrame

    dnd: DragAndDrop[None]

    _click_event: str

    def __init__(self, root: DirectFrame, parent: DirectFrame, **kwargs: Any):
        self.__class__._id_counter += 1
        self.id = self.__class__._id_counter
        self._click_event = f"click-tower-tile-{self.id}"

        self.root = root
        self.parent = parent
        self.content = NestedDirectFrame(self.parent, state=DGG.NORMAL, **kwargs)
        self.content.inner_frame.bind(DGG.B1PRESS, self._on_mousedown)

        self.dnd = DragAndDrop(
            drag_area=self.root,
            drag_start_events=(self._click_event,),
            on_drag_move=self._on_drag_move,
            on_drag_end=lambda state: print("on_drag_end"),
            on_drag_cancel=lambda state: print("on_drag_cancel"),
        )

    def set_xy(self, xy: tuple[float, float]):
        x, y = xy
        self.content.set_pos((x, 0, y))

    def set_frame_size(self, wh: tuple[float, float]):
        self.content.set_frame_size(wh)

    def delete(self):
        self.dnd.delete()

    def _on_mousedown(self, wtf: Any):
        print("onmousedown", wtf)
        g.base.messenger.send(self._click_event)

    def _on_drag_move(
        self, data: None, start: tuple[float, float], end: tuple[float, float]
    ) -> DragMoveState[None]:
        print("dragmove", data, start, end)
        return DragMoveState(data, start, end)
