import time

import simplepbr
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import WindowProperties

from game.game import Game
from game.map import Map
from game.play import PlayContext, play_game
from game.scenario import Path, Round, Scenario, Segment, Wave


def build_test_scenario():
    path = Path(
        start=(0, 10),
        segments=[
            Segment(axis="-y", dist=20),
        ],
    )

    waves = [
        Wave(
            enemies=5,
            path=path,
        ),
    ]

    round = Round(waves=waves)

    return Scenario(rounds=[round])


class App(ShowBase):
    map: Map | None

    def __init__(self):
        super().__init__()
        simplepbr.init()

        self.camera.setPos(0, 0, 40)
        self.camera.setP(-90)
        self.disableMouse()

        properties = WindowProperties()
        properties.setOrigin(7680, 0)
        properties.setSize(3840, 2160)

        self.win.requestProperties(properties)

        self.game = Game(scenario=build_test_scenario())

        ctx = PlayContext(
            game=self.game,
            first_tick=time.time(),
            render=True,
            sleep_fn=Task.pause,
        )
        self.task_mgr.add(play_game(ctx))


app = App()
app.run()
