from panda3d.core import NodePath

import g
from renderable import Renderable, StatefulProp
from tower import Tower
from unit import Unit


class Map(Renderable):
    units: list[Unit] = StatefulProp()  # type: ignore
    towers: list[Tower] = StatefulProp()  # type: ignore

    def __init__(self):
        super().__init__()

        self.units = []
        self.towers = []

    def add_unit(self, unit: Unit):
        self.units.append(unit)
        self.state["units"].mark_for_check()

    def add_tower(self, tower: Tower):
        self.towers.append(tower)
        self.state["towers"].mark_for_check()

    def render(self, parent: NodePath):
        if not self.pnode:
            self.pnode = NodePath("")

            board = g.loader.loadModel("data/assets/board.gltf")
            for idx_row in range(-10, 10):
                for idx_col in range(-10, 10):
                    b = self.pnode.attachNewNode("")
                    b.setPos(idx_col * 2, idx_row * 2, 0)
                    board.instanceTo(b)

            self.pnode.reparentTo(parent)

        if self.state["units"].needs_check:
            deleted = []  # todo
            for x in deleted:
                pass

        for unit in self.state["units"].current:
            unit.render(NodePath(self.pnode))

        for tower in self.state["towers"].current:
            tower.render(NodePath(self.pnode))

    def _loadModel(self):
        pass
