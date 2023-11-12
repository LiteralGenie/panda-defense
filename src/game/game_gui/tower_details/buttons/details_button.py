from typing import Literal

from direct.gui.DirectGui import DGG

from game.colors import C_DEFAULT, C_T_WARN, C_WARN
from game.game_gui.better_direct_frame import BetterDirectFrame
from utils.gui_utils import darken

_BG_COLORS = {
    None: C_DEFAULT + (1,),
    "warn": C_WARN + (1,),
}

_TEXT_COLORS = {
    None: (0.95, 0.95, 0.95, 1),
    "warn": C_T_WARN + (1,),
}


_SUFFIX_COLORS = {
    None: (0.69, 0.64, 0.26, 1),
    "warn": C_T_WARN + (1,),
}

_ICONS = {
    None: "+",
    "warn": "-",
}


class DetailsButton(BetterDirectFrame):
    icon: BetterDirectFrame
    suffix: str
    suffix_frame: BetterDirectFrame
    variant: Literal["warn"] | None

    def __init__(
        self,
        parent: BetterDirectFrame,
        variant: Literal["warn"] | None,
        text: str,
        suffix: str,
    ):
        super().__init__(
            parent,
            frameColor=_BG_COLORS[variant],
            state=DGG.NORMAL,
            text=text,
            text_fg=_TEXT_COLORS[variant],
            text_font=loader.load_font("data/assets/fonts/Roboto/Roboto-Bold.ttf"),
            text_scale=0.03,
        )

        self.icon = BetterDirectFrame(
            self,
            text=_ICONS[variant],
            frameColor=(0, 0, 0, 1),
            text_fg=_TEXT_COLORS[variant],
            text_font=loader.load_font("data/assets/fonts/Roboto/Roboto-Bold.ttf"),
            text_scale=0.04,
        )

        self.suffix_frame = BetterDirectFrame(
            self,
            text=suffix,
            text_fg=_SUFFIX_COLORS[variant],
            text_font=loader.load_font("data/assets/fonts/Roboto/Roboto-Bold.ttf"),
            text_scale=0.03,
        )

        self.variant = variant

        self.bind(DGG.B1PRESS, lambda _: self._on_mousedown())
        self.bind(DGG.B1RELEASE, lambda _: self._on_mouseup())

    def recalculate_layout(self):
        w = self.width
        h = self.height

        h *= 1.25  # anchor is at top-left, not center of text

        self["text_pos"] = (w / 2, h / 2)
        self.icon["text_pos"] = (w * 0.04, h * 1.035 / 2)
        self.suffix_frame["text_pos"] = (w * 0.935, h * 1.035 / 2)

    def _on_mousedown(self):
        self["frameColor"] = darken(_BG_COLORS[self.variant], 0.5)

    def _on_mouseup(self):
        self["frameColor"] = _BG_COLORS[self.variant]
