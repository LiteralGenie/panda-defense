import math

from game.play.play_cache import PlayCache
from game.play.play_context import PlayContext
from game.play.target import find_tower_targets, flatten_targets
from game.tower.basic import BasicTower
from game.unit.unit import Unit


def apply_damage(ctx: PlayContext, cache: PlayCache):
    # todo: why not store units pre-grouped by lane?
    #       so we can skip this grouping step every tick
    units: dict[int, list[Unit]] = {p.id: [] for p in ctx.game.scenario.paths.values()}
    for u in ctx.game.units:
        pid = u.ppath.id
        units[pid].append(u)

    to_delete: set[Unit] = set()
    for tower in ctx.game.towers:
        if isinstance(tower, BasicTower):
            tower.attack_speed_guage += tower.attack_speed
            rem, attacks = math.modf(tower.attack_speed_guage)
            tower.attack_speed_guage = rem

            if attacks > 0:
                targets = find_tower_targets(tower, units, cache.ranges)
                targets = flatten_targets(targets)

                if targets:
                    print(f"Attacking {len(targets)} targets {attacks:.0f} times")

                tgt_idx = 0
                for _ in range(int(attacks)):
                    if tgt_idx >= len(targets):
                        break

                    tgt = targets[tgt_idx]
                    tgt.unit.health -= tower.damage
                    print("Target HP:", tgt.unit.health)
                    # render: damage

                    if tgt.unit.health <= 0:
                        to_delete.add(tgt.unit)
                        tgt_idx += 1
        else:
            raise Exception(f"Unknown tower type: {tower.__class__.__name__}", tower)

    ctx.game.units = [u for u in ctx.game.units if u not in to_delete]
    [u.delete() for u in to_delete]
