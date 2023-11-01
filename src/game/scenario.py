from dataclasses import dataclass
from typing import Literal

Point = tuple[int, int]
Direction = Literal["x", "-x", "y", "-y"]


@dataclass
class Segment:
    dist: int
    dir: Direction


@dataclass
class Path:
    start: Point
    segments: list[Segment]


@dataclass
class Wave:
    enemies: int
    spawn_delay_ticks: int
    path: Path


@dataclass
class Round:
    waves: list[Wave]


@dataclass
class Scenario:
    rounds: list[Round]
