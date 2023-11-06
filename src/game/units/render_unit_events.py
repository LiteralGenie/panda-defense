from dataclasses import dataclass


@dataclass
class RenderUnitSpawn:
    ids: list[int]


@dataclass
class RenderUnitMovement:
    ids: list[int]


@dataclass
class RenderUnitDamage:
    ids: list[int]


@dataclass
class RenderUnitDeath:
    ids: list[int]


RenderUnitEvents = (
    RenderUnitSpawn | RenderUnitMovement | RenderUnitDamage | RenderUnitDeath
)
