from abc import ABC

from game.controller.controller_globals import ControllerGlobals
from game.id_manager import IdManager
from game.towers.range import Range
from utils.types import Point2


class TowerModel(ABC):
    id: int
    pos: Point2
    range: Range

    globals: ControllerGlobals

    def __init__(self, pos: Point2, range: Range, globals: ControllerGlobals):
        self.id = IdManager.create()

        self.pos = pos
        self.range = range

        self.globals = globals

    def serialize(self):
        return dict(
            id=self.id,
            pos=self.pos,
            range=self.range.serialize(),
        )
