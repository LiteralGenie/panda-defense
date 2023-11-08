from dataclasses import dataclass
from typing import Any, Type

from game.towers.tower_model import TowerModel


@dataclass
class BuyTowerAction:
    id_player: int
    TowerCls: Type[TowerModel]
    kwargs: dict[str, Any]


GameActions = BuyTowerAction
