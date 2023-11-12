from copy import deepcopy

from game.towers.tower_model import TowerModel
from game.towers.tower_range import PyramidalRange
from utils.types import Point2


class BasicTowerModel(TowerModel):
    cost = 5
    default_range = PyramidalRange(4)

    @classmethod
    def create(cls, pos: Point2):  # type: ignore
        return super().create(
            attack_speed=0.5,
            attack_speed_guage=0,
            damage=30,
            pos=pos,
            range=deepcopy(cls.default_range),
        )
