from game.scenario import Path, Point


class ParameterizedPath:
    points: list[Point]
    length: int

    def __init__(self, path: Path):
        pos = path.start
        self.points = [pos]

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
                self.points.append(pos)

        self.length = len(self.points)
