from dataclasses import dataclass

from game.parameterized_path import ParameterizedPath

_PathId = int


@dataclass
class GameViewCache:
    ppaths: dict[_PathId, ParameterizedPath]
