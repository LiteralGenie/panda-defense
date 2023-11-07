from enum import Enum
from typing import Any, ClassVar, Self

from game.id_manager import IdManager
from game.parameterized_path import ParameterizedPath
from game.state import StateCategory
from game.stateful_class import StatefulClass, StatefulProp


class UnitStatus(Enum):
    PRESPAWN = "PRESPAWN"
    ALIVE = "ALIVE"
    DEAD = "DEAD"


class UnitModel(StatefulClass):
    _state_category: ClassVar[StateCategory] = "UNIT"

    id: int = StatefulProp("id", read_only=True)  # type: ignore
    id_wave: int = StatefulProp("id_wave", read_only=True)  # type: ignore

    dist: float = StatefulProp("dist")  # type: ignore
    health: int = StatefulProp("health")  # type: ignore
    speed: float = StatefulProp("speed", read_only=True)  # type: ignore
    status: UnitStatus = StatefulProp("status")  # type: ignore

    ppath: ParameterizedPath

    @classmethod
    def create(
        cls,
        id_wave: int,
        ppath: ParameterizedPath,
        speed: float,
        **kwargs: Any,
    ) -> Self:
        id = IdManager.create()

        instance = cls(id)
        instance.ppath = ppath
        instance._register(
            init_state=dict(
                id=id,
                id_path=ppath.id,
                id_wave=id_wave,
                dist=0,
                health=100,
                speed=speed,
                status=UnitStatus.PRESPAWN,
                **kwargs,
            )
        )

        return instance

    @classmethod
    def load(cls, id: int, ppath: ParameterizedPath) -> Self:  # type: ignore
        instance = super().load(id)
        instance.ppath = ppath
        return instance
