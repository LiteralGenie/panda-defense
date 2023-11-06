from dataclasses import dataclass

from game.controller.range_cache import RangeCache
from game.parameterized_path import ParameterizedPath

_PathId = int
_RoundId = int


@dataclass
class ControllerCache:
    ppaths: dict[_PathId, ParameterizedPath]
    ranges: RangeCache
    start_ticks: dict[_RoundId, int]
