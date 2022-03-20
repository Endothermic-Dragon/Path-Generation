from math import ceil, floor, pi, sqrt, sin, cos
from DriveCharacterization import DriveCharacterization

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
    
    def getYslope(self, t):
        w = self.robotCharacteristics.w
        v = self.robotCharacteristics.v
        a = self.robotCharacteristics.a

        return (v - a*t/2) * sin(a * t**2 / 2 / w)
    
    def getMeasurements(self, degAngle):
        if not (0 <= degAngle <= 180):
            raise ValueError("Invalid angle value, must be between 0 and 180, in degrees.")
        
        radAngle = degAngle * pi / 180
        halfAngle = radAngle / 2

        w = self.robotCharacteristics.w
        a = self.robotCharacteristics.a

        t = sqrt(2 * w * halfAngle / a)

        travelDistance = self.getX(t)
        radius = self.getY(t)
        angleDerivative = (self.getYslope(t) * sqrt(w / (2*a*halfAngle))) * pi / 360

        return (radius, angleDerivative, travelDistance)