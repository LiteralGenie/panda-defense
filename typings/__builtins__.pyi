from direct.showbase.Loader import Loader
from direct.showbase.Messenger import Messenger
from direct.showbase.ShowBase import ShowBase
from direct.task.Task import TaskManager
from panda3d.core import NodePath, VirtualFileSystem

base: ShowBase
messenger: Messenger
taskMgr: TaskManager
render: NodePath
camera: NodePath
render2d: NodePath
aspect2d: NodePath
hidden: NodePath
loader: Loader
vfs: VirtualFileSystem
