import pyglet
from pyglet import shapes
from cpu import CPU
from keypad import Keypad

SCALE = 10
WIDTH = 64 * SCALE
HEIGHT = 32 * SCALE

class Emulator:
    def __init__(self, rom_path):
        self.keypad = Keypad()
        self.cpu = CPU(self.keypad)
        self.cpu.memory.load_rom(rom_path)

        self.window = pyglet.window.Window(WIDTH, HEIGHT, caption="CHIP-8 Emulator")
        self.batch = pyglet.graphics.Batch()

        self.window.push_handlers(
            on_key_press=self.keypad.on_key_press,
            on_key_release=self.keypad.on_key_release
        )

        # Create rectangles for pixels
        self.pixels = [[shapes.Rectangle(x*SCALE, HEIGHT - (y + 1) * SCALE, SCALE, SCALE,
                                         color=(0, 0, 0), batch=self.batch)
                        for x in range(64)] for y in range(32)]

    def draw(self):
        for y in range(32):
            for x in range(64):
                self.pixels[y][x].color = (255, 255, 255) if self.cpu.display.buffer[y][x] else (0, 0, 0)
