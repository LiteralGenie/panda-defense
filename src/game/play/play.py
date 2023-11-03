import sys
import time

from game.game import Game
from game.parameterized_path import ParameterizedPath
from game.play.apply_damage import apply_damage
from game.play.play_cache import PlayCache
from game.play.play_context import PlayContext, SleepFunction
from game.play.range_cache import RangeCache
from game.scenario import Scenario
from game.tower.basic import BasicTower
from game.tower.render_tower_events import RenderTowerPosition
from game.unit.render_unit_events import RenderUnitMovement, RenderUnitPosition
from game.unit.unit import Unit

TICK_FREQ_S = 4
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
    )

    tower = BasicTower(pos=(1, 1))
    game.towers.append(tower)
    tower.render_queue.append(RenderTowerPosition())

    for i in range(len(game.scenario.rounds)):
        game.round = i
        print(f"Round {game.round}")
        await _play_round(ctx, cache)

    print(f"Game end")


async def _play_round(ctx: PlayContext, cache: PlayCache):
    game = ctx.game

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

        # Raise warning if this tick took a while to finish
        elapsed = time.time() - start
        if elapsed > TICK_PERIOD_S * 0.8:
            print(f"Mid-tick calculations took {elapsed * 1000:.0f}ms", file=sys.stderr)

        # Stop loop on round end
        if is_round_end:
            game.next_tick = game.next_tick + BUILD_TIME_S
            break
        else:
            game.next_tick = game.next_tick + TICK_PERIOD_S
            continue


def _update_game_state(ctx: PlayContext, cache: PlayCache) -> bool:
    _spawn_units(ctx, cache)
    _move_units(ctx, cache)
    _sort_units(ctx, cache)

    apply_damage(ctx, cache)

    all_dead = len(ctx.game.units) == 0
    return all_dead


def _spawn_units(ctx: PlayContext, cache: PlayCache):
    tick = ctx.game.tick
    round_idx = ctx.game.round
    round_info = ctx.game.scenario.rounds[round_idx]

    for wave in round_info.waves:
        tick_end = (wave.enemies - 1) * wave.spawn_delay_ticks
        is_spawn_tick = 0 == tick % wave.spawn_delay_ticks

        if tick <= tick_end and is_spawn_tick:
            unit = Unit(
                ppath=cache.ppaths[wave.id_path],
                speed=0.25,
            )
            ctx.game.units.append(unit)
            unit.render_queue.append(RenderUnitPosition())


def _move_units(ctx: PlayContext, cache: PlayCache):
    to_delete: set[Unit] = set()

    for unit in ctx.game.units:
        unit.dist += unit.speed
        unit.render_queue.append(RenderUnitMovement())

        # Remove unit if it completed path
        if unit.dist >= unit.ppath.length - 1:
            to_delete.add(unit)

    ctx.game.units = [u for u in ctx.game.units if u not in to_delete]
    [u.delete() for u in to_delete]


def _sort_units(ctx: PlayContext, cache: PlayCache):
    # Sort units by distance traveled
    ctx.game.units.sort(key=lambda u: u.dist)
