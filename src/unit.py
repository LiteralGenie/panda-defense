from renderable import Renderable


class UnitNode:
    pass


class Unit(Renderable):
    pnode_factory = UnitNode

    def __init__(self):
        super().__init__()
