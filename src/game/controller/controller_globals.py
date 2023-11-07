from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from game.events.event_manager import EventManager


class ControllerGlobals:
    ev_mgr: "ClassVar[EventManager]"


CG = ControllerGlobals
