from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection

from game.controller.controller import play_game
from game.event_manager import TickEvents
from game.scenario import Path, Round, Scenario, Segment, Wave

# from faster_fifo import Queue


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
                    enemies=15,
                    id_path=path["id"],
                    spawn_delay_ticks=4,
                )
            ]
        ),
        Round(
            waves=[
                Wave(
                    id=2,
                    enemies=15,
                    id_path=path["id"],
                    spawn_delay_ticks=2,
                )
            ]
        ),
    ]

    return Scenario(
        rounds=rounds,
        paths={path["id"]: path},
    )


def run_renderer(scenario: Scenario, pipe: Connection):
    import simplepbr
    from direct.showbase.ShowBase import ShowBase
    from direct.task.Task import Task
    from panda3d.core import WindowProperties

    class Renderer(ShowBase):
        def __init__(self):
            super().__init__()
            simplepbr.init()

            self.camera.setPos(0, 0, 40)
            self.camera.setP(-90)
            self.disable_mouse()

            properties = WindowProperties()
            properties.set_origin(7680, 0)
            properties.set_size(3840, 2160)

            self.win.request_properties(properties)  # type: ignore

            self.view = None
            self.task_mgr.add(self._check_render_queue)

        def _check_render_queue(self, task: Task):
            if pipe.poll():
                tick: TickEvents = pipe.recv()

                if not self.view:
                    from game.view.game_view import GameView

                    self.view = GameView(tick.state, pipe)

                self.view.render(tick)

            return task.cont

    r = Renderer()
    r.run()


def run_game(scenario: Scenario, pipe: Connection):
    import asyncio

    coro = play_game(scenario, pipe)
    asyncio.run(coro)


if __name__ == "__main__":
    scenario = build_test_scenario()
    parent_conn, child_conn = Pipe()

    game = Process(target=run_game, args=(scenario, parent_conn))
    game.start()

    renderer = Process(target=run_renderer, args=(scenario, child_conn))
    renderer.start()

    game.join()
    renderer.join()
    # renderer.kill()
