from typing import Any

import reactivex.operators as ops
from reactivex import Observable

from game.events.event_manager import GameEvent
from game.game_model import GameModel
from game.state.game_state import StateUpdated
from game.units.unit_model import UnitModel, UnitStatus
from game.view.game_view_globals import GVG

_NumAlive = int
_NumTotal = int
_Result = tuple[_NumAlive, _NumTotal]


def _count_current_enemies() -> int:
    meta = GVG.data.meta
    round = meta.scenario["rounds"][meta.round]
    result = sum(w["enemies"] for w in round["waves"])
    return result


def enemy_count_subj() -> Observable[_Result]:
    status_key: str = UnitModel.status.key  # type: ignore
    round_key: str = GameModel.round_idx.key  # type: ignore

    num_alive = _count_current_enemies()
    num_total = num_alive

    def on_event(ev: GameEvent):
        nonlocal num_alive
        nonlocal num_total

        match ev:
            case StateUpdated("GAME", _, key, value):
                if key != round_key:
                    return

                num_total = _count_current_enemies()
                num_alive = num_total

                return (num_alive, num_total)
            case StateUpdated("UNIT", _, key, value):
                if key != status_key:
                    return

                if value == UnitStatus.DEAD:
                    num_alive -= 1
                    return (num_alive, num_total)
            case _:
                pass

    result: Observable[Any] = GVG.event_subj.pipe(
        ops.map(on_event),
        ops.filter(lambda v: v != None),
        ops.start_with((num_alive, num_total)),
        ops.debounce(0.1),
    )

    return result
