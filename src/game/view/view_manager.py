from typing import TypeVar

from game.towers.tower_view import TowerView
from game.units.unit_view import UnitView

T = TypeVar("T")

_ById = dict[int, T]


class GameViewManager:
    towers: _ById[TowerView]
    units: _ById[UnitView]

    def __init__(self):
        self.towers = dict()
        self.units = dict()
