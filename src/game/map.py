from panda3d.core import NodePath

import g
from game.parameterized_path import ParameterizedPath
from game.scenario import Path
from game.stateful import Stateful, StatefulProp
from game.tower import Tower
from game.unit.unit import Unit


class Lane:
    pnode: NodePath | None

    ppath: ParameterizedPath
    units: list[Unit]

    def __init__(self, ppath: ParameterizedPath):
        self.pnode = None

        self.ppath = ppath
        self.units = []

    def add_unit(self, unit: Unit):
        self.units.append(unit)

    def remove_unit(self, unit: Unit):
        self.units = [u for u in self.units if u is not unit]  # todo: faster deletion
        unit.delete()

    def render(self, parent: NodePath, period_s: float):
        for unit in self.units:
            unit.render(parent, period_s, self.ppath)


class Map(Stateful):
    pnode: NodePath | None

    lanes: dict[int, Lane]
    towers: list[Tower] = StatefulProp()  # type: ignore

    def __init__(self, paths: dict[int, Path]):
        super().__init__()
        self.pnode = None

        self.lanes = self._init_lanes(paths)
        self.towers = []

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

        for path in self.lanes.values():
            path.render(NodePath(self.pnode), period_s)

        for tower in self.state["towers"].current:
            tower.render(NodePath(self.pnode), period_s)

        super().save_props()

    def add_tower(self, tower: Tower):
        self.towers.append(tower)
        self.state["towers"].mark_for_check()

    @classmethod
    def _init_lanes(cls, paths: dict[int, Path]) -> dict[int, Lane]:
        ppaths = {id: ParameterizedPath(p) for id, p in paths.items()}
        result = {id: Lane(p) for id, p in ppaths.items()}
        return result
