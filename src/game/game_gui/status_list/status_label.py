from game.game_gui.better_direct_frame import BetterDirectFrame


class StatusLabel(BetterDirectFrame):
    def __init__(
        self,
        parent: BetterDirectFrame,
        text_fg: tuple[float, float, float, float],
    ):
        super().__init__(
            parent,
            frameColor=(0, 0, 0, 0.95),
            text_scale=0.04,
            text="Health: 32",
            text_fg=text_fg,
        )

    def recalculate_layout(self):
        w = self.width
        h = self.height

        h *= 1.25  # todo: replace this with height of TextNode / 2

        self["text_pos"] = (w / 2, h / 2)

    def delete(self):
        pass
