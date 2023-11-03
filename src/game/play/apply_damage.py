import math

from game.play.play_cache import PlayCache
from game.play.play_context import PlayContext
from game.play.target import find_tower_targets, flatten_targets
from game.tower.basic import BasicTower
from game.unit.render_unit_events import RenderUnitDeath
from game.unit.unit import UnitStatus
from utils.misc_utils import find


def apply_damage(ctx: PlayContext, cache: PlayCache):
    units = {
        ppath.id: ctx.game.unit_mgr.select(id_path=ppath.id)
        for ppath in cache.ppaths.values()
    }

    for tower in ctx.game.towers:
        if isinstance(tower, BasicTower):
            tower.attack_speed_guage += tower.attack_speed
            rem, attacks = math.modf(tower.attack_speed_guage)
            tower.attack_speed_guage = rem

            if attacks > 0:
                targets = find_tower_targets(tower, units, cache.ranges)
                targets = flatten_targets(targets)
                targets = [tgt.unit for tgt in targets]

                for _ in range(int(attacks)):
                    tgt = find(targets, lambda tgt: tgt.status == UnitStatus.ALIVE)
                    if not tgt:
                        break

                    tgt.health -= tower.damage
                    print("Target HP:", tgt.health)
                    # render: damage

                    if tgt.health <= 0:
                        ctx.game.unit_mgr.set_status(tgt, UnitStatus.DEAD)
                        tgt.render_queue.append(RenderUnitDeath())
        else:
            raise Exception(f"Unknown tower type: {tower.__class__.__name__}", tower)
