from dataclasses import dataclass
from typing import Any, Type

from game.towers.tower_model import TowerModel


@dataclass
class BuyTowerAction:
    TowerCls: Type[TowerModel]
    kwargs: dict[str, Any]


GameActions = BuyTowerAction
