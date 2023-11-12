from abc import ABC, abstractmethod, abstractproperty
from typing import ClassVar

from direct.actor.Actor import Actor
from panda3d.core import NodePath
from reactivex.abc import DisposableBase

from game.towers.tower_model import TowerModel


class TowerView(ABC):
    display_name: ClassVar[str] = "???"

    id: int
    model: TowerModel
    pnode: Actor

    _event_sub: DisposableBase

    def __init__(self, id: int):
        self.id = id
        self.model = self._init_model()
        self._init_assets()

    def _init_model(self):
        return TowerModel.load(self.id)

    def _init_assets(self):
        pnode = NodePath("")
        self.__class__.actor.instance_to(pnode)

        pnode.setPos(self.model.pos + (0,))
        pnode.reparent_to(render)

        self.pnode = pnode  # type: ignore

    @classmethod
    @abstractproperty
    def actor(cls) -> Actor:
        ...

    @classmethod
    @abstractmethod
    def preload_actor(cls) -> None:
        ...

    @classmethod
    @abstractproperty
    def placeholder(cls) -> Actor:
        ...

    @classmethod
    @abstractmethod
    def preload_placeholder(cls) -> None:
        ...

    def delete(self):
        self.pnode.remove_node()
