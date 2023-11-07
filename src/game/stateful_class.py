from abc import ABC
from typing import Any

from game.shared_globals import SG
from game.state import State, StateCategory


class StatefulClass(ABC):
    id: int
    _category: StateCategory
    _state: State

    def __init__(self, category: StateCategory):
        self._category = category

    @property
    def _state_data(self):
        return SG.entities.data[self._category][self.id]

    def create(self, id: int, **data: Any):
        SG.entities.create(self._category, dict(id=id, **data))

    def update(self, key: str, val: Any):
        SG.entities.update(self._category, self.id, key, val)

    def delete(self):
        SG.entities.delete(self._category, self.id)


class StatefulProp:
    key: str
    read_only: bool

    def __init__(self, key: str, read_only: bool = False):
        self.key = key
        self.read_only = read_only

    def __get__(self, obj: StatefulClass | None, objtype: Any = None):
        if obj is None:
            # Caller referenced the class object, not the instance
            # so they must want the descriptor itself
            return self

        return obj._state_data[self.key]  # type: ignore

    def __set__(self, obj: StatefulClass, value: Any):
        if self.read_only:
            raise Exception(f"Cannot set readonly attribute {self.key} to {value}")
        obj.update(self.key, value)
