from math import atan2, pi, sqrt
from typing import ClassVar

from direct.interval.FunctionInterval import Func
from direct.interval.Interval import Interval
from direct.interval.LerpInterval import LerpFunc
from direct.interval.MetaInterval import Parallel, Sequence
from panda3d.core import NodePath
from reactivex.abc import DisposableBase

from game.events.event_manager import GameEvent
from game.events.render_event import RenderLaserAttack
from game.game_gui.better_direct_frame import BetterDirectFrame
from game.shared_globals import SG
from game.state.game_state import StateDeleted, StateUpdated
from game.towers.basic.basic_tower_model import BasicTowerModel
from game.towers.tower_model import TowerModel
from game.towers.tower_view import TowerView
from game.view.game_view_globals import GVG
from game.view.procgen.square import build_rect


class LaserTowerView(TowerView):
    display_name: ClassVar[str] = "Laser Tower"

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
                case RenderLaserAttack(id_tower, id_targets):
                    if self.id != id_tower:
                        return

                    units = [GVG.data.views.units[id] for id in id_targets]
                    x_min = min(unit.model.interpolated_pos[0] for unit in units)
                    x_max = max(unit.model.interpolated_pos[0] for unit in units)
                    width = x_max - x_min

                    y_min = min(unit.model.interpolated_pos[1] for unit in units)
                    y_max = max(unit.model.interpolated_pos[1] for unit in units)
                    height = y_max - y_min

                    # create bullet
                    bullet = NodePath("bullet")
                    self.bullet.instance_to(bullet)
                    bullet.reparent_to(render)
                    bullet.set_pos(self.model.pos + (0,))

                    def cb(t: float):
                        x = x_min + t * width
                        y = y_min + t * height

                        x_rel = x - self.model.pos[0]
                        y_rel = y - self.model.pos[1]

                        length = sqrt((x_rel**2) + (y_rel**2))
                        bullet.set_sx(length)

                        angle = atan2(y_rel, x_rel) * 180 / pi
                        bullet.set_h(angle)

                    # translation + rotation
                    self._intervals["bullet"] = Sequence(
                        LerpFunc(
                            cb,
                            duration=SG.state.until_tick,
                            fromData=0,
                            toData=1,
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
            "glTF-Sample-Models/2.0/AntiqueCamera/glTF/AntiqueCamera.gltf"
        )

        pnode.getChild(0).setScale(0.25)
        return pnode

    @classmethod
    def preload_actor(cls):
        GVG.resource_mgr.preload_actor(
            "glTF-Sample-Models/2.0/AntiqueCamera/glTF/AntiqueCamera.gltf"
        )

    @classmethod
    @property
    def placeholder(cls):
        pnode = GVG.resource_mgr.load_actor(
            "glTF-Sample-Models/2.0/AntiqueCamera/glTF/AntiqueCamera.gltf"
        )
        pnode.getChild(0).setScale(0.25)
        return pnode

    @classmethod
    def preload_placeholder(cls):
        GVG.resource_mgr.preload_actor(
            "glTF-Sample-Models/2.0/AntiqueCamera/glTF/AntiqueCamera.gltf"
        )

    @classmethod
    @property
    def bullet(cls):
        def factory():
            bullet = build_rect(
                color=(
                    (0.65, 0.5, 0.2, 1),
                    (0.5, 0, 0, 1),
                    (0.5, 0, 0, 1),
                    (0.65, 0.5, 0.2, 1),
                ),
                height=1,
                width=1,
                centered=False,
            )
            bullet.set_pos((0, 0, 1))
            bullet.set_sy(0.25)
            return bullet

        return GVG.resource_mgr.load_or_register("laser_bullet", factory)

    def delete(self):
        super().delete()
        self._listener.ignore_all()
