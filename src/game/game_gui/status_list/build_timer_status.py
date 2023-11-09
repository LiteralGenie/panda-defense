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
            text_fg=(0.56, 0.56, 0.56, 1),
        )

        self.hide()

        self._status_sub = self._subscribe_status()

    def _subscribe_status(self):
        status_key: str = GameModel.round_idx.key  # type: ignore

        def on_next(ev: GameEvent):
            match ev:
                case StateUpdated("GAME", _, key, _):
                    if key != status_key:
                        return

                    tick_end = GVG.data.meta.tick_end
                    cb = self._create_countdown_cb(tick_end)
                    g.base.task_mgr.do_method_later(0.25, cb, f"build_timer_{uuid4()}")
                case _:
                    pass

        return GVG.event_subj.subscribe(on_next=on_next)

    def _create_countdown_cb(self, t_end_s: float):
        self["text"] = f"{t_end_s - time.time():.0f}s"
        self.show()

        def task_fn(task: Task):
            rem = t_end_s - time.time()

            if rem > 0:
                self["text"] = f"{rem:.0f}s"
                return task.again
            else:
                self.hide()
                return task.done

        return task_fn

    def delete(self):
        self._status_sub.dispose()
