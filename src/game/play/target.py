from dataclasses import dataclass

from game.parameterized_path import ParameterizedPath
from game.play.range_cache import RangeCache
from game.tower import Tower
from game.unit.unit import Unit
from utils.misc_utils import find_or_throw


@dataclass
class Target:
    unit: Unit
    path: ParameterizedPath

    @property
    def rem_dist(self) -> float:
        return self.path.length - self.unit.dist


TargetsByPath = dict[int, list[Target]]


def find_tower_targets(
    tower: Tower,
    units_sorted: dict[int, list[Unit]],
    cache: RangeCache,
) -> TargetsByPath:
    """Find targets in range of tower, grouped by path"""

    ivl_map = cache.get(tower.pos, tower.range)

    targets_by_path: TargetsByPath = dict()
    for id_path, intervals in ivl_map.items():
        path = find_or_throw(cache.paths, lambda p: p.id == id_path)
        targets_by_path[id_path] = []

        for ivl in intervals:
            units = ivl.find_units_sorted(units_sorted[id_path])
            targets = [Target(unit=unit, path=path) for unit in units]
            targets_by_path[id_path].extend(targets)

    return targets_by_path


def consolidate_targets(targets_by_path: TargetsByPath) -> list[Target]:
    """Consolidate targets from all paths into single sorted list"""

    result: list[Target] = []
    for targets in targets_by_path.values():
        result.extend(targets)

    result.sort(key=lambda tgt: tgt.rem_dist)

    return result
