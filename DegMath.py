from math import atan2 as rad_atan2, pi, asin as rad_asin, sin as rad_sin, cos as rad_cos

# Returns degrees instead of radians
def atan2(y, x):
    return rad_atan2(y, x) * 180 / pi

def asin(val):
    #print(val)
    return rad_asin(val) * 180 / pi

def sin(val):
    return rad_sin(val * pi / 180)

def cos(val):
    return rad_cos(val * pi / 180)