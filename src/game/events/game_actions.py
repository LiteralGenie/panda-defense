from dataclasses import dataclass
from typing import Any, Type

from game.towers.tower_model import TowerModel


@dataclass
class BuyTowerAction:
    TowerCls: Type[TowerModel]
    id_player: int
    kwargs: dict[str, Any]


GameActions = BuyTowerAction
