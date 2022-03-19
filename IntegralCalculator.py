from math import ceil, pi, sqrt, sin, cos

from DriveCharacterization import DriveCharacterization

class IntegralCalculator():
    def __init__(self, robotCharacteristics):
        self.robotCharacteristics = robotCharacteristics

        w = robotCharacteristics.w
        v = robotCharacteristics.v
        a = robotCharacteristics.a

        self.quarterTurn = sqrt(pi * w / a)
        self.maxT = max(self.quarterTurn, 2 * v / a)

        # Use 'middle point' to form quadratic
        count = ceil(self.quarterTurn / 0.005) # Make divisor smaller for more accuracy
        self.dt = self.quarterTurn / count

        points = []
        for i in range(2 * count + 1):
            t = self.quarterTurn * i / 2 / count
            commonTerm = (v - a*t/2, (a * t**2) / (2 * w))
            points.append((commonTerm[0] * cos(commonTerm[1]),commonTerm[0] * sin(commonTerm[1])))
        
        half_dt = self.dt/2
        self.curves = []
        for i in range(count):
            times = [self.dt*i, self.dt*i + half_dt, self.dt*i + half_dt*2]
            xVals = [points[i*2][0], points[i*2+1][0], points[i*2+2][0]]
            xCurve = self.solveQuadratic(times, xVals)

            yVals = [points[i*2][1], points[i*2+1][1], points[i*2+2][1]]
            yCurve = self.solveQuadratic(times, yVals)

            self.curves.append((xCurve, yCurve))
        
        self.sectionAreas = []
        # Precalculated integral sections
        for i in range(count):
            curve = self.curves[i]
            curveX = self.curves[i][0]
            curveY = self.curves[i][1]

            self.sectionAreas.append((\
                curveX[0] / 3 * ((self.dt * (i+1))**3 - (self.dt * i)**3)\
                + curveX[1] / 2 * ((self.dt * (i+1))**2 - (self.dt * i)**2)\
                + curveX[2] / 1 * ((self.dt * (i+1))**1 - (self.dt * i)**1),\
                curveY[0] / 3 * ((self.dt * (i+1))**3 - (self.dt * i)**3)\
                + curveY[1] / 2 * ((self.dt * (i+1))**2 - (self.dt * i)**2)\
                + curveY[2] / 1 * ((self.dt * (i+1))**1 - (self.dt * i)**1)\
            ))
        
        areas = []
        for i in self.sectionAreas:
            areas.append(i[1])
        print(sum(areas))



        #end

    def solveQuadratic(self, t: list[float, float, float], y: list[float, float, float]):
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
IntegralCalculator(DriveCharacterization(1,1,1,1))