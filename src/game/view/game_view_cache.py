from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.parameterized_path import ParameterizedPath
    from game.view.game_view_globals import GameViewMetaInfo
    from game.view.view_manager import GameViewManager

_PathId = int


@dataclass
class GameViewData:
    meta: "GameViewMetaInfo"
    ppaths: "dict[_PathId, ParameterizedPath]"
    views: "GameViewManager"
