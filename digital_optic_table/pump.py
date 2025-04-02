import math

from PIL.ImageChops import offset
from scipy.ndimage import rotate


class Pump:
    def __init__(self, image, offset, x, y, width, height, rotation, magnitude):
        self.image = image
        self.offset = offset
        self.x = offset[0] + int(x * magnitude)
        self.y = offset[1] + int(y * magnitude)
        self.width = int(width * magnitude)
        self.height = int(height * magnitude)
        self.rotation = rotation
        self.magnitude = magnitude

        self.center = [int(self.x + self.width/2), int(self.y + self.height/2)]
        print(self.center)

    def draw(self):
        for dx in range(self.width):
            x1, y1 = self.rotate(angle=self.rotation, center=self.center, x=self.x+dx, y=self.y)
            x2, y2 = self.rotate(angle=self.rotation, center=self.center, x=self.x+dx, y=self.y+self.height)
            x1 = min(x1, self.offset[2])
            x2 = min(x2, self.offset[2])
            y1 = min(y1, self.offset[2])
            y2 = min(y2, self.offset[2])
            self.image[x1][y1] = 1
            self.image[x2][y2] = 1
        for dy in range(self.height):
            x1, y1 = self.rotate(angle=self.rotation, center=self.center, x=self.x, y=self.y+dy)
            x2, y2 = self.rotate(angle=self.rotation, center=self.center, x=self.x+self.width, y=self.y+dy)
            x1 = min(x1, self.offset[2])
            x2 = min(x2, self.offset[2])
            y1 = min(y1, self.offset[2])
            y2 = min(y2, self.offset[2])
            self.image[x1][y1] = 1
            self.image[x2][y2] = 1

        for p in range(int(0.025*self.magnitude)):
            p -= int(p/2)
            x, y = self.rotate(angle=self.rotation, center=self.center, x=self.x+self.width+p, y=self.y+int(self.height/2))
            x = min(x, self.offset[2])
            y = min(y, self.offset[2])
            self.image[x][y] = 1
        return self.image

    def rotate(self, angle, center, x, y):
        _x = int(math.cos(math.radians(angle))*(x-center[0]) - math.sin(math.radians(angle))*(y-center[1]))
        _y = int(math.cos(math.radians(angle))*(y-center[1]) + math.sin(math.radians(angle))*(x-center[0]))
        return [_x+center[0], _y+center[1]]
