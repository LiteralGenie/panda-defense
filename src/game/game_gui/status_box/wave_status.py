from reactivex.abc import DisposableBase

from game.events.event_manager import GameEvent
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.status_box.status_label import StatusLabel
from game.game_model import GameModel
from game.state.game_state import StateUpdated
from game.view.game_view_globals import GVG


class RoundStatus(StatusLabel):
    _status_sub: DisposableBase

    def __init__(self, parent: BetterDirectFrame):
        super().__init__(
            parent,
            text_fg=(0.56, 0.56, 0.56, 1),
        )

        self._status_sub = self._subscribe_status()

    def _subscribe_status(self):
        status_key: str = GameModel.round_idx.key  # type: ignore
        num_rounds = len(GVG.data.meta.scenario["rounds"])

        # Init text
        round = GVG.data.meta.round
        self["text"] = f"Round {round + 1} / {num_rounds}"

        # Listen for changes
        def on_next(ev: GameEvent):
            match ev:
                case StateUpdated("GAME", _, key, value):
                    if key != status_key:
                        return

                    self["text"] = f"Round {value + 1} / {num_rounds}"
                case _:
                    pass

        return GVG.event_subj.subscribe(on_next=on_next)

    def delete(self):
        self._status_sub.dispose()
