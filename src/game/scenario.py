from typing import Literal, TypedDict

from utils.types import Point2

Direction = Literal["x", "-x", "y", "-y"]


class Segment(TypedDict):
    dist: int
    dir: Direction


class Path(TypedDict):
    id: int
    start: Point2
    segments: list[Segment]


class Wave(TypedDict):
    id: int
    enemies: int
    id_path: int
    spawn_delay_ticks: int


class Round(TypedDict):
    waves: list[Wave]


class Scenario(TypedDict):
    rounds: list[Round]
    paths: dict[int, Path]
