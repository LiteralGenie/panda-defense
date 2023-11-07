from dataclasses import dataclass
from multiprocessing.connection import Connection
from typing import ClassVar

from reactivex import Subject

from game.events.event_manager import GameEvent
from game.scenario import Scenario
from game.view.game_view_cache import GameViewCache


@dataclass
class GameViewMetaInfo:
    scenario: Scenario
    tick: int
    tick_end: float
    round: int


class GameViewGlobals:
    cache: ClassVar[GameViewCache]
    event_pipe: ClassVar[Connection]
    event_subj: ClassVar[Subject[GameEvent]]
    meta: GameViewMetaInfo


GVG = GameViewGlobals
