from math import ceil, pi, sqrt, sin, cos
from typing import List
from numpy import linalg.inv as inverseMatrix

class IntegralCalculator():
    def __init__(self, robotCharacteristics):
        self.robotCharacteristics = robotCharacteristics

        w = robotCharacteristics.w
        v = robotCharacteristics.v
        a = robotCharacteristics.a

        self.quarterTurn = sqrt(pi * w / a)
        self.maxT = max(self.quarterTurn, 2 * v / a)

        # Use 'middle point' to form quadratic
        count = ceil(self.quarterTurn / 0.125)
        self.dt = dt = self.quarterTurn / count

        points = []
        for i in range(count + 1):
            t = dt*i
            commonTerm = (v - a*t/2, (a * t**2) / (2 * w))
            points.append((commonTerm[0] * cos(commonTerm[1]),commonTerm[0] * sin(commonTerm[1])))
        
        # Solve quadratic




        self.dt *= 2
    def solveQuardatic(t: List[float, float, float], y: List[float, float, float]):
        eq1 = [(t[1]**2 - t[0]**2, t[1] - t[0]), y[1] - y[0]]
        reg_eq1 = [(1, eq1[1] / eq1[0]), eq1]
        eq2 = [(t[2]**2 - t[0]**2, t[2] - t[0]), y[2] - y[0]]
    def getY(t):
        print("Y")
        #return slope and y coordinate
    def getX(t):
        print("X")
        #return x coordinate


#0.25
