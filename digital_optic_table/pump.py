class Pump:
    def __init__(self, image, x, y, width, height, magnitude):
        self.image = image
        self.x = int(x * magnitude)
        self.y = int(y * magnitude)
        self.width = int(width * magnitude)
        self.height = int(height * magnitude)
        self.magnitude = magnitude

    def draw(self):
        for dx in range(self.width):
            self.image[self.y][self.x + dx] = 1
            self.image[self.y + self.height][self.x + dx] = 1
        for dy in range(self.height):
            self.image[self.y + dy][self.x] = 1
            self.image[self.y + dy][self.x + self.width] = 1
        return self.image
