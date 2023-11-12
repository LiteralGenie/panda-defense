from typing import ClassVar

from direct.interval.FunctionInterval import Func
from direct.interval.LerpInterval import LerpFunc
from direct.interval.MetaInterval import Sequence

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.tower_grid import TowerGrid
from game.game_gui.status_list.build_timer_status import BuildTimerStatus
from game.game_gui.status_list.enemy_status import EnemyStatus
from game.game_gui.status_list.gold_status import GoldStatus
from game.game_gui.status_list.health_status import HealthStatus
from game.game_gui.status_list.round_status import RoundStatus
from game.game_gui.status_list.status_list import StatusList
from utils.gui_utils import get_h


class Sidebar(BetterDirectFrame):
    GRID_COLS: ClassVar[int] = 2
    # Percentage of parent width
    GRID_WIDTH: ClassVar[float] = 0.55
    # Percentage of width per status in list
    STATUS_HEIGHT: ClassVar[float] = 0.35
    # Percentage of width
    STATUS_OFFSET: ClassVar[float] = 0.1
    # Percentage of status width
    INTER_STATUS_GAP: ClassVar[float] = 0.085

    container: BetterDirectFrame
    tower_grid: TowerGrid
    basic_status: StatusList
    wave_status: StatusList

    _is_visible: bool

    def __init__(self, parent: BetterDirectFrame):
        super().__init__(parent)

        self.container = BetterDirectFrame(self)

        self.tower_grid = TowerGrid(
            self.container,
            num_cols=self.GRID_COLS,
        )
        for _ in range(7):
            self.tower_grid.create_tile(
                recalculate_layout=False,
            )

        self.basic_status = StatusList(
            self.container,
            labels=[
                HealthStatus(self),
                GoldStatus(self),
            ],
        )

        self.wave_status = StatusList(
            self.container,
            labels=[
                RoundStatus(self),
                EnemyStatus(self),
                BuildTimerStatus(self),
            ],
        )

        # When a tower is clicked, swap out the sidebar with the tower description
        self._is_visible = True
        self.accept("showTowerDetails", lambda _: self._hide_container())
        self.accept("hideTowerDetails", lambda: self._show_container())

    def recalculate_layout(self):
        self._layout_container()
        self._layout_tower_grid()
        self._layout_basic_status()
        self._layout_wave_status(self.basic_status)

    def _layout_container(self):
        self.container.set_frame_size((self.width, self.height))
        if self._is_visible:
            self._show_container(animate=False)
        else:
            self._hide_container(animate=False)

    def _layout_tower_grid(self):
        """Anchor tower grid to right edge"""

        ch = get_h(self.parent_frame)

        w = self.container.width * self.GRID_WIDTH
        h = ch

        tl_x = self.container.width - w
        tl_y = 0

        self.tower_grid.set_xy((tl_x, tl_y))
        self.tower_grid.set_frame_size((w, h))
        self.tower_grid.recalculate_layout()

    def _layout_basic_status(self):
        """Anchor status displays left of tower grid"""

        tw = self.container.width * (1 - self.GRID_WIDTH)

        # Count left / right margins as partial column
        w = tw / (1 + 2 * self.STATUS_OFFSET)
        h = -self.STATUS_HEIGHT * w * len(self.basic_status.labels)

        offset = self.STATUS_OFFSET * w
        tl_x = offset
        tl_y = -offset

        self.basic_status.set_xy((tl_x, tl_y))
        self.basic_status.set_frame_size((w, h))
        self.basic_status.recalculate_layout()

    def _layout_wave_status(self, basic_status: StatusList):
        """Anchor status displays left of sidebar and below other status list"""

        tw = self.container.width * (1 - self.GRID_WIDTH)

        w = tw / (1 + 2 * self.STATUS_OFFSET)
        h = -self.STATUS_HEIGHT * w * len(self.wave_status.labels)

        offset_x = self.STATUS_OFFSET * w
        tl_x = offset_x

        offset_y = self.INTER_STATUS_GAP * w
        tl_y = basic_status.y + basic_status.height - offset_y

        self.wave_status.set_xy((tl_x, tl_y))
        self.wave_status.set_frame_size((w, h))
        self.wave_status.recalculate_layout()

    def _show_container(self, animate: bool = True):
        duration = 0 if not animate or self._is_visible else 0.35
        self._is_visible = True

        def cb():
            width = self.container.width
            y = 0

            def inner(t: float):
                current_x = width * (1 - t)
                self.container.set_pos((current_x, 0, y))

            inner(0)

            return inner

        Sequence(
            Func(lambda: self.show()),
            Func(lambda: self.basic_status.hide()),
            Func(lambda: self.wave_status.hide()),
            LerpFunc(
                cb(),
                duration=duration,
                fromData=0,
                toData=1,
                blendType="easeInOut",
            ),
            Func(lambda: self.basic_status.show()),
            Func(lambda: self.wave_status.show()),
        ).start()

    def _hide_container(self, animate: bool = True):
        duration = 0 if not animate or not self._is_visible else 0.35
        self._is_visible = False

        def cb():
            width = self.container.width
            y = 0

            def inner(t: float):
                current_x = width * t
                self.container.set_pos((current_x, 0, y))

            inner(0)

            return inner

        Sequence(
            Func(lambda: self.basic_status.hide()),
            Func(lambda: self.wave_status.hide()),
            LerpFunc(
                cb(),
                duration=duration,
                fromData=0,
                toData=1,
                blendType="easeInOut",
            ),
            Func(lambda: self.basic_status.show()),
            Func(lambda: self.wave_status.show()),
            Func(lambda: self.hide()),
        ).start()

    def delete(self):
        super().delete()
        self.tower_grid.delete()
        self.basic_status.delete()
        self.wave_status.delete()
