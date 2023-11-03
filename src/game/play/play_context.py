from dataclasses import dataclass
from typing import Awaitable, Callable

from game.game import Game

SleepFunction = Callable[[float], Awaitable[None]]


@dataclass
class PlayContext:
    game: Game
    render: bool
    sleep_fn: SleepFunction
