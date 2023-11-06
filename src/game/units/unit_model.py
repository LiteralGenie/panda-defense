from enum import Enum

from game.controller.controller_globals import ControllerGlobals
from game.id_manager import IdManager
from game.parameterized_path import ParameterizedPath
from game.towers.tower_model import TowerModel
from game.units.render_unit_events import (
    RenderUnitDamage,
    RenderUnitDeath,
    RenderUnitMovement,
    RenderUnitSpawn,
)


class UnitStatus(Enum):
    PRESPAWN = "PRESPAWN"
    ALIVE = "ALIVE"
    DEAD = "DEAD"


class UnitModel:
    id: int
    id_wave: int

    dist: float
    health: int
    ppath: ParameterizedPath
    speed: float
    status: UnitStatus

    globals: ControllerGlobals

    def __init__(
        self,
        id_wave: int,
        ppath: ParameterizedPath,
        speed: float,
        globals: ControllerGlobals,
    ):
        self.id = IdManager.create()
        self.id_wave = id_wave

        self.dist = 0
        self.health = 100
        self.ppath = ppath
        self.speed = speed
        self.status = UnitStatus.PRESPAWN

        self.globals = globals

    def serialize(self):
        return dict(
            id=self.id,
            id_path=self.ppath.id,
            dist=self.dist,
            health=self.health,
            speed=self.speed,
            status=self.status,
        )

    def set_dist(self, dist: float):
        self.dist = dist
        self.globals.ev_mgr.add(RenderUnitMovement(ids=[self.id]))

    def set_status(self, status: UnitStatus):
        self.status = status

        match status:
            case UnitStatus.ALIVE:
                self.globals.ev_mgr.add(RenderUnitSpawn(ids=[self.id]))
            case UnitStatus.DEAD:
                self.globals.ev_mgr.add(RenderUnitDeath(ids=[self.id]))
            case UnitStatus.PRESPAWN:
                raise Exception("Attempted to set unit status to PRESPAWN")

    def take_damage(self, damage: int, attacker: TowerModel):
        self.health -= damage
        self.globals.ev_mgr.add(RenderUnitDamage(ids=[self.id, attacker.id]))
