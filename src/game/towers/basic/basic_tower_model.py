from game.state.stateful_class import StatefulProp
from game.towers.tower_model import TowerModel
from game.towers.tower_range import PyramidalRange
from utils.types import Point2


class BasicTowerModel(TowerModel):
    type = "basic"

    attack_speed: float = StatefulProp(read_only=True)  # type: ignore
    attack_speed_guage: float = StatefulProp()  # type: ignore
    damage: int = StatefulProp(read_only=True)  # type: ignore

    @classmethod
    def create(cls, pos: Point2):  # type: ignore
        return super().create(
            pos,
            range=PyramidalRange(2),
            attack_speed=0.25,
            attack_speed_guage=0,
            damage=30,
        )
