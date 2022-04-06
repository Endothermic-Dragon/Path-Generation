from math import ceil, floor, pi, sqrt, sin, cos
from DegMath import atan2
from DriveCharacterization import DriveCharacterization
import matplotlib.pyplot as plt

class IntegralCalculator():
    def __init__(self, robotCharacteristics: DriveCharacterization):
        self.robotCharacteristics = robotCharacteristics

        w = robotCharacteristics.w
        v = robotCharacteristics.v
        a = robotCharacteristics.a

        self.quarterTurn = sqrt(pi * w / a)
        self.maxT = max(self.quarterTurn, 2 * v / a)

        # Use 'middle point' to form quadratic
        # Make divisor smaller for more accuracy (currently ≈ 10 digits)
        count = ceil(self.quarterTurn / 0.03)
        self.dt = self.quarterTurn / count

        points = []
        for i in range(2 * count + 1):
            t = self.quarterTurn * i / 2 / count
            commonTerm = (v - a*t/2, (a * t**2) / (2 * w))
            points.append((commonTerm[0] * cos(commonTerm[1]), commonTerm[0] * sin(commonTerm[1])))

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
        for i in range(count):
            self.sectionAreas.append((\
                half_dt * (points[i*2][0] + 4*points[i*2+1][0] + points[i*2+2][0]) / 3,\
                half_dt * (points[i*2][1] + 4*points[i*2+1][1] + points[i*2+2][1]) / 3,\
            ))

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

    def getY(self, t):
        count = floor(t / self.dt)
        displacement = sum([i[1] for i in self.sectionAreas[:count]])
        curve = self.curves[count][1]
        displacement += curve[0] / 3 * (t**3 - (count * self.dt)**3)\
            + curve[1] / 2 * (t**2 - (count * self.dt)**2)\
            + curve[2] * (t - (count * self.dt))

        return displacement

    def getX(self, t):
        count = floor(t / self.dt)
        displacement = sum([i[0] for i in self.sectionAreas[:count]])
        curve = self.curves[count][0]
        displacement += curve[0] / 3 * (t**3 - (count * self.dt)**3)\
            + curve[1] / 2 * (t**2 - (count * self.dt)**2)\
            + curve[2] * (t - (count * self.dt))

        return displacement
    
    # def getYslope(self, t):
    #     w = self.robotCharacteristics.w
    #     v = self.robotCharacteristics.v
    #     a = self.robotCharacteristics.a

    #     return (v - a*t/2) * sin(a * t**2 / 2 / w)
    
    def thetaToTime(self, theta):
        w = self.robotCharacteristics.w
        a = self.robotCharacteristics.a
        return sqrt(2 * w * theta / a)
    
    def timeToTheta(self, time):
        w = self.robotCharacteristics.w
        a = self.robotCharacteristics.a
        return (time**2 * a / 2 / w)

    def overflowTheta(self, degAngle):
        if self.thetaToTime(self.halfTurnAngle(degAngle)) < self.maxT:
            return 0
        return (self.thetaToTime(self.halfTurnAngle(degAngle)) - self.maxT) * 2

    def halfTurnAngle(self, degAngle):
        if not (0 <= degAngle <= 180):
            raise ValueError("Invalid angle value, must be between 0 and 180, in degrees.")
        
        radAngle = degAngle * pi / 180
        return radAngle / 2

    def getRadius(self, degAngle):
        halfAngle = self.halfTurnAngle(degAngle)
        t = min(self.thetaToTime(halfAngle), self.maxT)

        radius = self.getY(t)

        return radius
    
    def getCoord(self, halfDegAngle):
        halfAngle = halfDegAngle * pi / 180
        t = min(self.thetaToTime(halfAngle), self.maxT)

        return (self.getX(t) * 100, self.getY(t) * 100)

    def getCoords(self, degAngle, turnAngle, translate):
        turnDirection = 1 if degAngle >= 0 else -1
        degAngle = abs(degAngle)
        halfAngle = self.halfTurnAngle(degAngle)
        theta = min(halfAngle, self.timeToTheta(self.maxT)) * 180 / pi

        coords = []
        lastCoord = self.getCoord(theta)

        for sampleDegAngle in range(2*int(theta // 1)):
            coord = self.getCoord(sampleDegAngle / 2)
            coords.append([coord[0] - lastCoord[0], coord[1] - lastCoord[1]])

        if int(theta // 1) != theta:
            coords.append([0,0])

        for i in range(len(coords) - 1):
            r = (coords[i][0]**2 + coords[i][1]**2)**0.5
            arg = (atan2(coords[i][1], coords[i][0]) - theta) * pi / 180
            coords[i] = (r * cos(arg), r * sin(arg) * turnDirection)

        reversedCoords = [(-coords[-i][0], coords[-i][1]) for i in range(2,len(coords))]

        coords = coords + list(reversedCoords)

        for i in range(len(coords)):
            try:
                r = (coords[i][0]**2 + coords[i][1]**2)**0.5
                arg = (atan2(coords[i][1], coords[i][0]) + turnAngle) * pi / 180
                coords[i] = [r * cos(arg) + translate.x, r * sin(arg) + translate.y]
            except:
                coords[i] = [translate.x, translate.x]

        return coords