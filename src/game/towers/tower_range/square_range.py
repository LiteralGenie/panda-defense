from functools import lru_cache

from game.towers.tower_range.tower_range import TowerRange
from utils.types import Point2


class SquareRange(TowerRange):
    """
    example:
     xxxxx
     xxxxx
     xxxxx   radius=2
     xxxxx
     xxxxx
    """

    radius: int

    def __init__(self, radius: int):
        self.radius = radius
        self.points = self._generate_points(radius)

    @classmethod
    @lru_cache
    def _generate_points(cls, radius: int) -> set[Point2]:
        pts: set[Point2] = set()

        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):
                pts.add((x, y))

        return pts

    def id(self) -> str:
        name = self.__class__.__name__
        return f"{name}_{self.radius}"
