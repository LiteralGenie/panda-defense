class PandaNode:
    def removeNode(self) -> None: ...

class NodePath:
    def __init__(self, x: str | PandaNode | "NodePath") -> None: ...
    def attachNewNode(self, name: str) -> "NodePath": ...
    def getChild(self, n: int) -> "NodePath": ...
    def removeNode(self) -> None: ...
    def reparentTo(self, other: "NodePath") -> None: ...
    def setH(self, heading: float) -> "NodePath": ...
    def setPos(self, x: float, y: float, z: float) -> "NodePath": ...
    def setScale(self, scale: float) -> "NodePath": ...

class Point3:
    def __init__(self, x: float, y: float, z: float) -> None: ...
