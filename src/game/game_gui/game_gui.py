from typing import Callable, ClassVar

from direct.gui.DirectGui import DGG
from direct.interval.LerpInterval import LerpFunc
from panda3d.core import MouseWatcherParameter

import g
from game.events.event_manager import GameEvent
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.sidebar.sidebar import Sidebar
from game.state.game_state import StateCreated, StateDeleted
from game.towers.tower_view import TowerView
from game.view.game_view_globals import GVG
from utils.gui_utils import get_h, get_mouse_pos, get_w, mpos_to_real_pos
from utils.types import IntervalDict, Point2


class GameGui(BetterDirectFrame):
    # Percentage of viewport width
    SIDEBAR_WIDTH: ClassVar[float] = 0.20

    sidebar: Sidebar

    _intervals: IntervalDict
    _sidebar_visible: bool
    _sub_sink: list[Callable[[], None]]

    def __init__(self):
        super().__init__(
            g.aspect2d,
            state=DGG.NORMAL,
        )
        self["state"] = DGG.NORMAL

        self.sidebar = Sidebar(self)

        self._intervals = dict()
        self._sidebar_visible = True
        self._sub_sink = []

        self.accept("aspectRatioChanged", lambda: self.recalculate_layout())

        self._sub_clicks()

        self._sub_sink.append(lambda: self.ignore_all())

    def recalculate_layout(self):
        """Set origin to top-left and fill screen"""

        min_x = g.base.a2dLeft
        max_x = g.base.a2dRight
        vw = max_x - min_x

        min_y = g.base.a2dBottom
        max_y = g.base.a2dTop
        vh = max_y - min_y

        self.set_pos((min_x, 0, max_y))
        self.set_frame_size((vw, -vh))

        self._layout_sidebar()

    def _layout_sidebar(self):
        """Anchor sidebar to right edge"""

        vw = get_w(self)
        vh = get_h(self)

        w = self.SIDEBAR_WIDTH * vw
        h = -vh

        self.sidebar.set_frame_size((w, h))
        self.sidebar.recalculate_layout()

        if self._sidebar_visible:
            self._show_sidebar(animate=False)

    def _show_sidebar(self, animate: bool = True):
        self._sidebar_visible = True

        def cb():
            vw = get_w(self)
            w = self.SIDEBAR_WIDTH * vw
            start_x = vw
            start_y = 0

            self.sidebar.set_xy((start_x, start_y))

            print("showing", start_x, vw - w)

            def inner(t: float):
                current_x = vw - w * t
                self.sidebar.set_pos((current_x, 0, start_y))

            return inner

        LerpFunc(
            cb(),
            duration=0.2 if animate else 0,
            fromData=0,
            toData=1,
            blendType="easeInOut",
        ).start()

    def _hide_sidebar(self):
        self._sidebar_visible = False

        def cb():
            start_x = self.sidebar.get_pos()[0]
            start_y = self.sidebar.get_pos()[2]
            width = self.sidebar.width

            def inner(t: float):
                current_x = start_x + width * t
                self.sidebar.set_pos((current_x, 0, start_y))

            return inner

        LerpFunc(
            cb(),
            duration=0.2,
            fromData=0,
            toData=1,
            blendType="easeInOut",
        ).start()

    def _show_tower_details(self, view: TowerView):
        print("_show_tower_details()")
        self._hide_sidebar()

    def _hide_tower_details(self):
        print("_hide_tower_details()")
        self._show_sidebar()

    def _sub_clicks(self):
        path_tiles: set[Point2] = set()
        for path in GVG.data.ppaths.values():
            for point in path.points:
                path_tiles.add(point.pos)

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

        def on_click(param: MouseWatcherParameter):
            pos = get_mouse_pos()
            if not pos:
                return

            real_pos = mpos_to_real_pos(pos)
            active_tile = (round(real_pos[0]), round(real_pos[1]))

            if id := tower_tiles.get(active_tile, None):
                tower_view = GVG.data.views.towers[id]
                return self._show_tower_details(tower_view)

            self._hide_tower_details()

        self.bind(DGG.B1RELEASE, on_click)

    def delete(self):
        self.sidebar.delete()
