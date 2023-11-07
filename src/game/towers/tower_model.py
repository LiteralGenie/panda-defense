from abc import ABC
from typing import Any, ClassVar, Self

from game.id_manager import IdManager
from game.state.state import StateCategory
from game.state.stateful_class import StatefulClass, StatefulProp
from game.towers.tower_range import TowerRange
from utils.types import Point2


class TowerModel(StatefulClass, ABC):
    _state_category: ClassVar[StateCategory] = "TOWER"

    id: int = StatefulProp()  # type: ignore
    pos: Point2 = StatefulProp()  # type: ignore
    range: TowerRange = StatefulProp(read_only=True)  # type: ignore

    @classmethod
    def create(
        cls,
        pos: Point2,
        range: TowerRange,
        **kwargs: Any,
    ) -> Self:
        id = IdManager.create()

        instance = cls(id)
        instance._register(
            init_state=dict(
                id=id,
                pos=pos,
                range=range,
                **kwargs,
            )
        )

        return instance
