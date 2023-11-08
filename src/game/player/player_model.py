from typing import ClassVar, Self

from game.id_manager import IdManager
from game.state.state import StateCategory
from game.state.stateful_class import StatefulClass, StatefulProp


class PlayerModel(StatefulClass):
    _state_category: ClassVar[StateCategory] = "PLAYER"

    id: int = StatefulProp(read_only=True)  # type: ignore

    gold: int = StatefulProp()  # type: ignore
    health: int = StatefulProp()  # type: ignore
    towers: list[int] = StatefulProp()  # type: ignore

    @classmethod
    def create(
        cls,
        gold: int,
        health: int,
    ) -> Self:
        id = IdManager.create()

        instance = cls(id)
        instance._register(
            init_state=dict(
                id=id,
                gold=gold,
                health=health,
            )
        )

        return instance
