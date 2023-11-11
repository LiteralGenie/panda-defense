from typing import ClassVar

from direct.interval.LerpInterval import LerpScaleInterval
from panda3d.core import NodePath

from game.view.procgen.square import build_rect
from utils.types import Color


class HealthBar:
    _width: ClassVar[float] = 4
    _padding: ClassVar[float] = 0.5

    color: Color
    percent: float
    pnode: NodePath

    _pnode_inner: NodePath
    _pnode_outer: NodePath

    def __init__(self, color: Color) -> None:
        self.color = color
        self.percent = 1.0

        self._init_assets()

    def _init_assets(self):
        self._pnode_outer = build_rect(
            color=(0, 0, 0, 1),
            width=self._width,
            height=1,
            centered=False,
        )

        self._pnode_inner = build_rect(
            color=self.color,
            width=self._width - self._padding,
            height=self._padding,
            centered=False,
        )
        self._pnode_inner.reparent_to(self._pnode_outer)

        # center inside outter container
        self._pnode_inner.set_pos((self._padding / 2, -self._padding / 2, 0.01))

        self.pnode = NodePath(self._pnode_outer)

    def set_percent(self, percent: float, duration: float):
        self.percent = percent

        # shrink width
        LerpScaleInterval(
            self._pnode_inner,
            duration,
            (percent + 0.001, 1, 1),
        ).start()
