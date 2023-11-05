from typing import Any

from direct.gui.DirectGui import DirectFrame

from game.battle_gui.better_direct_frame import BetterDirectFrame
from game.battle_gui.drag_and_drop import DragAndDrop


class TowerTile(BetterDirectFrame):
    dnd: DragAndDrop[None, None]

    def __init__(self, parent: DirectFrame, **kwargs: Any):
        super().__init__(parent, **kwargs)

        self.dnd = DragAndDrop(
            target=self,
            on_drag_start=self._on_drag_start,
            on_drag_move=self._on_drag_move,
            on_drag_end=self._on_drag_end,
            on_drag_cancel=self._on_drag_cancel,
        )

    def delete(self):
        self.dnd.delete()

    def _on_drag_start(self, *args: Any):
        print("on_drag_start cb", args)

    def _on_drag_move(self, *args: Any):
        print("on_drag_move cb", args)

    def _on_drag_end(self, *args: Any):
        print("on_drag_end cb", args)

    def _on_drag_cancel(self, *args: Any):
        print("on_drag_cancel cb", args)
