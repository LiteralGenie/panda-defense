import sys
import time
from dataclasses import dataclass
from typing import Awaitable, Callable

import g
from game.cache.range_cache import RangeCache
from game.game import Game
from game.target import find_tower_targets
from game.tower import Tower
from game.unit import Unit

TICK_FREQ_S = 4
TICK_PERIOD_S = 1 / TICK_FREQ_S
BUILD_TIME_S = 30


@dataclass
class PlayContext:
    game: Game

    first_tick: float
    render: bool
    sleep_fn: Callable[[float], Awaitable[None]]


@dataclass
class _Cache:
    ranges: RangeCache


async def play_game(ctx: PlayContext):
    game = ctx.game

    game.next_tick = ctx.first_tick

    cache = _Cache(
        ranges=RangeCache([lane.ppath for lane in game.map.lanes.values()]),
    )

    game.map.add_tower(Tower((1, 1)))

    while game.round < len(game.scenario.rounds):
        await _play_round(ctx, cache)


async def _play_round(ctx: PlayContext, cache: _Cache):
    game = ctx.game
    game.round += 1

    while True:
        delay = game.next_tick - time.time()
        if delay > 0 and ctx.render:
            # Render game state if we have time before next tick
            # (This should happen every tick unless potato processor causes
            #  backlogged updates that skip this rendering step)
            game.render(g.render, delay)
            delay = game.next_tick - time.time()
        if delay > 0:
            await ctx.sleep_fn(delay)

        game.tick += 1
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


def _update_game_state(ctx: PlayContext, cache: _Cache) -> bool:
    _spawn_units(ctx, cache)
    _move_units(ctx, cache)
    _sort_units(ctx, cache)

    _apply_damage(ctx, cache)

    all_dead = all(len(lane.units) == 0 for lane in ctx.game.map.lanes.values())
    return all_dead


def _spawn_units(ctx: PlayContext, cache: _Cache):
    tick = ctx.game.tick
    round_idx = ctx.game.round
    round_info = ctx.game.scenario.rounds[round_idx]

    for wave in round_info.waves:
        tick_end = (wave.enemies - 1) * wave.spawn_delay_ticks
        is_spawn_tick = 0 == tick % wave.spawn_delay_ticks

        if tick < tick_end and is_spawn_tick:
            unit = Unit(
                speed=0.25,
            )
            lane = ctx.game.map.lanes[wave.id_path]
            lane.add_unit(unit)


def _move_units(ctx: PlayContext, cache: _Cache):
    for lane in ctx.game.map.lanes.values():
        for unit in lane.units:
            unit.dist += unit.speed

            # Remove unit if it completed path
            if unit.dist >= lane.ppath.length - 1:
                lane.remove_unit(unit)


def _sort_units(ctx: PlayContext, cache: _Cache):
    # Sort units by distance traveled
    for lane in ctx.game.map.lanes.values():
        lane.units.sort(key=lambda u: u.dist)


def _apply_damage(ctx: PlayContext, cache: _Cache):
    for tower in ctx.game.map.towers:
        units = {path_id: lane.units for path_id, lane in ctx.game.map.lanes.items()}
        targets = find_tower_targets(tower, units, cache.ranges)
