from dataclasses import dataclass


@dataclass
class RenderTowerSpawn:
    ids: list[int]


RenderTowerEvents = RenderTowerSpawn
