from abc import ABC, abstractmethod

from panda3d.core import NodePath, PandaNode


class Renderable(ABC):
    pnode: PandaNode
    state: dict[str, "State"]

    def __init__(self):
        self.pnode = None
        self.state = dict()

    @abstractmethod
    def render(self, parent: NodePath):
        ...


class State:
    def __init__(self, initial):
        self.prev = None
        self.current = initial

        self.first_change = True
        self.needs_check = True

    def set(self, value):
        self.current = value
        self.needs_check = True

    def mark_for_check(self):
        self.needs_check = True

    def reset(self):
        self.prev = self._current.copy()
        self.first_change = False


class StatefulProp:
    _name: str

    def __init__(self):
        self._name = ""

    def __set_name__(self, owner: Renderable, name):
        self._name = name

    def __get__(self, obj: Renderable, objtype=None):
        obj.state.setdefault(self._name, State(None))
        return obj.state[self._name].current

    def __set__(self, obj: Renderable, value):
        obj.state.setdefault(self._name, State(None))
        obj.state[self._name].set(value)
