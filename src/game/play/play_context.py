from dataclasses import dataclass
from typing import TYPE_CHECKING, Awaitable, Callable

from game.game import Game

SleepFunction = Callable[[float], Awaitable[None]]

if TYPE_CHECKING:
    from game.battle_gui.battle_gui import BattleGui


@dataclass
class PlayContext:
    game: Game
    gui: "BattleGui | None"
    render: bool
    sleep_fn: SleepFunction
