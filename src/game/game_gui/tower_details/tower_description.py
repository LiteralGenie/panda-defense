from game.game_gui.better_direct_frame import BetterDirectFrame


class TowerDescription(BetterDirectFrame):
    def __init__(self, parent: BetterDirectFrame):
        super().__init__(
            parent,
            frameColor=(0, 0, 0, 0),
            text="",
            text_fg=(0.95, 0.95, 0.95, 1),
            text_font=loader.load_font("data/assets/fonts/Roboto/Roboto-Medium.ttf"),
            text_scale=0.03,
        )

    def recalculate_layout(self):
        w = self.width

        self["text_pos"] = (w / 2, 0)
