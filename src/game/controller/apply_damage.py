import math

from game.controller.controller_context import ControllerContext
from game.controller.target import find_tower_targets, flatten_targets
from game.towers.basic.basic_tower_model import BasicTowerModel
from game.units.unit_model import UnitStatus
from utils.misc_utils import find


def apply_damage(ctx: ControllerContext):
    units = {
        ppath.id: ctx.game.unit_mgr.select(
            id_path=ppath.id, status=UnitStatus.ALIVE, order_by="dist"
        )
        for ppath in ctx.cache.ppaths.values()
    }

    for tower in ctx.game.towers:
        if isinstance(tower, BasicTowerModel):
            tower.attack_speed_guage += tower.attack_speed
            rem, attacks = math.modf(tower.attack_speed_guage)
            tower.attack_speed_guage = rem

            if attacks > 0:
                targets = find_tower_targets(tower, units, ctx.cache.ranges)
                targets = flatten_targets(targets)
                targets = [tgt.unit for tgt in targets]

                for _ in range(int(attacks)):
                    tgt = find(targets, lambda tgt: tgt.status == UnitStatus.ALIVE)
                    if not tgt:
                        break

                    tgt.take_damage(tower.damage, tower)
                    # print(f"Enemy {tgt.id} HP: {tgt.health}")

                    if tgt.health <= 0:
                        ctx.game.unit_mgr.set_status(tgt, UnitStatus.DEAD)
        else:
            raise Exception(f"Unknown tower type: {tower.__class__.__name__}", tower)
