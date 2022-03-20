from DegMath import atan2
import pygame
from DriveCharacterization import DriveCharacterization
from GradientDescent import GradientDescent

fieldSize = (1646, 823) #centimeters

# Store point with x and y coordinates as an object
class Point():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# Translate between field coordinate and pygame display coordinates
class Translate():
    def toNative(rect: pygame.Rect, coords: tuple[float, float]):
        size = rect.size
        shift = rect.topleft
        return Point((coords[0]-shift[0])*fieldSize[0]/size[0], (size[1] - (coords[1]-shift[1]))*fieldSize[1]/size[1])

    def toPygame(rect: pygame.Rect, point: Point):
        size = rect.size
        shift = rect.topleft
        return (point.x*size[0]/fieldSize[0] + shift[0], (fieldSize[1] - point.y)*size[1]/fieldSize[1] + shift[1])

# Setup with points and precalculated properties in a list before performing gradient descent
class Path():
    # Initialize with an empty list of points
    def __init__(self, robotCharacteristics: DriveCharacterization):
        self.robotCharacteristics = robotCharacteristics
        self.waypoints = []
        # Easily fetch length of array (not sure how efficient native fetching is)
        self.waypointsLength = 0
        self.lengths = []
        self.angles = []
        self.rotationAngles = []

    # Append point into list
    def append(self, point: Point):
        self.waypoints.append(point)
        self.waypointsLength += 1

        # Set angle of point in 2D space (standard position)
        if self.waypointsLength > 1:
            length, angle = self.getAngleAndLength(*self.waypoints[-2:])
            self.angles.append(angle)
            self.lengths.append(length / 100)

        # Set turn angle for robot at point
        if self.waypointsLength > 2:
            self.rotationAngles.append(self.angles[-1] - self.angles[-2])

    # Return angle between two points, with respect to the first point, in standard position
    def getAngleAndLength(self, point1: Point, point2: Point):
        distance = [point2.y - point1.y, point2.x - point1.x]
        return (atan2(*distance), (distance[0]**2 + distance[1]**2)**0.5)
    
    def drawPath(self):
        solver = GradientDescent(self.robotCharacteristics, self.lengths, self.rotationAngles)
        for i in range(1000):
            solver.step()
        print(solver.step())



# Use Gradient Descent to solve all systems
# https://en.wikipedia.org/wiki/Gradient_descent#Solution_of_a_non-linear_system


# https://www.desmos.com/calculator/ehohglgaod
# 1. [Completed] Implement full method
# 2. Implement adaptation that cuts off when opposite wheel is at -v
# 3. [Maybe] Implement adaptation that cuts off when opposive wheel is at 0
# 4. [Maybe] Implement backup using Cornu/Euler spiral?
# 5. Implement regular Hermite Spline for intersection

# Equations for 3 points:
#     f(θ + θ_1 + θ_2) = r
#     tan(θ_1) * d_1 = r
#     tan(θ_2) * d_2 = r

# Expand concepts to a variable number of points