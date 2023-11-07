from dataclasses import asdict
from multiprocessing.connection import Connection
from typing import Any

from reactivex import Subject

from game.events.event_manager import TickEvents
from game.game_gui.game_gui import GameGui
from game.maps.map_view import MapView
from game.parameterized_path import ParameterizedPath
from game.scenario import Scenario
from game.shared_globals import SG
from game.state.state import State, StateCreated, StateDeleted, StateUpdated
from game.towers.tower_view import TowerView
from game.units.unit_view import UnitView
from game.view.game_view_cache import GameViewCache
from game.view.game_view_globals import GVG, GameViewGlobals, GameViewMetaInfo


class GameView:
    globals: GameViewGlobals

    gui: GameGui
    map: MapView
    views: dict[int, Any]

    def __init__(
        self,
        first_tick: float,
        scenario: Scenario,
        event_pipe: Connection,
    ):
        # init globals
        GVG.event_pipe = event_pipe
        GVG.event_subj = Subject()
        GVG.meta = GameViewMetaInfo(
            round=-1,
            scenario=scenario,
            tick=-1,
            tick_end=first_tick,
        )

        ppaths = {id: ParameterizedPath(p) for id, p in scenario["paths"].items()}
        cache = GameViewCache(
            ppaths=ppaths,
        )
        GVG.cache = cache

        SG.entities = State(on_event=GVG.event_subj.on_next)

        self.gui = GameGui()
        self.map = MapView()
        self.views = dict()

    def render(self, update: TickEvents):
        # print(
        #     f"til render {(TICK_PERIOD_S - (tick.tick_end - time.time()))*1000:.0f}ms"
        # )

        GVG.meta.round = update.round
        GVG.meta.tick = update.tick
        GVG.meta.tick_end = update.tick_end

        # Sync state
        for ev in update.events:
            match ev:
                case StateCreated():
                    SG.entities.create(**asdict(ev))
                    self._init_view(ev)
                case StateUpdated():
                    SG.entities.update(**asdict(ev))
                case StateDeleted():
                    SG.entities.delete(**asdict(ev))
                case _:
                    GVG.event_subj.on_next(ev)

    def _init_view(self, ev: StateCreated):
        match ev.category:
            case "TOWER":
                self.views[ev.id] = TowerView(ev.id)
            case "UNIT":
                self.views[ev.id] = UnitView(ev.id)
