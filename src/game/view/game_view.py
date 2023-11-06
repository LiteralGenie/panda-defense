from multiprocessing.connection import Connection
from typing import Any

from game.event_manager import TickEvents
from game.game_gui.game_gui import GameGui
from game.game_state import GameState
from game.maps.map_view import MapView
from game.parameterized_path import ParameterizedPath
from game.towers.render_tower_events import RenderTowerSpawn
from game.towers.tower_view import TowerView
from game.units.render_unit_events import RenderUnitSpawn
from game.units.unit_view import UnitView
from game.view.game_view_cache import GameViewCache
from game.view.game_view_globals import GameViewGlobals


class GameView:
    globals: GameViewGlobals

    gui: GameGui
    entities: dict[int, Any]
    map: MapView

    def __init__(self, state: GameState, event_pipe: Connection):
        ppaths = {
            id: ParameterizedPath(p) for id, p in state["scenario"]["paths"].items()
        }
        cache = GameViewCache(
            ppaths=ppaths,
        )
        self.globals = GameViewGlobals(
            cache=cache,
            event_pipe=event_pipe,
            state=state,
        )

        self.gui = GameGui(self.globals)
        self.entities = dict()
        self.map = MapView()

    def render(self, tick: TickEvents):
        # print(
        #     f"til render {(TICK_PERIOD_S - (tick.tick_end - time.time()))*1000:.0f}ms"
        # )

        evs_by_tgt: dict[int, list[Any]] = dict()

        for ev in tick.events:
            for tgt_id in ev.ids:
                evs_by_tgt.setdefault(tgt_id, [])
                evs_by_tgt[tgt_id].append(ev)

            match ev:
                case RenderUnitSpawn(ids=[id]):
                    self.entities[id] = UnitView(id)
                case RenderTowerSpawn(ids=[id]):
                    self.entities[id] = TowerView(id)
                case _:
                    pass

        for tgt_id, evs in evs_by_tgt.items():
            self.entities[tgt_id].render(
                tick,
                self.globals,
                evs,
            )
