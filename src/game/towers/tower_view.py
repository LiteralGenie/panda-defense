from abc import ABC
from typing import ClassVar

from direct.actor.Actor import Actor
from panda3d.core import NodePath

import g
from game.towers.tower_model import TowerModel


class TowerView(ABC):
    actor: ClassVar[Actor] = Actor(
        "data/assets/glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf",
    )

    id: int
    model: TowerModel
    pnode: Actor

    def __init__(self, id: int):
        self.id = id
        self.model = self._init_model()
        self.pnode = self._init_pnode()

    def _init_model(self):
        return TowerModel.load(self.id)

    def _init_pnode(self) -> Actor:
        pnode = NodePath("")
        self.__class__.actor.instance_to(pnode)

        pnode.getChild(0).setScale(20)
        pnode.setPos(self.model.pos + (0,))
        pnode.reparent_to(g.render)

        return pnode  # type: ignore
