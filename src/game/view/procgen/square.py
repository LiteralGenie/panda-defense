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


def build_rect(
    color: tuple[float, float, float, float],
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

    color_writer.add_data4(color)
    color_writer.add_data4(color)
    color_writer.add_data4(color)
    color_writer.add_data4(color)

    prim = GeomTriangles(Geom.UH_static)
    prim.addVertices(3, 1, 0)
    prim.addVertices(3, 2, 1)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode("_")
    node.addGeom(geom)

    path = NodePath(node)
    if color[3] < 1:
        path.set_transparency(TransparencyAttrib.M_alpha)

    # simplepbr requires material and use_normal_maps flag
    # otherwise black blob gets rendered
    mat = Material()
    path.setMaterial(mat)

    return path
