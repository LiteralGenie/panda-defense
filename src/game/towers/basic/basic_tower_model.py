from copy import deepcopy

from game.towers.tower_model import TowerModel
from game.towers.tower_range import pyramidal_range
from utils.types import Point2


class BasicTowerModel(TowerModel):
    cost = 5
    default_range = pyramidal_range.PyramidalRange(3)

    @classmethod
    def create(cls, pos: Point2):  # type: ignore
        return super().create(
            attack_speed=0.5,
            attack_speed_guage=0,
            damage=45,
            pos=pos,
            range=deepcopy(cls.default_range),
        )
