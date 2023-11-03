import sys
import time

from game.game import Game
from game.map import Map
from game.parameterized_path import ParameterizedPath
from game.play.apply_damage import apply_damage
from game.play.play_cache import PlayCache
from game.play.play_context import PlayContext, SleepFunction
from game.play.range_cache import RangeCache
from game.scenario import Scenario
from game.tower.basic import BasicTower
from game.tower.render_tower_events import RenderTowerPosition
from game.unit.render_unit_events import (
    RenderUnitDeath,
    RenderUnitMovement,
    RenderUnitPosition,
)
from game.unit.unit import Unit, UnitStatus
from game.unit.unit_manager import UnitManager

TICK_FREQ_S = 24
TICK_PERIOD_S = 1 / TICK_FREQ_S
BUILD_TIME_S = 30


async def play_game(scenario: Scenario, sleep_fn: SleepFunction):
    game = Game(scenario, time.time())

    ctx = PlayContext(
        game=game,
        render=True,
        sleep_fn=sleep_fn,
    )
    game = ctx.game

    ppaths = {id: ParameterizedPath(p) for id, p in ctx.game.scenario.paths.items()}
    cache = PlayCache(
        ppaths=ppaths,
        ranges=RangeCache(list(ppaths.values())),
        start_ticks={0: 0},
    )

    tower = BasicTower(pos=(1, 1))
    game.towers.append(tower)
    tower.render_queue.append(RenderTowerPosition())

    for i in range(len(game.scenario.rounds)):
        game.round_idx = i
        cache.start_ticks[game.round_idx] = game.tick + 1

        print(f"Round {game.round_idx}")
        await _play_round(ctx, cache)

        # Clear out render queues
        ctx.game.render(0)

    print(f"Game end")
    _teardown()


async def _play_round(ctx: PlayContext, cache: PlayCache):
    game = ctx.game

    game.unit_mgr = UnitManager()
    _init_units_for_round(ctx, cache)

    while True:
        delay = game.next_tick - time.time()
        if delay > 0 and ctx.render:
            # Render game state if we have time before next tick
            # (This should happen every tick unless potato processor causes
            #  backlogged updates that skip this rendering step)
            game.render(delay)
            delay = game.next_tick - time.time()
        if delay > 0:
            await ctx.sleep_fn(delay)

        game.tick += 1
        print(game.tick)
        start = time.time()

        # Validate and apply actions
        for action in game.action_queue:
            pass
        game.action_queue = []

        # Update game state
        is_round_end = _update_game_state(ctx, cache)

        # Calculations should never (consistently) run over than tick period
        # (assuming the tick times are constant and reproducible
        #  simplifies a lot of the client-server and multiplayer syncing)
        elapsed = time.time() - start
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


def _init_units_for_round(ctx: PlayContext, cache: PlayCache):
    for wave in ctx.game.current_round.waves:
        for _ in range(wave.enemies):
            unit = Unit(
                id_wave=wave.id,
                ppath=cache.ppaths[wave.id_path],
                speed=0.25,
            )
            ctx.game.unit_mgr.add(unit)


def _update_game_state(ctx: PlayContext, cache: PlayCache) -> bool:
    _spawn_units(ctx, cache)
    _move_units(ctx, cache)

    apply_damage(ctx, cache)

    all_dead = len(list(ctx.game.unit_mgr)) == len(ctx.game.unit_mgr.dead)
    return all_dead


def _spawn_units(ctx: PlayContext, cache: PlayCache):
    # calculate ticks since round began
    round_idx = ctx.game.round_idx
    ticks_elapsed = ctx.game.tick - cache.start_ticks[round_idx]

    for wave in ctx.game.current_round.waves:
        tick_end = (wave.enemies - 1) * wave.spawn_delay_ticks
        is_spawn_tick = 0 == ticks_elapsed % wave.spawn_delay_ticks

        if ticks_elapsed <= tick_end and is_spawn_tick:
            u = ctx.game.unit_mgr.select(
                id_wave=wave.id,
                status=UnitStatus.PRESPAWN,
                fetch_one=True,
            )[0]
            ctx.game.unit_mgr.set_status(u, UnitStatus.ALIVE)
            u.render_queue.append(RenderUnitPosition())


def _move_units(ctx: PlayContext, cache: PlayCache):
    for unit in ctx.game.unit_mgr.alive:
        ctx.game.unit_mgr.set_dist(unit, unit.dist + unit.speed)
        unit.render_queue.append(RenderUnitMovement())

        # Remove unit if it completed path
        if unit.dist >= unit.ppath.length - 1:
            ctx.game.unit_mgr.set_status(unit, UnitStatus.DEAD)
            unit.render_queue.append(RenderUnitDeath())


def _teardown():
    actors = [Unit]
    for a in actors:
        if a.model:
            a.model.cleanup() # type: ignore
            a.model.removeNode()

    renderables = [Map]
    for r in renderables:
        if r.model:
            r.model.removeNode()
