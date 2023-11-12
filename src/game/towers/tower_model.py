from abc import ABC
from typing import Any, ClassVar, Self

from game.id_manager import IdManager
from game.state.game_state import StateCategory
from game.state.stateful_class import StatefulClass, StatefulProp
from game.towers.tower_range import TowerRange
from utils.types import Point2


class TowerModel(StatefulClass, ABC):
    _state_category: ClassVar[StateCategory] = "TOWER"

    cost: ClassVar[int]
    default_range: ClassVar[TowerRange]

    id: int = StatefulProp()  # type: ignore
    attack_speed: float = StatefulProp()  # type: ignore
    attack_speed_guage: float = StatefulProp()  # type: ignore
    damage: int = StatefulProp()  # type: ignore
    pos: Point2 = StatefulProp()  # type: ignore
    range: TowerRange = StatefulProp()  # type: ignore

    @classmethod
    def create(
        cls,
        pos: Point2,
        attack_speed: float,
        attack_speed_guage: float,
        damage: int,
        range: TowerRange,
        **kwargs: Any,
    ) -> Self:
        id = IdManager.create()

        instance = cls(id)
        instance._register(
            init_state=dict(
                id=id,
                pos=pos,
                attack_speed=attack_speed,
                attack_speed_guage=attack_speed_guage,
                damage=damage,
                range=range,
                **kwargs,
            )
        )

        return instance

    def delete(self):
        self._delete()
