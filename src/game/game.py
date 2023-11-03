from game.map import Map
from game.scenario import Scenario
from game.tower.tower import Tower
from game.unit.unit import Unit


class Game:
    action_queue: list[None]
    scenario: Scenario

    first_tick: float
    round: int
    tick: int
    next_tick: float

    map: Map
    towers: list[Tower]
    units: list[Unit]

    def __init__(self, scenario: Scenario, first_tick: float):
        super().__init__()

        self.action_queue = []
        self.scenario = scenario

        self.first_tick = first_tick
        self.round = -1
        self.tick = -1
        self.next_tick = first_tick

        self.map = Map()
        self.towers = []
        self.units = []

    def render(self, period_s: float):
        self.map.render(period_s)
        self.map.render_queue = []

        for unit in self.units:
            unit.render(period_s)
            unit.render_queue = []

        for tower in self.towers:
            tower.render(period_s)
            tower.render_queue = []
