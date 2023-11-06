from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from game.game_model import GameModel
    from game.state import GameState

T = TypeVar("T")


@dataclass
class TickEvents:
    tick: int
    tick_end: float

    state: "GameState"
    events: list[Any]


class EventManager:
    pending: list[Any]

    def __init__(self):
        self.pending = []

    def add(self, ev: Any):
        self.pending.append(ev)

    def dump(self, game: "GameModel") -> TickEvents:
        events = self.pending
        self.pending = []

        result = TickEvents(
            tick=game.tick,
            tick_end=game.next_tick,
            state=game.serialize(),
            events=events,
        )

        return result
