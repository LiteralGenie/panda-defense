from panda3d.core import NodePath


def set_frame_size(pnode: "NodePath", wh: tuple[float, float]):
    w, h = wh
    pnode["frameSize"] = (0, w, 0, h)  # type: ignore


def set_relative_frame_size(
    pnode: "NodePath",
    wh_container: tuple[float, float],
    wh_percentage: tuple[float, float],
):
    wh = (wh_container[0] * wh_percentage[0], wh_container[1] * wh_percentage[1])
    return set_frame_size(pnode, wh)


def get_w(pnode: "NodePath") -> float:
    sz = pnode["frameSize"]  # type: ignore
    if not sz:
        print("Node has no frame size", pnode)
        return 0.111
    return sz[1] - sz[0]  # type: ignore


def get_h(pnode: "NodePath") -> float:
    sz = pnode["frameSize"]  # type: ignore
    if not sz:
        print("Node has no frame size", pnode)
        return 0.111
    return sz[3] - sz[2]  # type: ignore
