import simplepbr
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import Task
from panda3d.core import WindowProperties

from game.map import Map
from game.play.play import play_game
from game.scenario import Path, Round, Scenario, Segment, Wave


def build_test_scenario():
    path = Path(
        id=1,
        start=(0, 10),
        segments=[
            Segment(dir="-y", dist=20),
        ],
    )

    rounds = [
        Round(
            waves=[
                Wave(
                    id=1,
                    enemies=5,
                    id_path=path.id,
                    spawn_delay_ticks=4,
                )
            ]
        ),
        Round(
            waves=[
                Wave(
                    id=2,
                    enemies=15,
                    id_path=path.id,
                    spawn_delay_ticks=2,
                )
            ]
        ),
    ]

    return Scenario(
        rounds=rounds,
        paths={path.id: path},
    )


class App(ShowBase):
    map: Map | None

    def __init__(self):
        super().__init__()
        simplepbr.init()

        self.camera.setPos(0, 0, 40)
        self.camera.setP(-90)
        self.disable_mouse()

        properties = WindowProperties()
        properties.set_origin(7680, 0)
        properties.set_size(3840, 2160)

        self.win.request_properties(properties)

        self.task_mgr.add(play_game(build_test_scenario(), Task.pause))


app = App()
app.run()
