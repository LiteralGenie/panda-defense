from game.map import Map
from game.scenario import Round, Scenario
from game.tower.tower import Tower
from game.unit.unit_manager import UnitManager


class Game:
    action_queue: list[None]
    scenario: Scenario

    first_tick: float
    next_tick: float
    round_idx: int
    tick: int

    map: Map
    towers: list[Tower]
    unit_mgr: UnitManager

    def __init__(self, scenario: Scenario, first_tick: float):
        super().__init__()

        self.action_queue = []
        self.scenario = scenario

        self.first_tick = first_tick
        self.next_tick = first_tick
        self.round_idx = -1
        self.tick = -1

        self.map = Map()
        self.towers = []
        self.unit_mgr = UnitManager()

    def render(self, period_s: float):
        self.map.render(period_s)
        self.map.render_queue = []

        for unit in self.unit_mgr:
            unit.render(period_s)
            unit.render_queue = []

        for tower in self.towers:
            tower.render(period_s)
            tower.render_queue = []

    @property
    def current_round(self) -> Round:
        return self.scenario.rounds[self.round_idx]
