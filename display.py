class Display:
    WIDTH = 64
    HEIGHT = 32

    def __init__(self):
        self.buffer = [[0] * self.WIDTH for _ in range(self.HEIGHT)]

    def clear(self):
        self.buffer = [[0] * self.WIDTH for _ in range(self.HEIGHT)]

    def draw_sprite(self, x, y, sprite):
        collision = 0
        for row, byte in enumerate(sprite):
            for col in range(8):
                pixel = (byte >> (7 - col)) & 1
                if pixel:
                    X = (x + col) % self.WIDTH
                    Y = (y + row) % self.HEIGHT
                    if self.buffer[Y][X]:
                        collision = 1
                    self.buffer[Y][X] ^= 1
        return collision
