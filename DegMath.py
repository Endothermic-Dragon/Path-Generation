from math import atan2 as rad_atan2, pi, asin as rad_asin

# Returns degrees instead of radians
def atan2(y, x):
    return rad_atan2(y, x) * 180 / pi

def asin(val):
    return rad_asin(val) * 180 / pi