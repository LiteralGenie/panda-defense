from typing import TypeVar

from game.player.player_model import PlayerModel
from game.towers.tower_model import TowerModel
from game.units.unit_model import UnitModel

T = TypeVar("T")

_ById = dict[int, T]


class ModelManager:
    players: _ById[PlayerModel]
    towers: _ById[TowerModel]
    units: _ById[UnitModel]

    def __init__(self):
        self.players = dict()
        self.towers = dict()
        self.units = dict()
