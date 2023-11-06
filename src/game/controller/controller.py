import asyncio
import sys
import time
from multiprocessing.connection import Connection

from game.controller.apply_damage import apply_damage
from game.controller.controller_cache import ControllerCache
from game.controller.controller_context import ControllerContext
from game.controller.controller_globals import ControllerGlobals
from game.controller.range_cache import RangeCache
from game.event_manager import EventManager
from game.game_model import GameModel
from game.parameterized_path import ParameterizedPath
from game.scenario import Scenario
from game.towers.basic.basic_tower_model import BasicTowerModel
from game.units.unit_manager import UnitManager
from game.units.unit_model import UnitModel, UnitStatus

TICK_FREQ_S = 4
TICK_PERIOD_S = 1 / TICK_FREQ_S
BUILD_TIME_S = 3


async def play_game(scenario: Scenario, render_pipe: Connection):
    globals = ControllerGlobals(ev_mgr=EventManager())

    ppaths = {id: ParameterizedPath(p) for id, p in scenario["paths"].items()}
    cache = ControllerCache(
        ppaths=ppaths,
        ranges=RangeCache(list(ppaths.values())),
        start_ticks={0: 0},
    )

    game = GameModel(scenario, time.time(), globals=globals)

    ctx = ControllerContext(
        game=game,
        cache=cache,
        globals=globals,
        render_pipe=render_pipe,
    )

    tower = BasicTowerModel(pos=(1, 1), globals=ctx.globals)
    game.add_tower(tower)

    for i in range(len(game.scenario["rounds"])):
        game.round_idx = i
        cache.start_ticks[game.round_idx] = game.tick + 1

        print(f"Round {game.round_idx}")
        await _play_round(ctx)

    print(f"Game end")


async def _play_round(ctx: ControllerContext):
    game = ctx.game

    game.unit_mgr = UnitManager()
    _init_units_for_round(ctx)

    while True:
        # Update view
        evs = ctx.globals.ev_mgr.dump(ctx.game)
        ctx.render_pipe.send(evs)

        # Wait for tick start
        delay = game.next_tick - time.time()
        if delay > 0:
            await asyncio.sleep(delay)

        game.tick += 1
        # print("Tick", game.tick)
        start = time.time()

        # Validate and apply actions
        for action in game.action_queue:
            pass
        game.action_queue = []

        # Update game state
        is_round_end = _update_game_state(ctx)

        # Calculations should never (consistently) run over than tick period
        # (assuming the tick times are constant and reproducible
        #  simplifies a lot of the client-server and multiplayer syncing)
        tick_end = time.time()
        elapsed = tick_end - start
        if elapsed > TICK_PERIOD_S * 0.8:
            print(f"Mid-tick calculations took {elapsed * 1000:.0f}ms", file=sys.stderr)

        # Stop loop on round end
        if is_round_end:
            print("Build phase")
            game.next_tick = game.next_tick + BUILD_TIME_S
            break
        else:
            game.next_tick = game.next_tick + TICK_PERIOD_S
            continue

    # Update view
    evs = ctx.globals.ev_mgr.dump(ctx.game)
    ctx.render_pipe.send(evs)


def _init_units_for_round(ctx: ControllerContext):
    for wave in ctx.game.current_round["waves"]:
        for _ in range(wave["enemies"]):
            unit = UnitModel(
                id_wave=wave["id"],
                ppath=ctx.cache.ppaths[wave["id_path"]],
                speed=0.25,
                globals=ctx.globals,
            )
            ctx.game.add_unit(unit)


def _update_game_state(ctx: ControllerContext) -> bool:
    _spawn_units(ctx)
    _move_units(ctx)

    apply_damage(ctx)

    all_dead = len(list(ctx.game.unit_mgr)) == len(ctx.game.unit_mgr.dead)
    return all_dead


def _spawn_units(ctx: ControllerContext):
    # calculate ticks since round began
    round_idx = ctx.game.round_idx
    ticks_elapsed = ctx.game.tick - ctx.cache.start_ticks[round_idx]

    for wave in ctx.game.current_round["waves"]:
        tick_end = (wave["enemies"] - 1) * wave["spawn_delay_ticks"]
        is_spawn_tick = 0 == ticks_elapsed % wave["spawn_delay_ticks"]

        if ticks_elapsed <= tick_end and is_spawn_tick:
            u = ctx.game.unit_mgr.select(
                id_wave=wave["id"],
                status=UnitStatus.PRESPAWN,
                fetch_one=True,
            )[0]
            ctx.game.unit_mgr.set_status(u, UnitStatus.ALIVE)


def _move_units(ctx: ControllerContext):
    for unit in ctx.game.unit_mgr.alive:
        ctx.game.unit_mgr.set_dist(unit, unit.dist + unit.speed)

        # Remove unit if it completed path
        if unit.dist >= unit.ppath.length - 1:
            ctx.game.unit_mgr.set_status(unit, UnitStatus.DEAD)
