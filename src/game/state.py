from dataclasses import dataclass
from typing import Any, Callable, Literal, Type, TypeAlias, TypedDict

StateCategory = Literal["TOWER", "UNIT"]
_STATE_CATEGORIES: list[StateCategory] = ["TOWER", "UNIT"]


class _Entry(TypedDict):
    cls: Type[Any]
    data: dict[str, Any]


_EntriesById = dict[int, _Entry]
_DataByCategory = dict[StateCategory, _EntriesById]

_OnEvent: TypeAlias = "Callable[[StateEvent], None]"


class State:
    """
    Basically a 2-layer dict with this shape
    {
        category_1: {
            id_1: entry_1,
            id_2: entry_2,
        },

        category_2: {
            ...
        }
    }

    all entries should have an id
    all entries for a category may not have the same type

    operations on this data are classified as one of...
        creation - new entry with unique id is added under a category
        update   - existing entry has one of its existing values updated
        delete   - entry is removed from a category

    all operations generate an "event" describing this change
    this event is pushed into a queue that's eventually flushed
        the motivation being that this allows the renderer process to both
        maintain a copy of this state and also animate the changes
            animations based on a state change usually only involve a single entity (eg unit movement)
            animations that involve multiple entities (eg tower attacking unit)
            are triggered by more specific events not generated by this class
    """

    data: _DataByCategory
    events: "list[StateEvent]"
    on_event: _OnEvent

    def __init__(self, on_event: _OnEvent):
        self.data = {cat: dict() for cat in _STATE_CATEGORIES}
        self.on_event = on_event

    def create(
        self,
        category: StateCategory,
        cls: Type[Any],
        data: dict[str, Any],
    ):
        self.data[category][data["id"]] = _Entry(
            cls=cls,
            data=data,
        )

        ev = StateCreated(category=category, cls=cls, data=data)
        self._log_event(ev)

    def update(self, category: StateCategory, id: int, key: str, value: Any):
        self.data[category][id]["data"][key] = value

        ev = StateUpdated(category=category, id=id, key=key, value=value)
        self._log_event(ev)

    def delete(self, category: StateCategory, id: int):
        data = self.data[category][id]
        del self.data[category][id]

        ev = StateDeleted(category=category, data=data)
        self._log_event(ev)

    def _log_event(self, event: "StateEvent"):
        self.on_event(event)


@dataclass
class StateCreated:
    category: StateCategory
    cls: Type[Any]
    data: dict[str, Any]

    @property
    def id(self):
        return self.data["id"]


@dataclass
class StateUpdated:
    category: StateCategory
    id: int
    key: str
    value: Any


@dataclass
class StateDeleted:
    category: StateCategory
    data: Any

    @property
    def id(self):
        return self.data["id"]


StateEvent = StateCreated | StateUpdated | StateDeleted
