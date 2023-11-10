import time

from direct.interval.FunctionInterval import Func
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.MetaInterval import Sequence
from panda3d.core import NodePath

import g
from game.events.event_manager import GameEvent
from game.events.render_event import RenderTowerAttack
from game.towers.tower_view import TowerView
from game.view.game_view_globals import GVG
from game.view.procgen.pyramid import build_pyramid


class BasicTowerView(TowerView):
    bullet: NodePath

    def __init__(self, id: int):
        super().__init__(id)

        self._event_sub = self._subscribe_events()

    def _init_assets(self):
        super()._init_assets()

        bullet = build_pyramid()
        bullet.set_scale(0.25)
        bullet.set_p(30)

        self.bullet = bullet

    def _subscribe_events(self):
        def on_next(ev: GameEvent):
            match ev:
                case RenderTowerAttack(id_tower, id_targets):
                    if self.id != id_tower:
                        return

                    for id in id_targets:
                        unit = GVG.data.views.units[id]
                        pos = unit.interpolated_pos

                        # create bullet
                        bullet = NodePath("bullet")  # why does this throw if no name?
                        self.bullet.instance_to(bullet)
                        bullet.reparent_to(g.render)

                        # animate it
                        ivl_move = LerpPosInterval(
                            bullet,
                            duration=GVG.data.meta.tick_end - time.time(),
                            pos=pos + (0,),
                            startPos=self.model.pos + (0,),
                        )

                        # delet
                        ivl_delete = Func(lambda: bullet.hide())

                        Sequence(ivl_move, ivl_delete).start()
                case _:
                    pass

        return GVG.event_subj.subscribe(on_next=on_next)

    @classmethod
    @property
    def actor(cls):
        pnode = GVG.resource_mgr.load_actor(
            "glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf"
        )

        pnode.getChild(0).setScale(20)
        return pnode

    @classmethod
    @property
    def placeholder(cls):
        pnode = GVG.resource_mgr.load_actor(
            "glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf"
        )
        pnode.getChild(0).setScale(20)
        return pnode
