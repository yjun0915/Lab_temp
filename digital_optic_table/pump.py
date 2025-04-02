import math
from algebra import rotate

rotate = rotate.rotate

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
        print(f"Pump located at {self.center}")

    def draw(self):
        self.image[self.center[0]][self.center[1]] = 1
        for dx in range(self.width):
            x1, y1 = rotate(angle=self.rotation, center=self.center, x=self.x+dx, y=self.y)
            x2, y2 = rotate(angle=self.rotation, center=self.center, x=self.x+dx, y=self.y+self.height)
            x1 = min(x1, self.offset[2])
            x2 = min(x2, self.offset[2])
            y1 = min(y1, self.offset[2])
            y2 = min(y2, self.offset[2])
            self.image[x1][y1] = 1
            self.image[x2][y2] = 1
        for dy in range(self.height):
            x1, y1 = rotate(angle=self.rotation, center=self.center, x=self.x, y=self.y+dy)
            x2, y2 = rotate(angle=self.rotation, center=self.center, x=self.x+self.width, y=self.y+dy)
            x1 = min(x1, self.offset[2])
            x2 = min(x2, self.offset[2])
            y1 = min(y1, self.offset[2])
            y2 = min(y2, self.offset[2])
            self.image[x1][y1] = 1
            self.image[x2][y2] = 1

        for p in range(int(0.025*self.magnitude)):
            p -= int(0.0125*self.magnitude)
            x, y = rotate(angle=self.rotation, center=self.center, x=self.x+self.width+p, y=self.y+int(self.height/2))
            x = min(x, self.offset[2])
            y = min(y, self.offset[2])
            self.image[x][y] = 1
        return self.image
