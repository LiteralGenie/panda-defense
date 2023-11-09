from reactivex.abc import DisposableBase

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.status_list.enemy_count_subj import enemy_count_subj
from game.game_gui.status_list.status_label import StatusLabel


class EnemyStatus(StatusLabel):
    _status_sub: DisposableBase

    def __init__(self, parent: BetterDirectFrame):
        super().__init__(
            parent,
            text_fg=(0.85, 0.85, 0.85, 1),
        )

        self._status_sub = self._subscribe_status()

    def _subscribe_status(self):
        # Init text
        num_alive = 0
        num_total = 0
        self["text"] = f"{num_alive} / {num_total}"

        # Listen for changes
        def on_next(x: tuple[int, int]):
            num_alive, num_total = x
            self["text"] = f"{num_alive} / {num_total}"

        return enemy_count_subj().subscribe(on_next=on_next)

    def delete(self):
        self._status_sub.dispose()
