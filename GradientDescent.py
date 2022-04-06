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

    def step(self):
        distances = self.distances
        turnAngles = self.turnAngles
        adjustAngles = self.adjustAngles
        radii = []
        integralCalculator = self.integralCalculator

        for i in range(len(turnAngles)):
            self.adjustedTurnAngles[i] = self.fixAngle(self.turnAngles[i] + self.adjustAngles[i+1] - self.adjustAngles[i])

        radii.append(0)
        for angle in self.adjustedTurnAngles:
            if angle >= 0:
                radii.append(integralCalculator.getRadius(angle))
            else:
                radii.append(-integralCalculator.getRadius(-angle))
        radii.append(0)
        self.radii = radii

        newAngles = []
        for i in range(len(radii) - 1):
            # Check if too short
            newAngles.append(asin((radii[i] - radii[i+1])/distances[i]))

        for i in range(len(adjustAngles)):
            self.adjustAngles[i] = (adjustAngles[i] + newAngles[i]) / 2