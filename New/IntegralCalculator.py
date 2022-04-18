# Edit constant





from math import atan2, pi, sqrt, sin, cos, ceil
import matplotlib.pyplot as plt
from DataObjects import Angle
# Global variables
import Global

class IntegralCalculator():
    def __init__(self):
        self.robotCharacteristics = Global.driveCharacterization

        w = self.robotCharacteristics.w
        v = self.robotCharacteristics.v
        a = self.robotCharacteristics.a

        self.quarterTurn = sqrt(pi * w / a)
        self.maxTurnTime = min(self.quarterTurn, 2 * v / a)

        # Check max turn time
        print(self.quarterTurn)
        print(2*v/a)
        print(self.maxTurnTime)
        #print(self.maxTurnTime)
        self.maxTurnTheta = (self.maxTurnTime**2 * a / 2 / w)
        #print(self.maxTurnTheta * 180 / pi)

        # Use 'middle point' to form quadratic
        # Make divisor smaller for more accuracy (currently ≈ 10 digits)
        count = max(ceil(self.quarterTurn / 0.03), 100)
        self.dt = self.quarterTurn / count

        points = []
        for i in range(2 * count + 1):
            t = self.quarterTurn * i / 2 / count
            commonTerm = (v - a*t/2, (a * t**2)/(2 * w))
            points.append((
                commonTerm[0] * cos(commonTerm[1]),
                commonTerm[0] * sin(commonTerm[1])
            ))

        half_dt = self.dt/2
        self.curves = []
        for i in range(count):
            if self.dt*i > self.maxTurnTime:
                break
            times = [self.dt*i, self.dt*i + half_dt, self.dt*(i+1)]
            xVals = [points[i*2][0], points[i*2+1][0], points[i*2+2][0]]
            #print(xVals)
            xCurve = self._modelQuadratic(times, xVals)

            yVals = [points[i*2][1], points[i*2+1][1], points[i*2+2][1]]
            #print(yVals)
            yCurve = self._modelQuadratic(times, yVals)

            self.curves.append((xCurve, yCurve))

        self.areas = [[0,0]]
        for i in range(count):
            if self.dt*i > self.maxTurnTime:
                break
            self.areas.append(
                [self.areas[-1][j] + half_dt\
                * (points[i*2][j] + 4*points[i*2+1][j] + points[i*2+2][j]) / 3\
                for j in [0,1]]
            )

    # "Private" methods
    def _modelQuadratic(self, x: list[float, float, float], y: list[float, float, float]):
        a = (2*y[1] - y[2] - y[0]) / (2*x[1]**2 - x[2]**2 - x[0]**2)
        b = (y[2] - y[0] - a * (x[2]**2 - x[0]**2)) / (self.dt)
        c = sum([y[i] - a*x[i]**2 - b*x[i] for i in [0,1,2]]) / 3
        return (a, b, c)

    @staticmethod
    def _checkTheta(theta: float):
        if not (-pi < theta < pi):
            raise ValueError(
                "Value of turn angle must be between -π and π radians, exclusive.\n"
                + "Turn angle provided was " + str(theta) + "."
            )

        # Convenience for function "stacking"
        return theta

    def _thetaToTurnTime(self, theta: float):
        w = self.robotCharacteristics.w
        a = self.robotCharacteristics.a
        return min(sqrt(2 * w * theta / a), self.maxTurnTime)

    # def _turnTimeToTheta(self, t: float):
    #     if not (0 <= t <= self.maxTurnTime):
    #         raise ValueError(
    #             "Turn time must be between 0 and " + str(self.maxTurnTime) + " seconds.\n"
    #             + "Time length provided was " + str(t) + "."
    #         )
    #     w = self.robotCharacteristics.w
    #     a = self.robotCharacteristics.a
    #     return (t**2 * a / 2 / w)

    def _getCoordFromTurnTime(self, t: float, coordType: int):
        count = int(t // self.dt)
        displacement = self.areas[count][coordType]
        curve = self.curves[count][coordType]
        displacement += curve[0] / 3 * (t**3 - (count * self.dt)**3)\
            + curve[1] / 2 * (t**2 - (count * self.dt)**2)\
            + curve[2] * (t - (count * self.dt))

        return displacement

    def _getCoordFromTheta(self, theta: float, coordType: int):
        theta = abs(self._checkTheta(theta)) / 2
        t = self._thetaToTurnTime(theta)
        return self._getCoordFromTurnTime(t, coordType)
    
    def _getCoordsFromTurnTheta(self, theta: float):
        t = self._thetaToTurnTime(theta)
        return [self._getCoordFromTurnTime(t, i) for i in [0,1]]

    # Public methods
    def getExtenderLength(self, theta: Angle):
        return self._getCoordFromTheta(theta.r, 0)

    def getRadius(self, theta: Angle):
        multiplier = 1 if theta.r > 0 else -1
        return self._getCoordFromTheta(theta.r, 1) * multiplier

    def getDrawPath(self, thetaOriginal: Angle, faceDirection: Angle, translate: list[float, float]):
        multiplier = 1 if thetaOriginal.r > 0 else -1
        theta = abs(self._checkTheta(thetaOriginal.r))
        print(theta*180/pi)
        faceDirection = faceDirection.r

        if theta <= self.maxTurnTheta * 2:
            stationaryAngle = 0
            theta /= 2
        else:
            # Calculate
            print(1)
            stationaryAngle = 0 #(theta - self.maxTurnTheta * 2) * multiplier
            theta = self.maxTurnTheta

        #Rest






        coords = []
        lastCoord = self._getCoordsFromTurnTheta(theta)

        for sampleDegAngle in range(2 * int(Angle(theta, "r").d // 1)):
            coord = self._getCoordsFromTurnTheta(Angle(sampleDegAngle / 2, "d").r)
            coords.append(
                [(coord[i] - lastCoord[i]) for i in [0,1]]
            )
        #if coords[-1] != [0,0]:
        #    coords.append([0,0])
        
        #print(coords[0])
        #print(len(self.areas))
        splitCoords = [[coords[j][i] for j in range(len(coords))] for i in [0,1]]
        plt.plot(*splitCoords)
        plt.show()

        for i in range(len(coords) - 1):
            r = (coords[i][0]**2 + coords[i][1]**2)**0.5
            arg = (atan2(coords[i][1], coords[i][0]) - theta) * pi / 180
            coords[i] = (r * cos(arg), r * sin(arg) * multiplier)

        reversedCoords = [(-coords[-i][0], coords[-i][1]) for i in range(2,len(coords))]

        coords = coords + list(reversedCoords)

        for i in range(len(coords)):
            r = (coords[i][0]**2 + coords[i][1]**2)**0.5
            arg = (atan2(coords[i][1], coords[i][0]) + faceDirection + stationaryAngle) * pi / 180
            coords[i] = [r * cos(arg) + translate[0], r * sin(arg) + translate[1]]

        return coords


    #def getTimestampCalculator(self, theta: float):
        #define










"""
    def _getOverflowTime(self, t: float):
        return max(t - self.maxTurnTime, 0)

    def _timeToTheta(self, t: float):
        # FIXXXXXXXXX
        #tTurning
        w = self.robotCharacteristics.w
        a = self.robotCharacteristics.a
        return (t**2 * a / 2 / w)

    def overflowTurnTime(self, t: float):
        return t / 2 > self.maxTurnTime

    def overflowTurnTheta(self, theta: float):
        return theta / 2 > self.timeToTheta(self.maxTurnTime)

    def getCoordFromTime(self, t: float, coordType: int):
        t = min(t, self.maxTurnTime)
        count = int(t // self.dt)
        displacement = self.areas[count][coordType]
        curve = self.curves[count][coordType]
        displacement += curve[0] / 3 * (t**3 - (count * self.dt)**3)\
            + curve[1] / 2 * (t**2 - (count * self.dt)**2)\
            + curve[2] * (t - (count * self.dt))

        return displacement

    def getCoordFromTurnTheta(self, theta: float, coordType: int):
        return self.getCoordFromTime(self._thetaToTime(theta) / 2, coordType)

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
"""

a = IntegralCalculator()
#x = a._getCoordFromTime(0.7, 0)
#y = a._getCoordFromTime(0.7, 1)
#print(x, y)
a.getDrawPath(Angle(150, "d"), Angle(0, "d"), [0,0])

vals = []
for i in [10, 50, 70]:
    vals.append(a.getRadius(Angle(i, "d")))
print(vals)


# Works
#   1. __init__
#   2. _modelQuadratic
#   3. _getCoordFromTurnTime
#   4. _getCoordFromTheta
# Not tested, but works
#   1. _checkTheta
#   2. _thetaToTurnTime
# Doesn't work
#   1. getExtenderLength
#   2. getRadius
#   3. getDrawPath
# Not tested
#   1. _getCoordFromTheta
#           Fixed - error was off by 1 in self.area index
#   2. _getCoordsFromTurnTheta

# Root problem in _getCoordFromTheta