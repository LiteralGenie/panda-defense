from dataclasses import dataclass
from typing import Literal


@dataclass
class RenderTowerAttack:
    id_tower: int
    id_targets: list[int]


@dataclass
class RenderLaserAttack:
    id_tower: int
    id_targets: list[int]
    axis: Literal["x", "y"]


RenderEvent = RenderTowerAttack | RenderLaserAttack
