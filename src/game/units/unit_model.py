from enum import Enum
from math import modf
from typing import Any, ClassVar, Self

from game.id_manager import IdManager
from game.parameterized_path import ParameterizedPath
from game.state.game_state import StateCategory
from game.state.stateful_class import StatefulClass, StatefulProp
from utils.types import Point2f


class UnitStatus(Enum):
    PRESPAWN = "PRESPAWN"
    ALIVE = "ALIVE"
    DEAD = "DEAD"


class UnitModel(StatefulClass):
    max_health: ClassVar[int] = 200
    _state_category: ClassVar[StateCategory] = "UNIT"

    id: int = StatefulProp(read_only=True)  # type: ignore
    id_wave: int = StatefulProp(read_only=True)  # type: ignore

    dist: float = StatefulProp()  # type: ignore
    health: int = StatefulProp()  # type: ignore
    speed: float = StatefulProp()  # type: ignore
    status: UnitStatus = StatefulProp()  # type: ignore

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
                health=cls.max_health,
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

    @property
    def interpolated_pos(self) -> Point2f:
        frac, idx = modf(self.dist)
        idx = int(idx)

        pt = self.ppath.points[idx]

        new_pos = (
            pt.pos[0] + frac * pt.dir[0],
            pt.pos[1] + frac * pt.dir[1],
        )
        return new_pos
