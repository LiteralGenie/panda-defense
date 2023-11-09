from reactivex.abc import DisposableBase

from game.events.event_manager import GameEvent
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.status_list.status_label import StatusLabel
from game.player.player_model import PlayerModel
from game.shared_globals import SG
from game.state.game_state import StateUpdated
from game.view.game_view_globals import GVG


class GoldStatus(StatusLabel):
    _status_sub: DisposableBase

    def __init__(self, parent: BetterDirectFrame):
        super().__init__(
            parent,
            text_fg=(0.69, 0.64, 0.26, 1),
        )

        self._status_sub = self._subscribe_status()

    def _subscribe_status(self):
        status_key: str = PlayerModel.gold.key  # type: ignore
        id_player = GVG.data.meta.id_player

        # Init text
        player = SG.state.data["PLAYER"][id_player]["data"]
        self["text"] = f"Gold: {player['gold']}"

        # Listen for changes
        def on_next(ev: GameEvent):
            match ev:
                case StateUpdated("PLAYER", id, key, value):
                    if id != id_player:
                        return

                    if key != status_key:
                        return

                    self["text"] = f"Gold: {value}"
                case _:
                    pass

        return GVG.event_subj.subscribe(on_next=on_next)

    def delete(self):
        self._status_sub.dispose()
