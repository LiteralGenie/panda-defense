from dataclasses import dataclass


@dataclass
class RenderTowerPosition:
    pass


@dataclass
class RenderTowerAttack:
    pass


RenderTowerEvents = RenderTowerPosition | RenderTowerAttack
