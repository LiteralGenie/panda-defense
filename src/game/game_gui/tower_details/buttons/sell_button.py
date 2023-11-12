from typing import Callable

from direct.gui.DirectGui import DGG

from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.tower_details.buttons.details_button import DetailsButton


class SellButton(DetailsButton):
    on_click: Callable[[], None]
    price: int

    def __init__(
        self,
        parent: BetterDirectFrame,
        price: int,
        on_click: Callable[[], None],
    ):
        super().__init__(
            parent,
            text="Sell",
            variant="warn",
            suffix=f"{price}G",
        )

        self.on_click = on_click
        self.price = price

        self.bind(DGG.B1RELEASE, lambda _: [on_click(), self._on_mouseup()])
