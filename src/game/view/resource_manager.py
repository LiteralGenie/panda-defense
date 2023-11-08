from typing import ClassVar

from direct.actor.Actor import Actor
from panda3d.core import NodePath

import g


class ResourceManager:
    _asset_dir: ClassVar[str] = "data/assets/"

    actors: dict[str, Actor]
    assets: dict[str, NodePath]

    def __init__(self):
        self.actors = dict()
        self.assets = dict()

    def load_actor(self, name: str):
        fp = self._asset_dir + name
        return Actor(fp)

    def load_asset(self, name: str):
        fp = self._asset_dir + name
        return g.loader.laodModel(fp)
