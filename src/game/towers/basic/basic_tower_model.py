from game.controller.controller_globals import ControllerGlobals
from game.towers.range import PyramidalRange
from game.towers.tower_model import TowerModel
from utils.types import Point2


class BasicTowerModel(TowerModel):
    attack_speed: float
    attack_speed_guage: float
    damage: int

    def __init__(self, pos: Point2, globals: ControllerGlobals):
        super().__init__(
            pos,
            range=PyramidalRange(2),
            globals=globals,
        )

        self.attack_speed = 0.25
        self.attack_speed_guage = 0
        self.damage = 30
