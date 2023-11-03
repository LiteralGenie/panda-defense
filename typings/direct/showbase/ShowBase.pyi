from typing import Any, Coroutine

from panda3d.core import WindowProperties

class ShowBase:
    camera: "_Camera"
    task_mgr: "_TaskManager"
    win: "_Window"

    def disableMouse(self) -> None: ...
    def run(self) -> None: ...

class _Camera:
    def setP(self, p: float) -> None: ...
    def setPos(self, x: float, y: float, z: float) -> None: ...

class _TaskManager:
    def add(self, x: Coroutine[Any, Any, Any]) -> None:
        pass

class _Window:
    def requestProperties(self, properties: WindowProperties) -> None: ...
