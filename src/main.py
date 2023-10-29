import simplepbr
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

import g
from map import Map
from tower import Tower
from unit import Unit


class App(ShowBase):
    map: Map | None

    def __init__(self):
        super().__init__()
        simplepbr.init()

        self.camera.setPos(0, 0, 20)
        self.camera.setP(-90)
        self.disableMouse()

        properties = WindowProperties()
        properties.setOrigin(7680, 0)
        properties.setSize(3840, 2160)

        self.win.requestProperties(properties)

        self.map = Map()
        self.map.add_unit(Unit())
        self.map.add_tower(Tower())
        self.map.render(self.render)

    def add_map(self, map: Map):
        self.map = map


app = App()
app.run()
