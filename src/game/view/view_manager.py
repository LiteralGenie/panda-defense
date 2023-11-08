from typing import TypeVar

from game.towers.tower_view import TowerView
from game.units.unit_view import UnitView

T = TypeVar("T")

_ModelsById = dict[int, T]


class GameViewManager:
    towers: _ModelsById[TowerView]
    units: _ModelsById[UnitView]

    def __init__(self):
        self.towers = dict()
        self.units = dict()
