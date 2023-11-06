from game.range import PyramidalRange
from game.tower.tower import Tower
from utils.types import Point2


class BasicTower(Tower):
    attack_speed: float
    attack_speed_guage: float
    damage: int

    def __init__(self, pos: Point2):
        super().__init__(
            pos,
            range=PyramidalRange(2),
        )

        self.attack_speed = 0.25
        self.attack_speed_guage = 0
        self.damage = 30
