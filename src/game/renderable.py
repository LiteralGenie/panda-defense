import copy
from abc import ABC

from panda3d.core import PandaNode


class Stateful(ABC):
    pnode: PandaNode
    state: dict[str, "State"]

    def __init__(self):
        self.pnode = None
        self.state = dict()

    def save_props(self):
        for prop in self.state.values():
            prop.save()


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

    def save(self):
        self.prev = copy.copy(self.current)
        self.first_change = False


class StatefulProp:
    _name: str

    def __init__(self):
        self._name = ""

    def __set_name__(self, owner: Stateful, name):
        self._name = name

    def __get__(self, obj: Stateful, objtype=None):
        obj.state.setdefault(self._name, State(None))
        return obj.state[self._name].current

    def __set__(self, obj: Stateful, value):
        obj.state.setdefault(self._name, State(None))
        obj.state[self._name].set(value)
