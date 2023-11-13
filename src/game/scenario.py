from typing import Any, Literal, TypedDict

Direction = Literal["x", "-x", "y", "-y"]


class Segment(TypedDict):
    dist: int
    dir: Direction


class Path(TypedDict):
    id: int
    start: list[int]
    segments: list[Segment]


class Wave(TypedDict):
    id: int
    id_path: int
    enemies: int
    spawn_delay_ticks: int


class Round(TypedDict):
    waves: list[Wave]


class Scenario(TypedDict):
    rounds: list[Round]
    paths: dict[int, Path]


def parse_scenario(raw_scenario: Any) -> Scenario:
    """I forgot JSON objects cant have numeric keys so need to convert it here"""

    raw_scenario["paths"] = {int(k): v for k, v in raw_scenario["paths"].items()}
    return raw_scenario
