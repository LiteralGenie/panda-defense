from dataclasses import dataclass
from typing import Generic, Iterator, TypeVar

from sortedcontainers import SortedKeyList

from game.unit.unit import Unit, UnitStatus

_Id = int
_UnitIds = set[int]

T = TypeVar("T")


@dataclass
class _WeightedUnitId(Generic[T]):
    id: int
    weight: T


class UnitManager:
    """Store a list of units and create db-like indices"""

    _units: dict[_Id, Unit]

    _units_by_path: dict[_Id, SortedKeyList[_WeightedUnitId[float], float]]
    _units_by_status: dict[UnitStatus, _UnitIds]
    _units_by_wave: dict[_Id, _UnitIds]

    def __init__(self):
        self._units = dict()

        self._units_by_path = dict()
        self._units_by_status = dict()
        self._units_by_wave = dict()

    def add(self, unit: Unit):
        self._units[unit.id] = unit
        self._add_by_path(unit)
        self._add_by_status(unit)
        self._add_by_wave(unit)

    def set_dist(self, unit: Unit, dist: float):
        old = _WeightedUnitId(id=unit.id, weight=unit.dist)
        self._units_by_path[unit.ppath.id].remove(old)

        unit.dist = dist
        self._add_by_path(unit)

    def set_status(self, unit: Unit, status: UnitStatus):
        self._units_by_status[unit.status].remove(unit.id)

        unit.status = status
        self._add_by_status(unit)

    def _add_by_path(self, unit: Unit):
        self._units_by_path.setdefault(unit.ppath.id, SortedKeyList(key=self._weigh))

        item = _WeightedUnitId(id=unit.id, weight=unit.dist)
        self._units_by_path[unit.ppath.id].add(item)

    def _add_by_status(self, unit: Unit):
        self._units_by_status.setdefault(unit.status, set())
        self._units_by_status[unit.status].add(unit.id)

    def _add_by_wave(self, unit: Unit):
        self._units_by_wave.setdefault(unit.id_wave, set())
        self._units_by_wave[unit.id_wave].add(unit.id)

    @staticmethod
    def _weigh(wui: _WeightedUnitId[T]) -> T:
        return wui.weight

    def __iter__(self) -> Iterator[Unit]:
        yield from self._units.values()

    @property
    def prespawn(self) -> list[Unit]:
        ids = self._units_by_status.get(UnitStatus.PRESPAWN, set())
        return [self._units[id] for id in ids]

    @property
    def alive(self) -> list[Unit]:
        ids = self._units_by_status.get(UnitStatus.ALIVE, set())
        return [self._units[id] for id in ids]

    @property
    def dead(self) -> list[Unit]:
        ids = self._units_by_status.get(UnitStatus.DEAD, set())
        return [self._units[id] for id in ids]

    @property
    def by_path(self) -> dict[int, list[Unit]]:
        return {
            id_path: [self._units[wui.id] for wui in wuis]
            for id_path, wuis in self._units_by_path.items()
        }

    def list_from_path(self, id_path: int) -> list[Unit]:
        wuis = self._units_by_path[id_path]
        return [self._units[x.id] for x in wuis]

    def list_from_wave(self, id_wave: int) -> list[Unit]:
        ids = self._units_by_wave.get(id_wave, set())
        return [self._units[id] for id in ids]
