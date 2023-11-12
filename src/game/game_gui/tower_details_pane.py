from typing import TYPE_CHECKING

from direct.gui.DirectGui import DGG
from panda3d.core import MouseWatcherParameter

from game.events.event_manager import GameEvent
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.state.game_state import StateCreated, StateDeleted
from game.view.game_view_globals import GVG
from utils.gui_utils import get_mouse_pos, mpos_to_real_pos
from utils.types import Point2

if TYPE_CHECKING:
    from game.game_gui.game_gui import GameGui


class TowerDetailsPane(BetterDirectFrame):
    active_tower: int | None

    def __init__(self, parent: "GameGui"):
        super().__init__(
            parent,
            state=DGG.NORMAL,
            frameColor=(0, 0, 0, 1),
        )

        self.active_tower = None

        self._sub_clicks()

    def recalculate_layout(self):
        pass

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
                prev = self.active_tower
                self.active_tower = id_tower

                # If this pane is already open, don't re-open it
                if prev is None:
                    messenger.send("showTowerDetails")

                self.recalculate_layout()
                return
            else:
                self.active_tower = None
                messenger.send("hideTowerDetails")
                return

        self.parent_frame.bind(DGG.B1RELEASE, on_click)
