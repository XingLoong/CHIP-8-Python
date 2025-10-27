class Display:
    WIDTH = 64
    HEIGHT = 32

    def __init__(self):
        self.buffer = [[0] * self.WIDTH for _ in range(self.HEIGHT)]

    def clear(self):
        self.buffer = [[0] * self.WIDTH for _ in range(self.HEIGHT)]

    def draw_sprite(self, x, y, sprite):
        x %= self.WIDTH
        y %= self.HEIGHT
        collision = 0
        for row, byte in enumerate(sprite):
            Y = y + row
            if Y >= self.HEIGHT:
                continue  # clip vertically

            for col in range(8):
                X = x + col
                if X >= self.WIDTH:
                    continue  # clip horizontally

                pixel = (byte >> (7 - col)) & 1
                if pixel:
                    if self.buffer[Y][X]:
                        collision = 1
                    self.buffer[Y][X] ^= 1
        return collision
