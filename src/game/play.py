import sys
import time
from dataclasses import dataclass
from typing import Callable

import g
from game.game import Game
from game.parameterized_path import ParameterizedPath
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
    sleep_fn: Callable


async def play_game(ctx: PlayContext):
    game = ctx.game

    game.next_tick = ctx.first_tick

    game.map.add_tower(Tower())

    while game.round < len(game.scenario.rounds):
        await _play_round(ctx)


async def _play_round(ctx: PlayContext):
    game = ctx.game
    game.round += 1

    while True:
        delay = game.next_tick - time.time()
        if delay > 0 and ctx.render:
            # Render game state if we have time before next tick
            # (This should happen every tick unless potato processor causes backlogged updates)
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
        is_round_end = _update_game_state(ctx)

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


def _update_game_state(ctx: PlayContext) -> bool:
    _move_units(ctx)
    _spawn_units(ctx)
    # _apply_damage(ctx)
    return False


def _spawn_units(ctx: PlayContext):
    tick = ctx.game.tick
    round_idx = ctx.game.round
    round_info = ctx.game.scenario.rounds[round_idx]

    for wave in round_info.waves:
        tick_end = (wave.enemies - 1) * wave.spawn_delay_ticks
        is_spawn_tick = 0 == tick % wave.spawn_delay_ticks

        if tick < tick_end and is_spawn_tick:
            unit = Unit(
                path=ParameterizedPath(wave.path),
                speed=0.25,
            )
            ctx.game.map.add_unit(unit)


def _move_units(ctx: PlayContext):
    # Move units
    units = ctx.game.map.units
    for u in units:
        u.dist += u.speed

        # Remove unit if it completed path
        if u.dist >= u.path.length - 1:
            ctx.game.map.remove_unit(u)
