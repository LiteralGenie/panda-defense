from tower import Tower
from unit import Unit


class MapNode:
    pass


class Map:
    pnode_factory = MapNode

    units: list[Unit]
    towers: list[Tower]

    def __init__(self):
        self.units = []
        self.towers = []

    def add_unit(self, unit: Unit):
        self.units.append(unit)

    def add_tower(self, tower: Tower):
        self.towers.append(tower)
