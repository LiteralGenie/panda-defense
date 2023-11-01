from panda3d.core import NodePath

from game.map import Map
from game.renderable import Renderable
from game.scenario import Scenario


class Game(Renderable):
    action_queue: list
    map: Map
    scenario: Scenario

    round: int
    tick: int
    next_tick: float

    def __init__(self, scenario: Scenario):
        super().__init__()

        self.action_queue = []
        self.map = Map()
        self.scenario = scenario

        self.round = -1
        self.tick = -1
        self.next_tick = float("inf")

    def render(self, parent: NodePath, period_s: float):
        self.map.render(parent, period_s)
