from DegMath import atan2
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

class Path():
    def __init__(self):
        self.waypoints = []
        self.waypointsLength = 0

    def append(self, point: Point):
        self.waypoints.append(point)
        self.waypointsLength += 1

        if self.waypointsLength > 1:
            self.waypoints[-2].angle = self.getAngle(*self.waypoints[-2:])

        if self.waypointsLength > 2:
            rotationAngle = self.waypoints[-2].angle - self.waypoints[-3].angle

            # Positive means clockwise rotation of robot
            # Negative means counterclockwise rotation of robot
            if rotationAngle > 180:
                rotationAngle -= 360
            elif rotationAngle < -180:
                rotationAngle += 360

            rotationAngle = rotationAngle - 360 if rotationAngle > 180 else rotationAngle
            self.waypoints[-2].rotationAngle = rotationAngle

    def getAngle(self, point1: Point, point2: Point):
        distance = [point2.y - point1.y, point2.x - point1.x]
        return atan2(*distance)



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