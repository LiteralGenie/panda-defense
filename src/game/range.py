from abc import ABC, abstractmethod
from functools import lru_cache

from game.scenario import Point


class Range(ABC):
    points: set[Point]

    @abstractmethod
    def id(self) -> str:
        ...


class PyramidalRange(Range):
    """
    example:
        x
       xxx
      xxxxx
     xxxxxxx   radius=3
      xxxxx
       xxx
        x
    """

    radius: int

    def __init__(self, radius: int):
        self.radius = radius
        self.points = self._generate_points(radius)

    @classmethod
    @lru_cache
    def _generate_points(cls, radius: int) -> set[Point]:
        pts: set[Point] = set()

        # Build the upper quarter
        #       x
        #      xxx
        for i in range(1, radius + 1):
            # center tile
            pts.add((0, i))

            # left / right wings
            for j in range(1, radius - i + 1):
                pts.add((-j, i))
                pts.add((j, i))

        # Flip vertically and union
        #       x
        #      xxx
        #
        #      xxx
        #       x
        for pt in pts.copy():
            pts.add((pt[0], -pt[1]))

        # Build center row
        #       x
        #      xxx
        #     xxxxx
        #      xxx
        #       x
        pts.add((0, 0))
        for i in range(1, radius + 1):
            pts.add((-i, 0))
            pts.add((i, 0))

        return pts

    def id(self) -> str:
        name = self.__class__.__name__
        return f"{name}_{self.radius}"
