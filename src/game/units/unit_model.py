from enum import Enum
from typing import Any, ClassVar

from game.id_manager import IdManager
from game.parameterized_path import ParameterizedPath
from game.stateful_class import StatefulClass, StatefulProp


class UnitStatus(Enum):
    PRESPAWN = "PRESPAWN"
    ALIVE = "ALIVE"
    DEAD = "DEAD"


class UnitModel(StatefulClass):
    type: ClassVar[str] = ""

    id: int
    id_wave: int = StatefulProp("id_wave", read_only=True)  # type: ignore

    dist: float = StatefulProp("dist")  # type: ignore
    health: int = StatefulProp("health")  # type: ignore
    speed: float = StatefulProp("speed", read_only=True)  # type: ignore
    status: UnitStatus = StatefulProp("status")  # type: ignore

    ppath: ParameterizedPath

    def __init__(
        self,
        id_wave: int,
        ppath: ParameterizedPath,
        speed: float,
        register: bool = True,
        **kwargs: Any,
    ):
        StatefulClass.__init__(self, "UNIT")

        self.ppath = ppath

        if register:
            self.id = IdManager.create()
            self.create(
                type=self.__class__.type,
                id=self.id,
                id_path=ppath.id,
                id_wave=id_wave,
                dist=0,
                health=100,
                speed=speed,
                status=UnitStatus.PRESPAWN,
                **kwargs,
            )
        else:
            self.id = kwargs["id"]
