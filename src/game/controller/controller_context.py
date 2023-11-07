from dataclasses import dataclass
from multiprocessing.connection import Connection

from game.controller.controller_cache import ControllerCache
from game.game_model import GameModel


@dataclass
class ControllerContext:
    game: GameModel
    cache: ControllerCache
    render_pipe: Connection
