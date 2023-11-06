from dataclasses import dataclass

from game.state import GameState
from game.view.game_view_cache import GameViewCache


@dataclass
class GameViewGlobals:
    cache: GameViewCache
    state: GameState
