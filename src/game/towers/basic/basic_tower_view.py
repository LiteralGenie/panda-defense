from direct.interval.FunctionInterval import Func
from direct.interval.Interval import Interval
from direct.interval.LerpInterval import LerpPosInterval
from direct.interval.MetaInterval import Sequence
from panda3d.core import NodePath
from reactivex.abc import DisposableBase

import g
from game.events.event_manager import GameEvent
from game.events.render_event import RenderTowerAttack
from game.shared_globals import SG
from game.towers.tower_view import TowerView
from game.view.game_view_globals import GVG
from game.view.procgen.pyramid import build_pyramid


class BasicTowerView(TowerView):
    _active_bullet: NodePath | None
    _event_sub: DisposableBase
    _intervals: "dict[str, Interval | Sequence]"

    def __init__(self, id: int):
        super().__init__(id)

        self._active_bullet = None
        self._event_sub = self._subscribe_events()
        self._intervals = dict()

    def _init_assets(self):
        super()._init_assets()

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
                        bullet = NodePath("bullet")
                        self.bullet.instance_to(bullet)
                        bullet.reparent_to(g.render)

                        # animate it
                        ivl_move = LerpPosInterval(
                            bullet,
                            duration=SG.state.until_tick,
                            pos=pos + (0,),
                            startPos=self.model.pos + (0,),
                        )

                        # delete
                        ivl_delete = Func(lambda: bullet.hide())

                        self._intervals["bullet_sequence"] = Sequence(
                            ivl_move,
                            ivl_delete,
                        )
                        self._intervals["bullet_sequence"].start()
                        self._active_bullet = bullet
                case _:
                    pass

        return GVG.event_subj.subscribe(on_next=on_next)

    def _on_click(self):
        g.messenger.send("showTowerDetails", [self])

    @classmethod
    @property
    def actor(cls):
        pnode = GVG.resource_mgr.load_actor(
            "glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf"
        )

        pnode.getChild(0).setScale(20)
        return pnode

    @classmethod
    def preload_actor(cls):
        GVG.resource_mgr.preload_actor(
            "glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf"
        )

    @classmethod
    @property
    def placeholder(cls):
        pnode = GVG.resource_mgr.load_actor(
            "glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf"
        )
        pnode.getChild(0).setScale(20)
        return pnode

    @classmethod
    def preload_placeholder(cls):
        GVG.resource_mgr.preload_actor(
            "glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf"
        )

    @classmethod
    @property
    def bullet(cls):
        def factory():
            bullet = build_pyramid()
            bullet.set_scale(0.25)
            bullet.set_p(30)
            return bullet

        return GVG.resource_mgr.load_or_register("basic_bullet", factory)
