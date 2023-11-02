import math

from game.play.play_cache import PlayCache
from game.play.play_context import PlayContext
from game.play.target import consolidate_targets, find_tower_targets
from game.towers.basic import BasicTower


def apply_damage(ctx: PlayContext, cache: PlayCache):
    lanes = ctx.game.map.lanes
    units = {path_id: lane.units for path_id, lane in ctx.game.map.lanes.items()}

    for tower in ctx.game.map.towers:
        if isinstance(tower, BasicTower):
            tower.attack_speed_guage += tower.attack_speed
            rem, attacks = math.modf(tower.attack_speed_guage)
            tower.attack_speed_guage = rem

            if attacks > 0:
                targets = find_tower_targets(tower, units, cache.ranges)
                targets = consolidate_targets(targets)

                if targets:
                    print(f"Attacking {len(targets)} targets {attacks:.0f} times")

                tgt_idx = 0
                for _ in range(int(attacks)):
                    if tgt_idx >= len(targets):
                        break

                    tgt = targets[tgt_idx]
                    tgt.unit.health -= tower.damage
                    print("Target HP:", tgt.unit.health)

                    if tgt.unit.health <= 0:
                        lanes[tgt.path.id].remove_unit(tgt.unit)
                        tgt_idx += 1
        else:
            raise Exception(f"Unknown tower type: {tower.__class__.__name__}", tower)
