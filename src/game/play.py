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

    first_round = game.scenario.rounds[0]
    game.map.add_unit(
        Unit(
            path=ParameterizedPath(first_round.waves[0].path),
            speed=1,
        )
    )

    game.map.add_tower(Tower())

    while game.round < len(game.scenario.rounds):
        await _play_round(ctx)


async def _play_round(ctx: PlayContext):
    game = ctx.game

    while True:
        delay = game.next_tick - time.time()
        if delay > 0 and ctx.render:
            # Render game state if we have time before next tick
            # (This should happen every tick unless potato processor causes backlogged updates)
            game.render(g.render, delay)
            delay = game.next_tick - time.time()
        if delay > 0:
            await ctx.sleep_fn(delay)

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
            game.next_tick = game.next_tick + TICK_PERIOD_S
            break
        else:
            game.next_tick = game.next_tick + TICK_PERIOD_S


def _update_game_state(ctx: PlayContext) -> bool:
    # Move units
    units = ctx.game.map.units
    for u in units:
        u.dist += u.speed

        # Remove unit if it completed path
        if u.dist >= u.path.length - 1:
            ctx.game.map.remove_unit(u)

    # Apply tower damage

    return False
