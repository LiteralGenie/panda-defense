from typing import Any, Callable, ClassVar

from direct.actor.Actor import Actor
from panda3d.core import NodePath

import g


class ResourceManager:
    _asset_dir: ClassVar[str] = "data/assets/"

    actors: dict[str, Actor]
    assets: dict[str, NodePath]

    _loading: set[str]

    def __init__(self):
        self.actors = dict()
        self.assets = dict()
        self._loading = set()

    def load_actor(self, name: str):
        if name not in self.actors:
            fp = self._asset_dir + name
            self.actors[name] = Actor(fp)
        return self.actors[name]

    def preload_actor(self, name: str):
        if name in self.actors:
            return

        if name in self._loading:
            return

        def cb(model: Any):
            self._loading.remove(name)
            if name not in self.actors:
                self.actors[name] = Actor(model)  # type: ignore

        self._loading.add(name)
        g.loader.load_model(self._asset_dir + name, callback=cb)

    def load_asset(self, name: str):
        fp = self._asset_dir + name
        if name not in self.actors:
            fp = self._asset_dir + name
            self.assets[name] = g.loader.load_model(fp)
        return self.assets[name]

    def load_or_register(self, key: str, factory_fn: Callable[[], NodePath]):
        if key not in self.assets:
            pnode = factory_fn()
            self.assets[key] = pnode

        return self.assets[key]
