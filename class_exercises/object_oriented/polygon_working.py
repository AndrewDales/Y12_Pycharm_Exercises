import numpy as np
import matplotlib.pyplot as plt
from math import sqrt


class Coord:
    def __init__(self, x1: float, y1: float):
        self.point = np.array((x1, y1))

    def distance(self, other) -> float:
        distance = sqrt((self.point[0] - other.point[0])**2 + (self.point[1] - other.point[1])**2)
        return distance


class Polygon:
    def __init__(self, points: list[Coord]):
        self.points = points

    def perimeter(self) -> float:
        pass

    def plot(self):
        pass


class Triangle(Polygon):
    def __init__(self, p0: Coord, p1: Coord, p2: Coord):
        pass

    def area(self) -> float:
        pass

if __name__ == "__main__":
    coord1 = Coord(1, 2)
    coord2 = Coord(4, 5)
    print(coord1.distance(coord2))