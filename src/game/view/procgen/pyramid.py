from panda3d.core import (
    Geom,
    GeomNode,
    GeomTriangles,
    GeomVertexData,
    GeomVertexFormat,
    GeomVertexWriter,
    Material,
    NodePath,
)


def build_pyramid():
    vdata = GeomVertexData("", GeomVertexFormat.getV3c4(), Geom.UH_dynamic)
    vdata.set_num_rows(6)

    vertex = GeomVertexWriter(vdata, "vertex")
    color = GeomVertexWriter(vdata, "color")

    # square base centered at origin
    # 0 --- 1
    # |  4  |
    # 3 --- 2

    # fmt: off
    vertex.add_data3((-0.5,  0.5, 0))
    vertex.add_data3(( 0.5,  0.5, 0))
    vertex.add_data3(( 0.5, -0.5, 0))
    vertex.add_data3((-0.5, -0.5, 0))
    vertex.add_data3(( 0.0,  0.0, 1))

    color.add_data4(255, 000, 000, 255)
    color.add_data4(000, 255, 000, 255)
    color.add_data4(000, 000, 255, 255)
    color.add_data4(000, 000, 255, 255)
    color.add_data4(255, 255, 000, 255)
    # fmt: on

    prim = GeomTriangles(Geom.UH_static)

    # base
    prim.addVertices(3, 1, 0)
    prim.addVertices(3, 2, 1)

    # left / back / right / front
    prim.addVertices(3, 4, 0)
    prim.addVertices(0, 4, 1)
    prim.addVertices(1, 4, 2)
    prim.addVertices(2, 4, 3)

    geom = Geom(vdata)
    geom.addPrimitive(prim)

    node = GeomNode("_")
    node.addGeom(geom)

    path = NodePath(node)

    # simplepbr requires material and use_normal_maps flag
    # otherwise black blob gets rendered
    mat = Material()
    path.setMaterial(mat)

    return path
