from dataclasses import dataclass
from typing import Any, Type


@dataclass
class BuyTowerAction:
    cls: Type[Any]
    kwargs: dict[str, Any]


GameActions = BuyTowerAction
