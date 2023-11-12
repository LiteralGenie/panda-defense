from game.game_gui.better_direct_frame import BetterDirectFrame


class TowerDetails(BetterDirectFrame):
    def __init__(self, parent: BetterDirectFrame):
        super().__init__(
            parent,
            frameColor=(0, 0, 0, 1),
        )

    def recalculate_layout(self):
        pass
