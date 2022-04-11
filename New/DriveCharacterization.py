# Basic characteristics of the robot
class DriveCharacterization():
    def __init__(self, width: float, maxVelocity: float, maxAcceleration: float, maxWidth: float):
        self.width = self.w = width
        self.maxVelocity = self.v = maxVelocity
        self.maxAcceleration = self.a = maxAcceleration
        self.maxWidth = maxWidth