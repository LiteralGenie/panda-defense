from typing import Any, ClassVar, Self

from game.events.game_actions import GameActions
from game.id_manager import IdManager
from game.player.player_model import PlayerModel
from game.scenario import Round, Scenario
from game.state.game_state import StateCategory
from game.state.stateful_class import StatefulClass, StatefulProp
from game.towers.tower_model import TowerModel
from game.units.unit_manager import UnitManager
from game.units.unit_model import UnitModel


class GameModel(StatefulClass):
    _state_category: ClassVar[StateCategory] = "GAME"

    action_queue: list[GameActions]
    scenario: Scenario = StatefulProp(read_only=True)  # type: ignore

    first_tick: float = StatefulProp(read_only=True)  # type: ignore
    next_tick: float = StatefulProp()  # type: ignore
    round_idx: int = StatefulProp()  # type: ignore
    tick: int = StatefulProp()  # type: ignore

    players: dict[int, PlayerModel]
    towers: dict[int, TowerModel]
    unit_mgr: UnitManager

    id: int = StatefulProp(read_only=True)  # type: ignore
    id_player: int = StatefulProp(read_only=True)  # type: ignore
    health: int = StatefulProp()  # type: ignore

    @classmethod
    def create(
        cls,
        scenario: Scenario,
        first_tick: float,
        id_player: int,
        players: list[PlayerModel],
    ) -> Self:
        id = IdManager.create()
        instance = cls(id)

        instance.action_queue = []
        instance.players = {pl.id: pl for pl in players}
        instance.towers = dict()
        instance.unit_mgr = UnitManager()

        # Unlike other models, we don't intend to have multiple instances of GameModel
        # nor re-instantiate it in the View process
        # this is mostly so the View is notified of health / gold changes
        instance._register(
            dict(
                scenario=scenario,
                first_tick=first_tick,
                next_tick=first_tick,
                round_idx=-1,
                tick=-1,
                id=id,
                id_player=id_player,
                health=30,
            )
        )

        return instance

    @property
    def current_round(self) -> Round:
        return self.scenario["rounds"][self.round_idx]

    def add_tower(self, tower: TowerModel):
        self.towers[tower.id] = tower

    def add_unit(self, unit: UnitModel):
        self.unit_mgr.add(unit)

    def add_action(self, action: Any):
        self.action_queue.append(action)
        # todo: validate
