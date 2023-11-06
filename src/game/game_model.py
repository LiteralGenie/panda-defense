from game.controller.controller_globals import ControllerGlobals
from game.scenario import Round, Scenario
from game.state import GameState
from game.towers.render_tower_events import RenderTowerSpawn
from game.towers.tower_model import TowerModel
from game.units.unit_manager import UnitManager
from game.units.unit_model import UnitModel


class GameModel:
    action_queue: list[None]
    scenario: Scenario

    first_tick: float
    next_tick: float
    round_idx: int
    tick: int

    towers: list[TowerModel]
    unit_mgr: UnitManager

    globals: ControllerGlobals

    def __init__(
        self,
        scenario: Scenario,
        first_tick: float,
        globals: ControllerGlobals,
    ):
        self.action_queue = []
        self.scenario = scenario

        self.first_tick = first_tick
        self.next_tick = first_tick
        self.round_idx = -1
        self.tick = -1

        self.towers = []
        self.unit_mgr = UnitManager()

        self.globals = globals

    def serialize(self) -> GameState:
        return dict(
            scenario=self.scenario,
            towers={t.id: t.serialize() for t in self.towers},
            units={u.id: u.serialize() for u in self.unit_mgr},
        )  # type: ignore

    @property
    def current_round(self) -> Round:
        return self.scenario["rounds"][self.round_idx]

    def add_tower(self, tower: TowerModel):
        self.towers.append(tower)
        self.globals.ev_mgr.add(RenderTowerSpawn(ids=[tower.id]))

    def add_unit(self, unit: UnitModel):
        self.unit_mgr.add(unit)

    # def delete(self):
    #     actors = [UnitView]
    #     for a in actors:
    #         if a.model:
    #             a.model.cleanup()  # type: ignore
    #             a.model.removeNode()

    #     renderables = [Map]
    #     for r in renderables:
    #         if r.model:
    #             r.model.removeNode()
