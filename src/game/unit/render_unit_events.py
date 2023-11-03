from dataclasses import dataclass


@dataclass
class RenderUnitPosition:
    pass


@dataclass
class RenderUnitMovement:
    pass


RenderUnitEvents = RenderUnitPosition | RenderUnitMovement
