from dataclasses import dataclass
from multiprocessing.connection import Connection

from game.controller.controller_cache import ControllerCache
from game.controller.controller_globals import ControllerGlobals
from game.game_model import GameModel


@dataclass
class ControllerContext:
    game: GameModel
    cache: ControllerCache
    globals: ControllerGlobals
    render_pipe: Connection
