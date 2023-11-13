from copy import deepcopy

from game.towers.tower_model import TowerModel
from game.towers.tower_range.square_range import SquareRange
from utils.types import Point2


class LaserTowerModel(TowerModel):
    cost = 15
    default_range = SquareRange(1)

    @classmethod
    def create(cls, pos: Point2):  # type: ignore
        return super().create(
            attack_speed=0.25,
            attack_speed_guage=0,
            damage=20,
            pos=pos,
            range=deepcopy(cls.default_range),
        )
