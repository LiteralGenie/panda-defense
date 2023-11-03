import sqlite3
from sqlite3 import Connection
from typing import Iterator, Literal, NotRequired, TypedDict, Unpack

from game.unit.unit import Unit, UnitStatus
from utils.where_builder import WhereBuilder

_Id = int


class _Filters(TypedDict):
    id_path: NotRequired[_Id]
    id_wave: NotRequired[_Id]

    dist: NotRequired[float]
    status: NotRequired[UnitStatus]


class UnitManager:
    """Store a list of units and create db-like indices"""

    _units: dict[_Id, Unit]

    _db: Connection

    def __init__(self):
        self._units = dict()

        self._db = self._init_db()

    def add(self, unit: Unit):
        self._units[unit.id] = unit
        self._insert(unit)

    def set_dist(self, unit: Unit, dist: float):
        unit.dist = dist
        self._insert(unit)

    def set_status(self, unit: Unit, status: UnitStatus):
        unit.status = status
        self._insert(unit)

    def select(
        self,
        fetch_one: bool = False,
        order_by: Literal["id", "id_wave", "id_path", "dist", "status", "dist"] = "id",
        descending: bool = False,
        **filters: Unpack[_Filters],
    ) -> list[Unit]:
        wb = WhereBuilder("AND")

        if id_wave := filters.get("id_wave"):
            wb.add("id_wave = ?", [id_wave])

        if id_path := filters.get("id_path"):
            wb.add("id_path = ?", [id_path])

        if dist := filters.get("dist"):
            wb.add("dist = ?", [dist])

        if status := filters.get("status"):
            wb.add("status = ?", [status.value])

        asc_or_desc = "DESC" if descending else "ASC"

        where, values = wb.print()

        query = self._db.execute(
            f"""
            SELECT id FROM units
            {where}
            ORDER BY {order_by} {asc_or_desc}
            """,
            values,
        )

        rows = [query.fetchone()] if fetch_one else query.fetchall()
        return [self._units[r["id"]] for r in rows]

    def clear(self) -> None:
        self._units.clear()
        self._db.execute("DELETE FROM units")

    def _init_db(self) -> Connection:
        db = sqlite3.connect(":memory:", detect_types=True)
        db.row_factory = sqlite3.Row

        db.execute(
            """
            CREATE TABLE units (
                id          INTEGER     PRIMARY KEY,
                id_wave     INTEGER,
                id_path     INTEGER,

                dist        REAL,
                status      TEXT
            )
            """
        )

        return db

    def _insert(self, unit: Unit):
        self._db.execute(
            """
            INSERT OR REPLACE INTO units
                (id, id_wave, id_path, dist, status)
            VALUES
                (?, ?, ?, ?, ?)
            """,
            [unit.id, unit.id_wave, unit.ppath.id, unit.dist, unit.status.value],
        )

    def __iter__(self) -> Iterator[Unit]:
        yield from self._units.values()

    @property
    def prespawn(self) -> list[Unit]:
        return self.select(status=UnitStatus.PRESPAWN)

    @property
    def alive(self) -> list[Unit]:
        return self.select(status=UnitStatus.ALIVE)

    @property
    def dead(self) -> list[Unit]:
        return self.select(status=UnitStatus.DEAD)
