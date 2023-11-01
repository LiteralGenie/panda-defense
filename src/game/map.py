from panda3d.core import NodePath

import g
from game.renderable import Renderable, StatefulProp
from game.tower import Tower
from game.unit import Unit


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

    def remove_unit(self, unit: Unit):
        self.units = [u for u in self.units if u is not unit]
        self.state["units"].mark_for_check()

    def add_tower(self, tower: Tower):
        self.towers.append(tower)
        self.state["towers"].mark_for_check()

    def render(self, parent: NodePath, period_s: float):
        if not self.pnode:
            self.pnode = NodePath("")

            board = g.loader.loadModel("data/assets/board.gltf")
            for idx_row in range(-15, 15):
                for idx_col in range(-15, 15):
                    b = self.pnode.attachNewNode("")
                    b.setPos(idx_col * 2, idx_row * 2, 0)
                    board.instanceTo(b)

            self.pnode.reparentTo(parent)

        # Remove deleted units from scene graph
        units_change = self.state["units"]
        if units_change.needs_check:
            if units_change.prev:
                deleted: list[Unit] = [
                    old for old in units_change.prev if old not in units_change.current
                ]
                for unit in deleted:
                    unit.delete()

        #
        for unit in units_change.current:
            unit.render(NodePath(self.pnode), period_s)

        for tower in self.state["towers"].current:
            tower.render(NodePath(self.pnode), period_s)

        super().save_props()

    def _loadModel(self):
        pass
