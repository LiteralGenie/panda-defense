from typing import TYPE_CHECKING, ClassVar

from direct.gui.DirectGui import DGG
from direct.interval.FunctionInterval import Func
from direct.interval.LerpInterval import LerpFunc
from direct.interval.MetaInterval import Sequence
from panda3d.core import MouseWatcherParameter

from game.events.event_manager import GameEvent
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.status_list.build_timer_status import BuildTimerStatus
from game.game_gui.status_list.enemy_status import EnemyStatus
from game.game_gui.status_list.gold_status import GoldStatus
from game.game_gui.status_list.health_status import HealthStatus
from game.game_gui.status_list.round_status import RoundStatus
from game.game_gui.status_list.status_list import StatusList
from game.game_gui.tower_details.tower_details import TowerDetails
from game.state.game_state import StateCreated, StateDeleted
from game.view.game_view_globals import GVG
from utils.gui_utils import get_mouse_pos, mpos_to_real_pos
from utils.types import Point2

if TYPE_CHECKING:
    from game.game_gui.game_gui import GameGui


class TowerDetailsPane(BetterDirectFrame):
    # Percentage of parent width
    PANE_WIDTH: ClassVar[float] = 0.66
    # Percentage of width per status in list
    STATUS_HEIGHT: ClassVar[float] = 0.35
    # Percentage of width
    STATUS_OFFSET: ClassVar[float] = 0.1
    # Percentage of status width
    INTER_STATUS_GAP: ClassVar[float] = 0.085

    active_tower: int | None
    container: BetterDirectFrame
    details: TowerDetails
    basic_status: StatusList
    wave_status: StatusList

    _is_visible: bool

    def __init__(self, parent: "GameGui"):
        super().__init__(parent)

        self.active_tower = None

        self.container = BetterDirectFrame(self)

        self.details = TowerDetails(self.container)

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

        self._is_visible = False

        self._sub_clicks()

    def recalculate_layout(self):
        self._layout_container()
        self._layout_details()
        self._layout_basic_status()
        self._layout_wave_status(self.basic_status)

    def _layout_container(self):
        self.container.set_frame_size((self.width, self.height))
        if self._is_visible:
            self._show_container(animate=False)
        else:
            self._hide_container(animate=False)

    def _layout_details(self):
        """Anchor tower description to right edge"""

        ch = self.container.height

        w = self.width * self.PANE_WIDTH
        h = ch

        tl_x = self.width - w
        tl_y = 0

        self.details.set_xy((tl_x, tl_y))
        self.details.set_frame_size((w, h))
        self.details.recalculate_layout()

    def _layout_basic_status(self):
        """Anchor status displays left of tower grid"""

        tw = self.width * (1 - self.PANE_WIDTH)

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

        tw = self.width * (1 - self.PANE_WIDTH)

        w = tw / (1 + 2 * self.STATUS_OFFSET)
        h = -self.STATUS_HEIGHT * w * len(self.wave_status.labels)

        offset_x = self.STATUS_OFFSET * w
        tl_x = offset_x

        offset_y = self.INTER_STATUS_GAP * w
        tl_y = basic_status.y + basic_status.height - offset_y

        self.wave_status.set_xy((tl_x, tl_y))
        self.wave_status.set_frame_size((w, h))
        self.wave_status.recalculate_layout()

    def _sub_clicks(self):
        """When a tower is clicked, replace sidebar with details pane"""

        # Monitor clickable tiles
        tower_tiles: dict[Point2, int] = dict()

        def on_next(ev: GameEvent):
            match ev:
                case StateCreated(category="TOWER"):
                    tower_tiles[ev.data["pos"]] = ev.id
                case StateDeleted(category="TOWER"):
                    tower_tiles[ev.data["pos"]] = ev.id
                case _:
                    pass

        tile_sub = GVG.event_subj.subscribe(on_next=on_next)
        self._sub_sink.append(lambda: tile_sub.dispose())

        # Map clicks to tile coordinates
        def on_click(param: MouseWatcherParameter):
            pos = get_mouse_pos()
            if not pos:
                return

            real_pos = mpos_to_real_pos(pos)
            active_tile = (round(real_pos[0]), round(real_pos[1]))

            id_tower = tower_tiles.get(active_tile, None)
            if self.active_tower == id_tower:
                return
            elif id_tower:
                self.active_tower = id_tower
                self.details.set_id_tower(id_tower)

                messenger.send("showTowerDetails", [id_tower])
                self._show_container()

                self.details.recalculate_layout()
                return
            else:
                self.active_tower = None
                messenger.send("hideTowerDetails")
                self._hide_container()
                return

        self.parent_frame.bind(DGG.B1RELEASE, on_click)

        # A child component can also generate this event
        self.accept("hideTowerDetails", lambda: self._hide_container())

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
                current_x = width * (t)
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
        self.basic_status.delete()
        self.wave_status.delete()
