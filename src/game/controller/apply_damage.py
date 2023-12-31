import math

from game.controller.controller_context import ControllerContext
from game.controller.controller_globals import CG
from game.controller.target import find_tower_targets, flatten_targets
from game.events.render_event import RenderLaserAttack, RenderTowerAttack
from game.towers.basic.basic_tower_model import BasicTowerModel
from game.towers.laser.laser_tower_model import LaserTowerModel
from game.units.unit_model import UnitStatus
from utils.misc_utils import find


def apply_damage(ctx: ControllerContext):
    units = {
        ppath.id: ctx.game.unit_mgr.select(
            id_path=ppath.id,
            status=UnitStatus.ALIVE,
            order_by="dist",
        )
        for ppath in ctx.cache.ppaths.values()
    }

    for tower in ctx.game.towers.values():
        new_guage = tower.attack_speed_guage + tower.attack_speed
        rem, attacks = math.modf(new_guage)
        tower.attack_speed_guage = rem
        if attacks < 0:
            continue

        if isinstance(tower, BasicTowerModel):
            """Basic tower attacks farthest unit"""

            targets = find_tower_targets(tower, units, ctx.cache.ranges)
            targets = flatten_targets(targets)
            targets = [tgt.unit for tgt in targets]

            for _ in range(int(attacks)):
                tgt = find(targets, lambda tgt: tgt.status == UnitStatus.ALIVE)
                if not tgt:
                    break

                tgt.health -= tower.damage
                CG.ev_mgr.add(RenderTowerAttack(tower.id, [tgt.id]))
                # print(f"Enemy {tgt.id} HP: {tgt.health}")

                if tgt.health <= 0:
                    ctx.game.unit_mgr.set_status(tgt, UnitStatus.DEAD)

                    for player in ctx.game.players.values():
                        player.gold += 1
        elif isinstance(tower, LaserTowerModel):
            """Laser tower attacks farthest unit and all units in a line behind it"""

            targets = find_tower_targets(tower, units, ctx.cache.ranges)
            targets = flatten_targets(targets)
            targets = [tgt.unit for tgt in targets]

            for _ in range(int(attacks)):
                tgt = find(targets, lambda tgt: tgt.status == UnitStatus.ALIVE)
                if not tgt:
                    break

                pt = tgt.ppath.points[int(tgt.dist)]
                axis = "x" if pt.dir[0] else "y"
                if axis == "x":
                    mn: int = tower.pos[0] - tower.range.radius  # type: ignore
                    mx: int = tower.pos[0] + tower.range.radius  # type: ignore
                    tgts = ctx.game.unit_mgr.select(
                        status=UnitStatus.ALIVE,
                        x=[
                            (">=", mn),
                            ("<=", mx),
                        ],
                        y=[
                            ("=", pt.pos[1]),
                        ],
                    )
                else:
                    mn: int = tower.pos[1] - tower.range.radius  # type: ignore
                    mx: int = tower.pos[1] + tower.range.radius  # type: ignore
                    tgts = ctx.game.unit_mgr.select(
                        status=UnitStatus.ALIVE,
                        x=[
                            ("=", pt.pos[0]),
                        ],
                        y=[
                            (">=", mn),
                            ("<=", mx),
                        ],
                    )

                for unit in tgts:
                    unit.health -= tower.damage
                    # print(f"Enemy {tgt.id} HP: {tgt.health}")

                    if unit.health <= 0:
                        ctx.game.unit_mgr.set_status(unit, UnitStatus.DEAD)

                        for player in ctx.game.players.values():
                            player.gold += 1

                CG.ev_mgr.add(
                    RenderLaserAttack(
                        tower.id,
                        [unit.id for unit in tgts],
                    )
                )
        else:
            raise Exception(f"Unknown tower type: {tower.__class__.__name__}", tower)
