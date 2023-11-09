from typing import ClassVar

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.status_list.health_status import HealthStatus
from game.game_gui.status_list.status_label import StatusLabel
from utils.gui_utils import get_h, get_w


class StatusList(BetterDirectFrame):
    # Relative to width
    PAD_PERCENT: ClassVar[float] = 0.1
    # Relative to height
    GAP_PERCENT: ClassVar[float] = 0.1

    labels: list[StatusLabel]
    health_status: HealthStatus

    def __init__(self, parent: BetterDirectFrame, labels: list[StatusLabel]):
        super().__init__(parent)

        self.labels = labels
        for lbl in self.labels:
            lbl.reparent_to(self)

    def recalculate_layout(self):
        for i, label in enumerate(self.labels):
            tl_x = 0
            tl_y = i * (self._status_height + self._gap_height)
            label.set_xy((tl_x, tl_y))

            w = get_w(self)
            h = self._status_height
            label.set_frame_size((w, h))

            label.recalculate_layout()

    def delete(self):
        pass

    @property
    def _status_height(self) -> float:
        # Treat each gap as a partial tile
        height_tiles = len(self.labels) + (len(self.labels) - 1) * self.GAP_PERCENT

        result = get_h(self) / height_tiles
        return result

    @property
    def _gap_height(self) -> float:
        result = self._status_height * self.GAP_PERCENT
        return result
