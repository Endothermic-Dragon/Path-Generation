from DegMath import asin
from DriveCharacterization import DriveCharacterization
from IntegralCalculator import IntegralCalculator

class GradientDescent:
    def __init__(self, robotCharacteristics: DriveCharacterization, distances: list[float], turnAngles: list[float]):
        self.distances = distances
        self.turnAngles = turnAngles.copy()
        self.adjustedTurnAngles = turnAngles.copy()
        self.adjustAngles = [0] * len(distances)
        self.integralCalculator = IntegralCalculator(robotCharacteristics)

    # Convert any angle to a domain-restricted angle between (-180, 180] degrees
    def fixAngle(self, angle):
        # Efficiently turn into a workable range between [0, 360)
        angle %= 360

        # Positive means clockwise rotation of robot
        # Negative means counterclockwise rotation of robot
        if angle > 180:
            angle -= 360

        return angle

#    def cost(self):
#        integralCalculator = self.integralCalculator
#        for angle in self.adjustedTurnAngles:
#            integralCalculator.getMeasurements(angle)

# Equations for 3 points:
#     f(θ + θ_1 + θ_2) = r
#     tan(θ_1) * d_1 = r
#     tan(θ_2) * d_2 = r

    def step(self):
        distances = self.distances
        turnAngles = self.turnAngles
        adjustAngles = self.adjustAngles
        radii = []
        angleGradient = []
        integralCalculator = self.integralCalculator

        for i in range(len(turnAngles)):
            self.adjustedTurnAngles[i] = self.fixAngle(self.turnAngles[i] + self.adjustAngles[i+1] - self.adjustAngles[i])

        radii.append(0)
        for angle in self.adjustedTurnAngles:
            if angle >= 0:
                radii.append(integralCalculator.getMeasurements(angle))
            else:
                radii.append(-integralCalculator.getMeasurements(-angle))
        radii.append(0)
        self.radii = radii
        #print(radii)

        newAngles = []
        for i in range(len(radii) - 1):
            newAngles.append(asin((radii[i] - radii[i+1])/distances[i]))

        for i in range(len(adjustAngles)):
            self.adjustAngles[i] = (adjustAngles[i] + newAngles[i]) / 2
        
        #return adjustAngles