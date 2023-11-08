from dataclasses import dataclass
from multiprocessing.connection import Connection
from typing import ClassVar

from reactivex import Subject

from game.events.event_manager import GameEvent
from game.scenario import Scenario
from game.view.game_view_cache import GameViewData
from game.view.resource_manager import ResourceManager


@dataclass
class GameViewMetaInfo:
    scenario: Scenario
    tick: int
    tick_end: float
    round: int


class GameViewGlobals:
    data: ClassVar[GameViewData]
    event_pipe: ClassVar[Connection]
    event_subj: ClassVar[Subject[GameEvent]]
    resource_mgr: ClassVar[ResourceManager]


GVG = GameViewGlobals
