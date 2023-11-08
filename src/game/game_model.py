from typing import Any

from game.events.game_actions import BuyTowerAction, GameActions
from game.player.player_model import PlayerModel
from game.scenario import Round, Scenario
from game.towers.tower_model import TowerModel
from game.units.unit_manager import UnitManager
from game.units.unit_model import UnitModel


class GameModel:
    action_queue: list[GameActions]
    scenario: Scenario

    first_tick: float
    next_tick: float
    round_idx: int
    tick: int

    players: list[PlayerModel]
    towers: list[TowerModel]
    unit_mgr: UnitManager

    def __init__(
        self,
        scenario: Scenario,
        first_tick: float,
    ):
        self.action_queue = []
        self.scenario = scenario

        self.first_tick = first_tick
        self.next_tick = first_tick
        self.round_idx = -1
        self.tick = -1

        self.players = []
        self.towers = []
        self.unit_mgr = UnitManager()

    @property
    def current_round(self) -> Round:
        return self.scenario["rounds"][self.round_idx]

    def add_player(self, player: PlayerModel):
        self.players.append(player)

    def add_tower(self, tower: TowerModel):
        self.towers.append(tower)

    def add_unit(self, unit: UnitModel):
        self.unit_mgr.add(unit)

    def add_action(self, action: Any):
        self.action_queue.append(action)
        # todo: validate

    def apply_actions(self):
        for action in self.action_queue:
            match action:
                case BuyTowerAction(cls, kwargs):
                    tower: TowerModel = cls(**kwargs)
                    self.add_tower(tower)

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
