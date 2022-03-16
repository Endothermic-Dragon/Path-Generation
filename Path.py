from math import atan2, pi
from multiprocessing.sharedctypes import Value
from typing import Tuple
import pygame

fieldSize = (1646, 823) #centimeters

class Point():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

class Translate():
    def toNative(rect: pygame.Rect, coords: Tuple[float, float]):
        size = rect.size
        shift = rect.topleft
        return Point((coords[0]-shift[0])*fieldSize[0]/size[0], (size[1] - (coords[1]-shift[1]))*fieldSize[1]/size[1])

    def toPygame(rect: pygame.Rect, point: Point):
        size = rect.size
        shift = rect.topleft
        return (point.x*size[0]/fieldSize[0] + shift[0], (fieldSize[1] - point.y)*size[1]/fieldSize[1] + shift[1])

class Angle():
    def __init__(self, angle: float, inputType: str):
        if inputType.lower() in ["d", "deg", "degrees"]:
            angle = angle % 360
            self.angleDeg = angle
            self.angleRad = angle * pi / 180
        elif inputType.lower() in ["r", "rad", "radians"]:
            angle = angle % (2*pi)
            self.angleDeg = angle * 180 / pi
            self.angleRad = angle
        else:
            raise ValueError("Invalid unit for angle.")

def subtractAngles(self, other: Angle):
    return Angle(self.angleDeg - other.angleDeg, "d")

Angle.__sub__ = subtractAngles

class Path():
    def __init__(self):
        self.waypoints = []

    def append(self, point: Point):
        self.waypoints.append(point)

    def getAngle(self, point1: Point, point2: Point):
        distance = [point2.x - point1.x, point2.y - point1.y]
        angle = Angle(atan2(*distance[::-1]), "r")
        return angle.angleDeg

# Use Gradient Descent to solve all systems
# https://en.wikipedia.org/wiki/Gradient_descent#Solution_of_a_non-linear_system


# https://www.desmos.com/calculator/ehohglgaod
# 1. Implement full method
# 2. Implement adaptation that cuts off when opposite wheel is at -v
# 3. Implement adaptation that cuts off when opposive wheel is at 0
# 4. [Maybe] Implement backup using Cornu/Euler spiral?
# 5. Implement regular Hermite Spline for intersection


# Custom method details
# y value is the radius

# Equations for 3 points:
#     f(θ + θ_1 + θ_2) = r
#     tan(θ_1) * d_1 = r
#     tan(θ_2) * d_2 = r