from panda3d.core import PandaNode, Point3


class Actor(PandaNode):
    def __init__(self, models: str, anims: dict[str, str] = dict()):
        ...

    def posInterval(self, t: float, pt: Point3):
        ...
