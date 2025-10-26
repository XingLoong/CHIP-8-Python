import pyglet
from pyglet import shapes
from cpu import CPU
from keypad import Keypad

SCALE = 10
WIDTH = 64 * SCALE
HEIGHT = 32 * SCALE

window = pyglet.window.Window(WIDTH, HEIGHT, caption="CHIP-8 Emulator")
batch = pyglet.graphics.Batch()
keypad = Keypad()
cpu = CPU(keypad)
cpu.memory.load_rom("./ROMs/5-quirks.ch8")

window.push_handlers(
    on_key_press=keypad.on_key_press,
    on_key_release=keypad.on_key_release
)

# Create rectangles for pixels
pixels = [[shapes.Rectangle(x*SCALE, HEIGHT - (y + 1) * SCALE, SCALE, SCALE, color=(0, 0, 0), batch=batch)
           for x in range(64)] for y in range(32)]

def update(dt):
    # Run a few CPU cycles per frame to control speed
    for _ in range(60):
        cpu.cycle()

@window.event

def on_draw():
    window.clear()
    # Update screen based on display buffer
    for y in range(32):
        for x in range(64):
            if cpu.display.buffer[y][x]:
                pixels[y][x].color = (255, 255, 255)
            else:
                pixels[y][x].color = (0, 0, 0)
    batch.draw()

pyglet.clock.schedule_interval(update, 1/60.0)  # 60 FPS
pyglet.app.run()
