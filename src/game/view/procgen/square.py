from panda3d.core import (
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    Material,
    NodePath,
    TransparencyAttrib,
)

from utils.types import Color


def build_rect(
    color: Color | tuple[Color, Color, Color, Color],
    width: float = 1,
    height: float = 1,
    centered: bool = True,
):
    vdata = GeomVertexData("", GeomVertexFormat.getV3c4(), Geom.UH_dynamic)
    vdata.set_num_rows(4)

    vertex = GeomVertexWriter(vdata, "vertex")
    color_writer = GeomVertexWriter(vdata, "color")

    if centered:
        x_mn = -width / 2
        y_mn = height / 2
    else:
        x_mn = 0
        y_mn = 0

    x_mx = x_mn + width
    y_mx = y_mn - height

    vertex.add_data3((x_mn, y_mn, 0))
    vertex.add_data3((x_mx, y_mn, 0))
    vertex.add_data3((x_mx, y_mx, 0))
    vertex.add_data3((x_mn, y_mx, 0))

    (c1, c2, c3, c4) = (color,) * 4 if not isinstance(color[0], tuple) else color
    color_writer.add_data4(c1)
    color_writer.add_data4(c2)
    color_writer.add_data4(c3)
    color_writer.add_data4(c4)

    prim = GeomTriangles(Geom.UH_static)
    prim.addVertices(3, 1, 0)
    prim.addVertices(3, 2, 1)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode("_")
    node.addGeom(geom)

    path = NodePath(node)
    if any(c[3] < 1 for c in [c1, c2, c3, c4]):
        path.set_transparency(TransparencyAttrib.M_alpha)

    # simplepbr requires material and use_normal_maps flag
    # otherwise black blob gets rendered
    mat = Material()
    path.setMaterial(mat)

    return path
