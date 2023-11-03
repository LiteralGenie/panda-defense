from dataclasses import dataclass


@dataclass
class RenderUnitPosition:
    pass


@dataclass
class RenderUnitMovement:
    pass


@dataclass
class RenderUnitDeath:
    pass


RenderUnitEvents = RenderUnitPosition | RenderUnitMovement | RenderUnitDeath
