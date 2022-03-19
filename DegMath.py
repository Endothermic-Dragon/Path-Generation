from math import atan2 as rad_atan2, pi, cos as rad_cos

# Returns degrees instead of radians
def atan2(y, x):
    return rad_atan2(y, x) * 180 / pi

def cos(deg):
    return rad_cos(deg * pi / 180)