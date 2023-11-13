from abc import ABC, abstractmethod

from utils.types import Point2


class TowerRange(ABC):
    points: set[Point2]

    @abstractmethod
    def id(self) -> str:
        ...
