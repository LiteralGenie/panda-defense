from dataclasses import dataclass

from game.parameterized_path import ParameterizedPath
from game.range import Range
from game.scenario import Point
from game.unit.unit import Unit
from utils.misc_utils import find_insertion_index, split_with_lookback


class PathInterval:
    start: int
    end: int

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def filter_units(self, units_sorted: list[Unit]) -> list[Unit]:
        if not len(units_sorted):
            return []

        vals = [u.dist for u in units_sorted]

        if self.start > vals[-1]:
            return []
        if self.end < vals[0]:
            return []

        idx_start = find_insertion_index(vals, self.start)
        idx_end = find_insertion_index(vals, self.end, return_largest_idx=True)

        return units_sorted[idx_start : idx_end + 1]


_PathId = int
PathIntervalMap = dict[_PathId, list[PathInterval]]


@dataclass
class _CacheEntry:
    id_range: str
    intervals: PathIntervalMap


class RangeCache:
    """
    Cache the intersection of each tower range with each path
    (so we don't have to search the whole range for targets)
    """

    _data: dict[Point, _CacheEntry]
    paths: list[ParameterizedPath]

    def __init__(self, paths: list[ParameterizedPath]):
        self._data = dict()
        self.paths = paths

    def get(self, pos: Point, range: Range) -> PathIntervalMap:
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
        intervals: PathIntervalMap = dict()

        for path in self.paths:
            # Map relative coords to absolute coords
            pts = {(pos[0] + pt[0], pos[1] + pt[1]) for pt in range.points}

            # Map coords to path parameters
            params = [path.point_to_param(pt) for pt in pts]

            # Consolidate consecutive params into intervals
            params = sorted(p for p in params if p is not None)
            grouped = split_with_lookback(params, lambda prev, curr: curr - prev > 1)

            intervals[path.id] = [PathInterval(grp[0], grp[-1]) for grp in grouped]

        return _CacheEntry(
            id_range=range.id(),
            intervals=intervals,
        )
