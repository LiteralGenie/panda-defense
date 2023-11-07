# pyright: reportPrivateUsage=false

from abc import ABC
from typing import Any, ClassVar, Self, Type

from game.shared_globals import SG
from game.state.state import StateCategory


class StatefulClass(ABC):
    _state_category: ClassVar[StateCategory]

    _id: int

    def __init__(self, id: int):
        self._id = id

    @classmethod
    def load(cls, id: int) -> Self:
        return cls(id)

    def _register(self, init_state: Any):
        SG.entities.create(self._state_category, self.__class__, init_state)

    def _update(self, key: str, val: Any):
        SG.entities.update(self._state_category, self._id, key, val)

    def _delete(self):
        SG.entities.delete(self._state_category, self._id)

    @property
    def _state_data(self):
        return SG.entities.data[self._state_category][self._id]["data"]


class StatefulProp:
    key: str
    read_only: bool

    def __init__(self, read_only: bool = False):
        self.read_only = read_only

    def __set_name__(self, cls: Type[Any], key: str):
        self.key = key

    def __get__(self, obj: StatefulClass | None, objtype: Any = None):
        if obj is None:
            # Caller referenced the class object, not the instance
            # so they must want the descriptor itself
            return self

        return obj._state_data[self.key]

    def __set__(self, obj: StatefulClass, value: Any):
        if self.read_only:
            raise Exception(f"Cannot set readonly attribute {self.key} to {value}")
        obj._update(self.key, value)
