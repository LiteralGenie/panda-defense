from typing import Any, TypedDict

from utils.types import Point2


class GameState(TypedDict):
    scenario: dict[Any, Any]
    towers: dict[int, "_TowerState"]
    units: dict[int, "_UnitState"]


class _RangeState(TypedDict):
    points: list[Point2]


class _TowerState(TypedDict):
    id: int
    pos: Point2
    range: _RangeState


class _UnitState(TypedDict):
    id: int
    id_path: int
    dist: float
    health: float
    speed: float
    status: str
