from typing import ClassVar

from direct.interval.FunctionInterval import Func
from direct.interval.Interval import Interval
from direct.interval.LerpInterval import LerpHprInterval, LerpPosInterval
from direct.interval.MetaInterval import Parallel, Sequence
from panda3d.core import NodePath
from reactivex.abc import DisposableBase

from game.events.event_manager import GameEvent
from game.events.render_event import RenderTowerAttack
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.shared_globals import SG
from game.state.game_state import StateDeleted, StateUpdated
from game.towers.basic.basic_tower_model import BasicTowerModel
from game.towers.tower_model import TowerModel
from game.towers.tower_view import TowerView
from game.view.game_view_globals import GVG
from game.view.procgen.pyramid import build_pyramid
from game.view.procgen.square import build_rect


class BasicTowerView(TowerView):
    display_name: ClassVar[str] = "Basic Tower"

    _active_bullet: NodePath | None
    _range_preview: NodePath | None
    _event_sub: DisposableBase
    _intervals: "dict[str, Interval | Sequence | Parallel]"
    _listener: BetterDirectFrame

    def __init__(self, id: int):
        super().__init__(id)

        self._active_bullet = None
        self._range_preview = None
        self._event_sub = self._subscribe_events()
        self._intervals = dict()

        self._listener = BetterDirectFrame(aspect2d)  # type: ignore
        self._listener.accept(
            "showTowerDetails",
            lambda id_tower: self._show_range()
            if id_tower == self.id
            else self._hide_range(),
        )
        self._listener.accept("hideTowerDetails", lambda: self._hide_range())

    def _init_model(self):
        return BasicTowerModel.load(self.id)

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
                        bullet.reparent_to(render)

                        # translation + rotation
                        self._intervals["bullet"] = Sequence(
                            Parallel(
                                LerpPosInterval(
                                    bullet,
                                    duration=SG.state.until_tick,
                                    pos=pos + (1,),
                                    startPos=self.model.pos + (0,),
                                ),
                                LerpHprInterval(
                                    bullet,
                                    duration=SG.state.until_tick,
                                    hpr=(90, 0, 0),
                                ),
                            ),
                            Func(lambda: bullet.hide()),
                        )
                        self._intervals["bullet"].start()
                        self._active_bullet = bullet
                case StateUpdated("TOWER", id, key, _):
                    if id != self.id:
                        return

                    if key != TowerModel.range.key:  # type: ignore
                        return

                    self._hide_range()
                    self._show_range()
                case StateDeleted("TOWER", id):
                    if id != self.id:
                        return

                    self.delete()
                case _:
                    pass

        return GVG.event_subj.subscribe(on_next=on_next)

    def _show_range(self):
        self._range_preview = NodePath("_")
        self._range_preview.reparent_to(self.pnode)

        tile = build_rect((0, 0, 0.2, 0.9))
        for pos in self.model.range.points:
            t = NodePath("")
            t.reparent_to(self._range_preview)
            tile.instance_to(t)
            t.set_pos(pos + (0.001,))

    def _hide_range(self):
        if self._range_preview:
            self._range_preview.remove_node()
            self._range_preview = None

    def _on_click(self):
        messenger.send("showTowerDetails", [self])

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

    def delete(self):
        super().delete()
        self._listener.ignore_all()
