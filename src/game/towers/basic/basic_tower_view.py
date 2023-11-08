from game.towers.tower_view import TowerView
from game.view.game_view_globals import GVG


class BasicTowerView(TowerView):
    @classmethod
    @property
    def actor(cls):
        pnode = GVG.resource_mgr.load_actor(
            "glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf"
        )

        pnode.getChild(0).setScale(20)
        return pnode

    @classmethod
    @property
    def placeholder(cls):
        pnode = GVG.resource_mgr.load_actor(
            "glTF-Sample-Models/2.0/Avocado/glTF/Avocado.gltf"
        )
        pnode.getChild(0).setScale(20)
        return pnode
