from direct.actor.Actor import Actor
from direct.interval.FunctionInterval import Func, Wait
from direct.interval.Interval import Interval
from direct.interval.MetaInterval import Sequence
from panda3d.core import NodePath
from reactivex import operators as ops
from reactivex.abc import DisposableBase

from game.events.event_manager import GameEvent
from game.events.render_event import RenderTowerAttack
from game.shared_globals import SG
from game.state.game_state import StateUpdated
from game.units.health_bar.health_bar import HealthBar
from game.units.unit_model import UnitModel, UnitStatus
from game.view.game_view_globals import GVG


class UnitView:
    id: int
    model: UnitModel
    pnode: Actor | None

    _event_sub: DisposableBase
    _health_bar: HealthBar
    _intervals: "dict[str, Interval]"

    def __init__(self, id: int):
        self.id = id
        self.model = self._init_model()
        self.pnode = None

        self._intervals = dict()
        self._event_sub = self._subscribe_events()

        self.preload_actor()

    def _init_model(self):
        data = SG.state.data["UNIT"][self.id]["data"]
        ppath = GVG.data.ppaths[data["id_path"]]
        return UnitModel.load(self.id, ppath=ppath)

    def _init_assets(self):
        self.pnode = NodePath("unit_view")  # type: ignore
        self.__class__.actor.instance_to(self.pnode)
        self.pnode.reparent_to(render)

        # set position
        dist = int(self.model.dist)
        pos = self.model.ppath.points[dist].pos
        self.pnode.set_pos(pos + (0,))

        # add health bar
        self._health_bar = HealthBar((0.6, 0, 0, 1))
        self._health_bar.pnode.reparent_to(self.pnode)
        self._health_bar.pnode.set_scale(0.125)
        self._health_bar.pnode.set_pos((-0.25, 0, 0.25))

    def _subscribe_events(self):
        def filter(ev: GameEvent):
            match ev:
                case RenderTowerAttack():
                    return self.id in ev.id_targets
                case StateUpdated():
                    return ev.id == self.id
                case _:
                    return False

        def on_next(ev: GameEvent):
            match ev:
                case StateUpdated(_, _, key, value):
                    match key:
                        case UnitModel.dist.key:  # type: ignore
                            self._render_pos()
                        case UnitModel.status.key:  # type: ignore
                            if value == UnitStatus.ALIVE:
                                self._init_assets()
                            elif value == UnitStatus.DEAD:
                                Sequence(
                                    Wait(SG.state.until_tick),
                                    Func(lambda: self.delete()),
                                ).start()
                        case UnitModel.health.key:  # type: ignore
                            percent = max(value / self.model.max_health, 0)
                            self._health_bar.set_percent(percent, SG.state.until_tick)
                        case _:
                            pass
                case _:
                    pass

        return GVG.event_subj.pipe(
            ops.filter(filter),
        ).subscribe(on_next=on_next)

    def _render_pos(self):
        if ivl := self._intervals.get("pos"):
            ivl.pause()

        self._intervals["pos"] = self.pnode.posInterval(  # type: ignore
            SG.state.until_tick,
            self.model.interpolated_pos + (0,),
        )
        self._intervals["pos"].start()  # type: ignore

    def delete(self):
        self._event_sub.dispose()

        if self.pnode:
            self.pnode.removeNode()

    @classmethod
    @property
    def actor(cls):
        pnode = GVG.resource_mgr.load_actor(
            "glTF-Sample-Models/2.0/BoomBox/glTF/BoomBox.gltf"
        )

        pnode.getChild(0).setScale(20)
        return pnode

    @classmethod
    def preload_actor(cls):
        GVG.resource_mgr.preload_actor(
            "glTF-Sample-Models/2.0/BoomBox/glTF/BoomBox.gltf"
        )
