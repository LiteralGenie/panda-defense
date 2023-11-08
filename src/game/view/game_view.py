from dataclasses import asdict
from multiprocessing.connection import Connection

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
from game.view.game_view_cache import GameViewData
from game.view.game_view_globals import GVG, GameViewGlobals, GameViewMetaInfo
from game.view.view_manager import GameViewManager


class GameView:
    globals: GameViewGlobals

    gui: GameGui
    map: MapView

    def __init__(
        self,
        first_tick: float,
        scenario: Scenario,
        event_pipe: Connection,
    ):
        # init globals
        GVG.event_pipe = event_pipe
        GVG.event_subj = Subject()

        cache = GameViewData(
            meta=GameViewMetaInfo(
                round=-1,
                scenario=scenario,
                tick=-1,
                tick_end=first_tick,
            ),
            ppaths={id: ParameterizedPath(p) for id, p in scenario["paths"].items()},
            views=GameViewManager(),
        )
        GVG.data = cache

        SG.state = State(on_event=GVG.event_subj.on_next)

        self.gui = GameGui()
        self.map = MapView()

    def render(self, update: TickEvents):
        # print(
        #     f"til render {(TICK_PERIOD_S - (tick.tick_end - time.time()))*1000:.0f}ms"
        # )

        GVG.data.meta.round = update.round
        GVG.data.meta.tick = update.tick
        GVG.data.meta.tick_end = update.tick_end

        # Sync state
        for ev in update.events:
            match ev:
                case StateCreated():
                    SG.state.create(**asdict(ev))
                    self._init_view(ev)
                case StateUpdated():
                    SG.state.update(**asdict(ev))
                case StateDeleted():
                    SG.state.delete(**asdict(ev))
                case _:
                    GVG.event_subj.on_next(ev)

    def _init_view(self, ev: StateCreated):
        match ev.category:
            case "TOWER":
                GVG.data.views.towers[ev.id] = TowerView(ev.id)
            case "UNIT":
                GVG.data.views.units[ev.id] = UnitView(ev.id)
