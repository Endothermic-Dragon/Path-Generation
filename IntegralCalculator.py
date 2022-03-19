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
        count = ceil(self.quarterTurn / 0.25)
        self.dt = self.quarterTurn / count / 2

        points = []
        for i in range(2 * count + 1):
            t = self.quarterTurn * i / 2 / count
            commonTerm = (v - a*t/2, (a * t**2) / (2 * w))
            points.append((commonTerm[0] * cos(commonTerm[1]),commonTerm[0] * sin(commonTerm[1])))
        
        curves = []
        for i in range(count):
            self.solveQuadratic(, *points[i*2:i*2+2])
        # Solve quadratic



        #end

    def solveQuadratic(t: List[float, float, float], y: List[float, float, float]):
        eq1 = [(t[1]**2 - t[0]**2, t[1] - t[0]), y[1] - y[0]]
        reg_eq1 = [(1, eq1[0][1] / eq1[0][0]), eq1[1] / eq1[0][0]]
        reg_eq3 = [(eq1[0][0] / eq1[0][1], 1), eq1[1] / eq1[0][1]]
        eq2 = [(t[2]**2 - t[0]**2, t[2] - t[0]), y[2] - y[0]]
        reg_eq2 = [(1, eq2[0][1] / eq2[0][0]), eq2[1] / eq2[0][0]]
        reg_eq4 = [(eq2[0][0] / eq2[0][1], 1), eq2[1] / eq2[0][1]]
        a = (reg_eq3[1] - reg_eq4[1]) / (reg_eq3[0][0] - reg_eq4[0][0])
        b = (reg_eq2[1] - reg_eq1[1]) / (reg_eq2[0][1] - reg_eq1[0][1])
        c = y[2] - a * t[2]**2 - b * t[2]
        return (a, b, c)

    def getY(t):
        print("Y")
        #return slope and y coordinate

    def getX(t):
        print("X")
        #return x coordinate


#0.25
