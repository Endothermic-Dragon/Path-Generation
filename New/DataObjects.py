import pygame
from math import degrees, radians

# Global variables
import Global

# Store point as object, accessible by index or attribute
class Point():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.coords = [x, y]

    def __getitem__(self, i: int):
        if i not in [0,1]:
            raise IndexError(
                "Coordinate index out of range, must be either 0 or 1.\n"
                + "Attempted to access index " + str(i) + "."
            )
        return self.coords[i]

    def __len__(self):
        return 2

# Translate between field coordinate and pygame display coordinates
class Translate():
    @staticmethod
    def toNative(rect: pygame.Rect, coords: tuple[float, float]):
        fieldSize = Global.fieldDimensions
        size = rect.size
        shift = rect.topleft
        return Point(
            [(coords[i]-shift[i]) * fieldSize[i]/size[i] for i in [0,1]]
        )

    @staticmethod
    def toPygame(rect: pygame.Rect, point: Point | list[float, float]):
        fieldSize = Global.fieldDimensions
        size = rect.size
        shift = rect.topleft
        return tuple(
            [point[i] * size[i]/fieldSize[i] + shift[i] for i in [0,1]]
        )

# Easily deal with angles
class Angle():
    def __init__(self, angle: float, angleType: str) -> None:
        angleType = angleType.lower()
        if angleType in ["d", "deg", "degrees"]:
            self.d = self.deg = self.degrees = angle
            self.r = self.rad = self.radians = radians(angle)

        elif angleType in ["r", "rad", "radians"]:
            self.r = self.rad = self.radians = angle
            self.d = self.deg = self.degrees = degrees(angle)

        else:
            raise SyntaxError(
                "Invalid input for angle type, must be instantiated in degrees or radians.\n"
                + "Please enter \"d\", \"deg\", or \"degrees\" to instantiate the angle in degrees.\n"
                + "Please enter \"r\", \"rad\", or \"radians\" to instantiate the angle in radians.\n"
                + "Attempted to instantiate in \"" + angleType + "\"."
            )
    
    def __add__(self, otherAngle):
        return Angle(self.d + otherAngle.d, "d")
    
    def __sub__(self, otherAngle):
        return Angle(self.d - otherAngle.d, "d")