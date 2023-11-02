from dataclasses import dataclass

from game.play.range_cache import RangeCache


@dataclass
class PlayCache:
    ranges: RangeCache
