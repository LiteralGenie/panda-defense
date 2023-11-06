from dataclasses import dataclass

from game.event_manager import EventManager


@dataclass
class ControllerGlobals:
    ev_mgr: EventManager
