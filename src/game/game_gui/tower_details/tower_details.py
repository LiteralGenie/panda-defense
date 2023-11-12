from typing import ClassVar

from game.events.event_manager import GameEvent
from game.events.game_actions import SellTowerAction, UpgradeTowerAction
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.game_gui.tower_details.buttons.details_button import DetailsButton
from game.game_gui.tower_details.buttons.sell_button import SellButton
from game.game_gui.tower_details.buttons.upgrade_button import UpgradeButton
from game.game_gui.tower_details.tower_description import TowerDescription
from game.state.game_state import StateUpdated
from game.view.game_view_globals import GVG


class TowerDetails(BetterDirectFrame):
    # Percentage of container height
    DESCRIPTION_HEIGHT: ClassVar[float] = 0.05
    # Percentage of container width
    BUTTON_HEIGHT: ClassVar[float] = 0.12
    # Percentage of container width
    GAP_HEIGHT: ClassVar[float] = 0.035

    id_tower: int | None

    description: TowerDescription
    sell_button: DetailsButton
    upgrade_damage_button: DetailsButton
    upgrade_range_button: DetailsButton
    upgrade_speed_button: DetailsButton

    def __init__(self, parent: BetterDirectFrame):
        super().__init__(
            parent,
            frameColor=(0, 0, 0, 0.95),
        )

        self.id_tower = None

        self._init_components()
        self._sub_events()

    def set_id_tower(self, id_tower: int):
        self.id_tower = id_tower
        self._update_button_text()

    def _update_button_text(self):
        if not self.id_tower:
            return

        tower = GVG.data.views.towers[self.id_tower]

        self.description["text"] = f"{tower.display_name} Upgrades"

        self.sell_button.suffix_frame["text"] = f"{tower.model.cost}G"

        self.upgrade_damage_button["text"] = f"Damage ({tower.model.damage:.0f} -> {1.1 * tower.model.damage:.0f})"  # type: ignore
        self.upgrade_range_button["text"] = f"Range ({tower.model.range.radius:.2f} -> {1 + tower.model.range.radius:.2f})"  # type: ignore
        self.upgrade_speed_button["text"] = f"Attack Speed ({tower.model.attack_speed:.2f} -> {1.1 * tower.model.attack_speed:.2f})"  # type: ignore

    def recalculate_layout(self):
        self._layout_description()
        self._layout_buttons()
        self._layout_delete_button()

    def _init_components(self):
        self.description = TowerDescription(self)

        self.sell_button = SellButton(
            self,
            0,
            on_click=lambda: [
                GVG.event_pipe.send(
                    SellTowerAction(
                        id_player=GVG.data.meta.id_player,
                        id_tower=self.id_tower,  # type: ignore
                    )
                ),
                messenger.send("hideTowerDetails"),
            ],
        )

        self.upgrade_damage_button = UpgradeButton(
            self,
            7,
            on_click=lambda: [
                GVG.event_pipe.send(
                    UpgradeTowerAction(
                        id_player=GVG.data.meta.id_player,
                        id_tower=self.id_tower,  # type: ignore
                        trait="damage",
                    )
                ),
                self._update_button_text(),
            ],
        )
        self.upgrade_range_button = UpgradeButton(
            self,
            15,
            on_click=lambda: [
                GVG.event_pipe.send(
                    UpgradeTowerAction(
                        id_player=GVG.data.meta.id_player,
                        id_tower=self.id_tower,  # type: ignore
                        trait="range",
                    ),
                ),
                self._update_button_text(),
            ],
        )
        self.upgrade_speed_button = UpgradeButton(
            self,
            7,
            on_click=lambda: [
                GVG.event_pipe.send(
                    UpgradeTowerAction(
                        id_player=GVG.data.meta.id_player,
                        id_tower=self.id_tower,  # type: ignore
                        trait="speed",
                    ),
                ),
                self._update_button_text(),
            ],
        )

    def _layout_description(self):
        cw = self.width
        ch = self.height

        offset = 0.075 * cw

        tl_x = offset
        tl_y = -offset

        w = cw - 2 * offset
        h = ch * self.DESCRIPTION_HEIGHT

        self.description.set_xy((tl_x, tl_y))
        self.description.set_frame_size((w, h))
        self.description.recalculate_layout()

    def _layout_buttons(self):
        cw = self.width
        ch = self.height

        buttons = [
            self.upgrade_damage_button,
            self.upgrade_range_button,
            self.upgrade_speed_button,
        ]

        h = -cw * self.BUTTON_HEIGHT
        gh = -cw * self.GAP_HEIGHT

        w = cw + 2 * gh

        start_y = ch * self.DESCRIPTION_HEIGHT

        for idx, button in enumerate(buttons):
            tl_x = -gh
            tl_y = start_y + idx * (h + gh)

            button.set_xy((tl_x, tl_y))
            button.set_frame_size((w, h))
            button.recalculate_layout()

    def _layout_delete_button(self):
        cw = self.width
        ch = self.height

        offset = cw * self.GAP_HEIGHT

        h = cw * -self.BUTTON_HEIGHT
        w = cw - 2 * offset

        tl_x = offset
        tl_y = ch - h + offset

        self.sell_button.set_xy((tl_x, tl_y))
        self.sell_button.set_frame_size((w, h))
        self.sell_button.recalculate_layout()

    def _sub_events(self):
        # Listen for changes
        def on_next(ev: GameEvent):
            match ev:
                case StateUpdated("TOWER", id, _, _):
                    if id == self.id_tower:
                        self._update_button_text()
                case _:
                    pass

        sub = GVG.event_subj.subscribe(on_next=on_next)
        self._sub_sink.append(lambda: sub.dispose())
