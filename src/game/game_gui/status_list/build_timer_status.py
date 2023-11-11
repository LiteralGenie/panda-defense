import time
from uuid import uuid4

from direct.task.Task import Task
from reactivex.abc import DisposableBase

import g
from game.events.event_manager import GameEvent
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.status_list.status_label import StatusLabel
from game.game_model import GameModel
from game.state.game_state import StateUpdated
from game.view.game_view_globals import GVG


class BuildTimerStatus(StatusLabel):
    _status_sub: DisposableBase

    def __init__(self, parent: BetterDirectFrame):
        super().__init__(
            parent,
            text_fg=(0.85, 0.85, 0.85, 1),
        )

        self.hide()

        self._status_sub = self._subscribe_status()

    def _subscribe_status(self):
        status_key: str = GameModel.round_idx.key  # type: ignore

        self._start_countdown()

        def on_next(ev: GameEvent):
            match ev:
                case StateUpdated("GAME", _, key, _):
                    if key != status_key:
                        return

                    self._start_countdown()
                case _:
                    pass

        return GVG.event_subj.subscribe(on_next=on_next)

    def _start_countdown(self):
        tick_end = GVG.data.meta.tick_end
        self["text"] = f"{tick_end - time.time():.0f}s"
        self.show()

        def task_fn(task: Task):
            rem = tick_end - time.time()
            if rem > 0:
                self["text"] = f"{rem:.0f}s"
                return task.again
            else:
                self.hide()
                return task.done

        g.base.task_mgr.do_method_later(0.25, task_fn, f"build_timer_{uuid4()}")

    def delete(self):
        self._status_sub.dispose()
