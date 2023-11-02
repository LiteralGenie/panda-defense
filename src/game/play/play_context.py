from dataclasses import dataclass
from typing import Awaitable, Callable

from game.game import Game


@dataclass
class PlayContext:
    game: Game

    first_tick: float
    render: bool
    sleep_fn: Callable[[float], Awaitable[None]]
