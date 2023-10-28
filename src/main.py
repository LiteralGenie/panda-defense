from direct.showbase.ShowBase import ShowBase

from map import Map
from renderable import Renderable


class AppNode(ShowBase):
    def __init__(self):
        super().__init__()


class App(Renderable):
    pnode_factory = AppNode

    map: Map | None

    def add_map(self, map: Map):
        self.map = map


app = App()
app.run()
