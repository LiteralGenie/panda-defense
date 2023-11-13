import json
import pathlib
import time
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection

from panda3d.core import loadPrcFile

from game.controller.controller import play_game
from game.events.event_manager import TickEvents
from game.scenario import Scenario, parse_scenario


def run_renderer(
    first_tick: float,
    scenario: Scenario,
    id_player: int,
    pipe: Connection,
):
    import simplepbr
    from direct.showbase.ShowBase import ShowBase
    from direct.task.Task import Task

    class Renderer(ShowBase):
        def __init__(self):
            loadPrcFile(str(pathlib.Path(__file__).parent / "data" / "Config.prc"))

            super().__init__()
            simplepbr.init(use_normal_maps=True)

            self.camera.setPos(0, 0, 40)
            self.camera.setP(-90)
            self.disable_mouse()

            from game.view.game_view import GameView

            self.view = GameView(first_tick, scenario, id_player, pipe)
            self.task_mgr.add(self._check_render_queue)

        def _check_render_queue(self, task: Task):
            if pipe.poll():
                update: TickEvents = pipe.recv()
                self.view.render(update)

            return task.cont

    r = Renderer()
    r.run()


def run_game(
    first_tick: float,
    scenario: Scenario,
    id_player: int,
    pipe: Connection,
):
    import asyncio

    coro = play_game(first_tick, scenario, id_player, pipe)
    asyncio.run(coro)


if __name__ == "__main__":
    first_tick = time.time()
    parent_conn, child_conn = Pipe()

    fp_scenario = pathlib.Path(__file__).parent / "data" / "scenarios" / "1_test.json"
    scenario: Scenario = parse_scenario(json.load(open(fp_scenario)))

    game = Process(
        target=run_game,
        args=(
            first_tick,
            scenario,
            3232,
            parent_conn,
        ),
    )
    renderer = Process(
        target=run_renderer,
        args=(
            first_tick,
            scenario,
            3232,
            child_conn,
        ),
    )

    game.start()
    renderer.start()

    game.join()
    renderer.join()
    # renderer.kill()
