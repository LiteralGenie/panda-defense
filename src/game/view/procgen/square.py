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


def build_square(color: tuple[float, float, float, float]):
    vdata = GeomVertexData("", GeomVertexFormat.getV3c4(), Geom.UH_dynamic)
    vdata.set_num_rows(4)

    vertex = GeomVertexWriter(vdata, "vertex")
    color_writer = GeomVertexWriter(vdata, "color")

    # fmt: off
    vertex.add_data3((-0.5,  0.5, 0))
    vertex.add_data3(( 0.5,  0.5, 0))
    vertex.add_data3(( 0.5, -0.5, 0))
    vertex.add_data3((-0.5, -0.5, 0))

    color_writer.add_data4(color)
    color_writer.add_data4(color)
    color_writer.add_data4(color)
    color_writer.add_data4(color)
    # fmt: on

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
