from dataclasses import dataclass
from typing import Literal

from utils.types import Point2

Direction = Literal["x", "-x", "y", "-y"]


@dataclass
class Segment:
    dist: int
    dir: Direction


@dataclass
class Path:
    id: int
    start: Point2
    segments: list[Segment]


@dataclass
class Wave:
    id: int
    enemies: int
    id_path: int
    spawn_delay_ticks: int


@dataclass
class Round:
    waves: list[Wave]


@dataclass
class Scenario:
    rounds: list[Round]
    paths: dict[int, Path]
