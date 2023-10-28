from renderable import Renderable


class TowerNode:
    pass


class Tower(Renderable):
    pnode_factory = TowerNode

    def __init__(self):
        super().__init__()
