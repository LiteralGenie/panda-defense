from dataclasses import dataclass
from multiprocessing.connection import Connection

from game.game_state import GameState
from game.view.game_view_cache import GameViewCache


@dataclass
class GameViewGlobals:
    cache: GameViewCache
    event_pipe: Connection
    state: GameState
