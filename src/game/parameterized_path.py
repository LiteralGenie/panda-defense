from dataclasses import dataclass

from game.scenario import Path, Point


@dataclass
class PointWithDirection:
    pos: Point
    dir: Point


class ParameterizedPath:
    points: list[PointWithDirection]
    length: int

    def __init__(self, path: Path):
        pos = path.start
        dir = (0, 0)
        self.points = [PointWithDirection(pos=pos, dir=dir)]

        for segment in path.segments:
            step_x = 0
            if segment.axis == "x":
                step_x = 1
            if segment.axis == "-x":
                step_x = -1

            step_y = 0
            if segment.axis == "y":
                step_y = 1
            if segment.axis == "-y":
                step_y = -1

            for _ in range(1, segment.dist):
                pos = (pos[0] + step_x, pos[1] + step_y)
                dir = (step_x, step_y)
                self.points.append(PointWithDirection(pos=pos, dir=dir))

        self.length = len(self.points)
