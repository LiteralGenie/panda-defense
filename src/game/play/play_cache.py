from dataclasses import dataclass

from game.parameterized_path import ParameterizedPath
from game.play.range_cache import RangeCache

_PathId = int
_RoundId = int


@dataclass
class PlayCache:
    ppaths: dict[_PathId, ParameterizedPath]
    ranges: RangeCache
    start_ticks: dict[_RoundId, int]
