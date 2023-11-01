from dataclasses import dataclass
from typing import Literal

Point = tuple[int, int]


@dataclass
class Segment:
    dist: int
    axis: Literal["x", "-x", "y", "-y"]


@dataclass
class Path:
    start: Point
    segments: list[Segment]


@dataclass
class Wave:
    enemies: int
    path: Path


@dataclass
class Round:
    waves: list[Wave]


@dataclass
class Scenario:
    rounds: list[Round]
