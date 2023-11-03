from dataclasses import dataclass

from game.parameterized_path import ParameterizedPath
from game.play.range_cache import RangeCache


@dataclass
class PlayCache:
    ppaths: dict[int, ParameterizedPath]
    ranges: RangeCache
