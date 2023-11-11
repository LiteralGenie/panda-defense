from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from direct.interval.Interval import Interval
    from direct.interval.MetaInterval import Sequence

Point2 = tuple[int, int]
Point2f = tuple[float, float]
Color = tuple[float, float, float, float]

IntervalDict: TypeAlias = "dict[str, Interval | Sequence]"
