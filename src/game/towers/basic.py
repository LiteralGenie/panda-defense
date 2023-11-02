from game.range import PyramidalRange
from game.scenario import Point
from game.tower import Tower


class BasicTower(Tower):
    attack_speed: float
    attack_speed_guage: float
    damage: int

    def __init__(self, pos: Point):
        super().__init__(
            pos,
            range=PyramidalRange(2),
        )

        self.attack_speed = 0.25
        self.attack_speed_guage = 0
        self.damage = 30
