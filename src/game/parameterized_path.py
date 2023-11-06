from dataclasses import dataclass
from functools import lru_cache

from game.scenario import Direction, Path
from utils.misc_utils import find_index
from utils.types import Point2


@dataclass
class PointWithDirection:
    pos: Point2
    dir: Point2


class ParameterizedPath:
    id: int
    points: list[PointWithDirection]
    length: int

    def __init__(self, path: Path):
        self.id = path.id

        start = path.start
        dir = _dir_to_pt(path.segments[0].dir)
        self.points = [PointWithDirection(pos=start, dir=dir)]

        for segment in path.segments:
            (step_x, step_y) = _dir_to_pt(segment.dir)

            for _ in range(1, segment.dist):
                pos = (start[0] + step_x, start[1] + step_y)
                dir = (step_x, step_y)
                self.points.append(PointWithDirection(pos=pos, dir=dir))

        self.length = len(self.points)

    @lru_cache(maxsize=None)
    def point_to_param(self, point: Point2) -> int | None:
        return find_index(self.points, lambda pt: pt.pos == point)


def _dir_to_pt(dir: Direction) -> Point2:
    step_x = 0
    if dir == "x":
        step_x = 1
    if dir == "-x":
        step_x = -1

    step_y = 0
    if dir == "y":
        step_y = 1
    if dir == "-y":
        step_y = -1

    return (step_x, step_y)
