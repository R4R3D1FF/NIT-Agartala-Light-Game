from math import pi, atan
def dist(x, y, a, b):
    return ((x - a)**2 + (y - b)**2)**(0.5)

def arctan(a, b):
    if b == 0:
        if a > 0:
            return pi/2
        elif a < 0:
            return -pi/2
        else:
            return -pi/2
    elif b > 0:
        return atan(a/b)
    elif b < 0:
        return pi + atan(a/b)
    else:
        if b > 0:
            return pi
        else:
            return -pi