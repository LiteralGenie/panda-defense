from game.play.play import PlayContext
from game.play.play_cache import PlayCache


def apply_damage(ctx: PlayContext, cache: PlayCache):
    for tower in ctx.game.map.towers:
        units = {path_id: lane.units for path_id, lane in ctx.game.map.lanes.items()}
        targets = find_tower_targets(tower, units, cache.ranges)
