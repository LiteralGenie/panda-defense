from abc import ABC
from typing import ClassVar

from direct.actor.Actor import Actor
from panda3d.core import NodePath

import g
from game.event_manager import TickEvents
from game.towers.render_tower_events import RenderTowerEvents, RenderTowerSpawn
from game.view.game_view_globals import GameViewGlobals
from utils.event_utils import get_latest_event


class TowerView(ABC):
    model: ClassVar[Actor] = Actor(
        "data/assets/glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf",
    )

    id: int
    pnode: Actor

    def __init__(self, id: int):
        self.id = id
        self.pnode = self._init_model()

    def _init_model(self) -> Actor:
        pnode = NodePath("")
        self.__class__.model.instanceTo(pnode)

        pnode.getChild(0).setScale(20)
        pnode.reparentTo(g.render)

        return pnode  # type: ignore

    def render(
        self,
        tick: TickEvents,
        globals: GameViewGlobals,
        events: list[RenderTowerEvents],
    ):
        tower = tick.state["towers"][self.id]

        if get_latest_event(RenderTowerSpawn, events):
            pos = tower["pos"]
            self.pnode.setPos(pos[0], pos[1], 0)
