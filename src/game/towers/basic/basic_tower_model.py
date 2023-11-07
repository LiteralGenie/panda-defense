from game.stateful_class import StatefulProp
from game.towers.tower_model import TowerModel
from game.towers.tower_range import PyramidalRange
from utils.types import Point2


class BasicTowerModel(TowerModel):
    type = "basic"

    attack_speed: float = StatefulProp("attack_speed", read_only=True)  # type: ignore
    attack_speed_guage: float = StatefulProp("attack_speed_guage")  # type: ignore
    damage: int = StatefulProp("damage", read_only=True)  # type: ignore

    def __init__(self, pos: Point2):
        super().__init__(
            pos,
            range=PyramidalRange(2),
            attack_speed=0.25,
            attack_speed_guage=0,
            damage=30,
        )
