import asyncio
import sys
import time
from multiprocessing.connection import Connection

from game.controller.apply_damage import apply_damage
from game.controller.controller_cache import ControllerCache
from game.controller.controller_context import ControllerContext
from game.controller.controller_globals import CG
from game.controller.range_cache import RangeCache
from game.events.event_manager import EventManager
from game.events.game_actions import (
    BuyTowerAction,
    GameActions,
    SellTowerAction,
    UpgradeTowerAction,
)
from game.game_model import GameModel
from game.parameterized_path import ParameterizedPath
from game.player.player_model import PlayerModel
from game.scenario import Scenario
from game.shared_globals import SG
from game.state.game_state import GameState
from game.towers.basic.basic_tower_model import BasicTowerModel
from game.towers.tower_range.pyramidal_range import PyramidalRange
from game.towers.tower_range.square_range import SquareRange
from game.units.unit_manager import UnitManager
from game.units.unit_model import UnitModel, UnitStatus

TICK_FREQ_S = 4
TICK_PERIOD_S = 1 / TICK_FREQ_S
BUILD_TIME_S = 5


async def play_game(
    first_tick: float,
    scenario: Scenario,
    id_player: int,
    render_pipe: Connection,
):
    # init globals
    # (things that most models need access to and would be painful to supply via contructor)
    CG.ev_mgr = EventManager(render_pipe)
    SG.state = GameState(on_event=CG.ev_mgr.add)

    # init game model
    players = [PlayerModel.create(id=id_player, gold=500)]
    game = GameModel.create(scenario, first_tick, players[0].id, players)

    # init cache
    ppaths = {id: ParameterizedPath(p) for id, p in scenario["paths"].items()}
    cache = ControllerCache(
        ppaths=ppaths,
        ranges=RangeCache(list(ppaths.values())),
        start_ticks={0: 0},
    )

    # init context
    # (god object passed to all controller functions)
    ctx = ControllerContext(
        game=game,
        cache=cache,
        render_pipe=render_pipe,
    )

    # start game
    for i in range(len(game.scenario["rounds"])):
        print(f"Round {i}")
        game.round_idx = i
        cache.start_ticks[game.round_idx] = game.tick + 1
        game.next_tick += BUILD_TIME_S

        # Update view
        CG.ev_mgr.flush(game)

        # Wait for build phase
        while (delay := game.next_tick - time.time()) > 0:
            # Apply any actions that occur while waiting
            while ctx.render_pipe.poll(timeout=delay):
                action = ctx.render_pipe.recv()
                _apply_action(action, game)

                CG.ev_mgr.flush(game)
                break

        await _play_round(ctx)

    CG.ev_mgr.flush(game)

    print(f"Game end")


async def _play_round(ctx: ControllerContext):
    game = ctx.game

    game.unit_mgr = UnitManager()
    _init_units_for_round(ctx)

    while True:
        # Update view
        CG.ev_mgr.flush(game)

        # Wait for tick start
        delay = game.next_tick - time.time()
        if delay > 0:
            await asyncio.sleep(delay)

        game.tick += 1
        game.next_tick += TICK_PERIOD_S
        # print("Tick", game.tick)
        start = time.time()

        # Validate and apply actions
        while ctx.render_pipe.poll():
            action = ctx.render_pipe.recv()
            _apply_action(action, game)

        # Update game state
        is_round_end = _update_game_state(ctx)

        # Calculations should never (consistently) run over than tick period
        # (because assuming the tick times are constant and reproducible
        #  simplifies a lot of the client-server and multiplayer syncing)
        tick_end = time.time()
        elapsed = tick_end - start
        if elapsed > TICK_PERIOD_S * 0.8:
            print(f"Mid-tick calculations took {elapsed * 1000:.0f}ms", file=sys.stderr)

        # Stop loop on round end
        if is_round_end:
            break


def _init_units_for_round(ctx: ControllerContext):
    for wave in ctx.game.current_round["waves"]:
        for _ in range(wave["enemies"]):
            unit = UnitModel.create(
                id_wave=wave["id"],
                ppath=ctx.cache.ppaths[wave["id_path"]],
                speed=0.25,
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
            ctx.game.health -= 1


def _apply_action(action: GameActions, game: GameModel):
    match action:
        case BuyTowerAction(TowerCls, id_player, kwargs):
            player = game.players[id_player]
            if player.gold >= TowerCls.cost:
                player.gold -= TowerCls.cost
                tower = TowerCls.create(**kwargs)
                game.add_tower(tower)
            else:
                print("Not enough gold to buy tower")
        case UpgradeTowerAction(id_player, id_tower, trait):
            player = game.players[id_player]

            tower = game.towers[id_tower]
            match trait:
                case "damage":
                    cost = 7
                    if player.gold < cost:
                        print("Not enough gold to upgrade tower")
                        return

                    tower.damage = int(1.1 * tower.damage)
                case "range":
                    cost = 15
                    if player.gold < cost:
                        print("Not enough gold to upgrade tower")
                        return

                    if isinstance(tower, BasicTowerModel):
                        tower.range = PyramidalRange(tower.range.radius + 1)
                    else:
                        tower.range = SquareRange(tower.range.radius + 1)
                case "speed":
                    cost = 7
                    if player.gold < cost:
                        print("Not enough gold to upgrade tower")
                        return

                    tower.attack_speed *= 1.1

            player.gold -= cost
        case SellTowerAction(id_player, id_tower):
            player = game.players[id_player]
            tower = game.towers[id_tower]

            player.gold += tower.cost

            tower.delete()
            del game.towers[id_tower]
