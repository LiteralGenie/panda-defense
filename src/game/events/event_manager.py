from dataclasses import dataclass
from multiprocessing.connection import Connection
from typing import Any

from game.events.render_event import RenderEvent
from game.game_model import GameModel
from game.state.game_state import StateEvent

GameEvent = RenderEvent | StateEvent


@dataclass
class TickEvents:
    round: int
    tick: int
    tick_end: float

    events: list[GameEvent]


class EventManager:
    pending: list[Any]
    pipe: Connection

    def __init__(self, pipe: Connection):
        self.pipe = pipe
        self.pending = []

    def add(self, ev: Any):
        self.pending.append(ev)

    def flush(self, game: GameModel) -> None:
        events = self.pending
        self.pending = []

        result = TickEvents(
            round=game.round_idx,
            tick=game.tick,
            tick_end=game.next_tick,
            events=events,
        )

        self.pipe.send(result)
