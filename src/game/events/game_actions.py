from dataclasses import dataclass
from typing import Any, Literal, Type

from game.towers.tower_model import TowerModel


@dataclass
class BuyTowerAction:
    TowerCls: Type[TowerModel]
    id_player: int
    kwargs: dict[str, Any]


@dataclass
class UpgradeTowerAction:
    id_player: int
    id_tower: int
    trait: Literal["damage", "range", "speed"]


@dataclass
class SellTowerAction:
    id_player: int
    id_tower: int


GameActions = BuyTowerAction | UpgradeTowerAction | SellTowerAction
