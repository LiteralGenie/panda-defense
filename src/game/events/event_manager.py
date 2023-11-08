from dataclasses import dataclass
from multiprocessing.connection import Connection
from typing import Any

from game.events.render_event import RenderEvent
from game.game_model import GameModel
from game.state.state import StateEvent

GameEvent = RenderEvent | StateEvent


@dataclass
class TickEvents:
    round: int
    tick: int
    tick_end: float

    events: list[GameEvent]


class EventManager:
    game: GameModel
    pipe: Connection

    pending: list[Any]

    def __init__(self, game: GameModel, pipe: Connection):
        self.game = game
        self.pipe = pipe

        self.pending = []

    def add(self, ev: Any):
        self.pending.append(ev)

    def flush(self) -> None:
        events = self.pending
        self.pending = []

        result = TickEvents(
            round=self.game.round_idx,
            tick=self.game.tick,
            tick_end=self.game.next_tick,
            events=events,
        )

        self.pipe.send(result)
