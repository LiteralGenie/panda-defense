from dataclasses import dataclass

from game.parameterized_path import ParameterizedPath
from game.range import Range
from game.scenario import Point
from utils.misc_utils import split_with_lookback

_PathId = int
_Interval = tuple[int, int]
RangeIntervals = dict[_PathId, list[_Interval]]


@dataclass
class _CacheEntry:
    id_range: str
    intervals: RangeIntervals


class RangeCache:
    _data: dict[Point, _CacheEntry]
    paths: list[ParameterizedPath]

    def __init__(self, paths: list[ParameterizedPath]):
        self._data = dict()
        self.paths = paths

    def get(self, pos: Point, range: Range) -> RangeIntervals:
        entry = self._data.get(pos)
        if not entry:
            self._data[pos] = self._create_entry(pos, range)
            return self._data[pos].intervals

        if entry.id_range != range.id():
            self._data[pos] = self._create_entry(pos, range)
            return self._data[pos].intervals

        return entry.intervals

    def remove(self, pos: Point):
        del self._data[pos]

    def _create_entry(self, pos: Point, range: Range) -> _CacheEntry:
        intervals: RangeIntervals = dict()

        for path in self.paths:
            # Map relative coords to absolute coords
            pts = {(pos[0] + pt[0], pos[1] + pt[1]) for pt in range.points}

            # Map coords to path parameters
            params = [path.point_to_param(pt) for pt in pts]

            # Consolidate consecutive params into intervals
            params = sorted(p for p in params if p)
            grouped = split_with_lookback(params, lambda prev, curr: curr - prev > 1)

            intervals[path.id] = [(grp[0], grp[-1]) for grp in grouped]

        return _CacheEntry(
            id_range=range.id(),
            intervals=intervals,
        )
