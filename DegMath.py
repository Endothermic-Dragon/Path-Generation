from math import atan2 as rad_atan2, pi

def atan2(y, x):
    return rad_atan2(y, x) * 180 / pi