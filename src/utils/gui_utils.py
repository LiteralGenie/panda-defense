from direct.gui.DirectGuiBase import DirectGuiWidget
from panda3d.core import Plane, Point3

import g
from utils.types import Point2f


def set_frame_size(widget: DirectGuiWidget, wh: tuple[float, float]):
    w, h = wh
    widget["frameSize"] = (0, w, 0, h)  # type: ignore


def set_relative_frame_size(
    widget: DirectGuiWidget,
    wh_container: tuple[float, float],
    wh_percentage: tuple[float, float],
):
    wh = (wh_container[0] * wh_percentage[0], wh_container[1] * wh_percentage[1])
    return set_frame_size(widget, wh)


def get_w(widget: DirectGuiWidget) -> float:
    sz = widget["frameSize"]  # type: ignore
    if not sz:
        raise Exception("Widget has no frame size", widget)
    return sz[1] - sz[0]  # type: ignore


def get_h(widget: DirectGuiWidget) -> float:
    sz = widget["frameSize"]  # type: ignore
    if not sz:
        raise Exception("Widget has no frame size", widget)
    return sz[3] - sz[2]  # type: ignore


def get_mouse_pos() -> Point2f | None:
    node = g.base.mouseWatcherNode
    if node.hasMouse():
        return (node.getMouseX(), node.getMouseY())


_ground_plane = Plane((0, 0, 1), (0, 0, 0))


def mpos_to_real_pos(mpos: Point2f) -> Point2f:
    # https://discourse.panda3d.org/t/super-fast-mouse-ray-collisions-with-ground-plane/5022

    render = g.render
    base = g.base

    pos = Point3()
    near_point = Point3()
    far_point = Point3()

    # init near_point, far_point
    base.camLens.extrude(mpos, near_point, far_point)

    # init pos
    if not _ground_plane.intersectsLine(
        pos,
        render.getRelativePoint(base.camera, near_point),
        render.getRelativePoint(base.camera, far_point),
    ):
        raise Exception("No intersection")

    xz = pos.get_xz()
    return (xz[0], xz[1])
