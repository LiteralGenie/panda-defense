from dataclasses import asdict
from multiprocessing.connection import Connection

from reactivex import Subject

from game.events.event_manager import TickEvents
from game.game_gui.game_gui import GameGui
from game.maps.map_view import MapView
from game.parameterized_path import ParameterizedPath
from game.player.player_model import PlayerModel
from game.scenario import Scenario
from game.shared_globals import SG
from game.state.game_state import GameState, StateCreated, StateDeleted, StateUpdated
from game.towers.basic.basic_tower_view import BasicTowerView
from game.units.unit_view import UnitView
from game.view.game_view_cache import GameViewData
from game.view.game_view_globals import GVG, GameViewGlobals, GameViewMetaInfo
from game.view.resource_manager import ResourceManager
from game.view.view_manager import GameViewManager
from model_manager import ModelManager


class GameView:
    globals: GameViewGlobals

    gui: GameGui
    map: MapView

    def __init__(
        self,
        first_tick: float,
        scenario: Scenario,
        id_player: int,
        event_pipe: Connection,
    ):
        # init globals
        GVG.event_pipe = event_pipe
        GVG.event_subj = Subject()
        GVG.resource_mgr = ResourceManager()

        cache = GameViewData(
            meta=GameViewMetaInfo(
                id_player=id_player,
                round=-1,
                scenario=scenario,
                tick=-1,
                tick_end=first_tick,
            ),
            models=ModelManager(),
            ppaths={id: ParameterizedPath(p) for id, p in scenario["paths"].items()},
            views=GameViewManager(),
        )
        GVG.data = cache

        SG.state = GameState(on_event=lambda _: None)

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
                    pass
            GVG.event_subj.on_next(ev)

        # Wait for state to init
        if SG.state.data["GAME"] and not getattr(self, "gui", None):
            self.gui = GameGui()

    def _init_view(self, ev: StateCreated):
        match ev.category:
            case "GAME":
                pass
            case "PLAYER":
                model = PlayerModel(ev.id)
                GVG.data.models.players[model.id] = model
            case "TOWER":
                view = BasicTowerView(ev.id)
                GVG.data.views.towers[view.id] = view
                GVG.data.models.towers[view.id] = view.model
            case "UNIT":
                view = UnitView(ev.id)
                GVG.data.views.units[view.id] = view
                GVG.data.models.units[view.id] = view.model
