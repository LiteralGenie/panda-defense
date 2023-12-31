from dataclasses import dataclass


@dataclass
class RenderTowerAttack:
    id_tower: int
    id_targets: list[int]


@dataclass
class RenderLaserAttack:
    id_tower: int
    id_targets: list[int]


RenderEvent = RenderTowerAttack | RenderLaserAttack
