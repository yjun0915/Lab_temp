import math

def rotate(angle, center, x, y):
    _x = int(math.cos(math.radians(angle)) * (x - center[0]) - math.sin(math.radians(angle)) * (y - center[1]))
    _y = int(math.cos(math.radians(angle)) * (y - center[1]) + math.sin(math.radians(angle)) * (x - center[0]))
    return [_x + center[0], _y + center[1]]
