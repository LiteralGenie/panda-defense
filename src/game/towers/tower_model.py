from abc import ABC
from typing import Any, ClassVar

from game.id_manager import IdManager
from game.stateful_class import StatefulClass, StatefulProp
from game.towers.tower_range import TowerRange
from utils.types import Point2


class TowerModel(StatefulClass, ABC):
    type: ClassVar[str]

    id: int
    pos: Point2 = StatefulProp("pos")  # type: ignore
    range: TowerRange = StatefulProp("range", read_only=True)  # type: ignore

    def __init__(
        self,
        pos: Point2,
        range: TowerRange,
        register: bool = True,
        **kwargs: Any,
    ):
        StatefulClass.__init__(self, "TOWER")

        if register:
            self.id = IdManager.create()

            self.create(
                type=self.__class__.type,
                id=self.id,
                pos=pos,
                range=range,
                **kwargs,
            )
        else:
            self.id = kwargs["id"]
