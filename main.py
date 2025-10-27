import pyglet
import math
import array
from pyglet import shapes
from cpu import CPU
from keypad import Keypad

SCALE = 10
WIDTH = 64 * SCALE
HEIGHT = 32 * SCALE

keypad = Keypad()
cpu = CPU(keypad)

window = pyglet.window.Window(WIDTH, HEIGHT, caption="CHIP-8 Emulator")
batch = pyglet.graphics.Batch()

window.push_handlers(
    on_key_press=keypad.on_key_press,
    on_key_release=keypad.on_key_release
)

# Create rectangles for pixels
pixels = [[shapes.Rectangle(x*SCALE, HEIGHT - (y + 1) * SCALE, SCALE, SCALE, color=(0, 0, 0), batch=batch)
           for x in range(64)] for y in range(32)]

cpu.memory.load_rom("./ROMs/7-beep.ch8")

def make_sound(frequency, duration, volume):
    tone = pyglet.media.synthesis.Square(duration, frequency)
    static_tone = pyglet.media.StaticSource(tone)
    player = pyglet.media.Player()
    player.volume = volume
    player.queue(static_tone)
    player.loop = True

    def keepalive(dt):
        if player.playing and player.source is None:
            player.queue(static_tone)
            player.play()

    pyglet.clock.schedule_interval(keepalive, duration * 0.9)
    return player

sound_player = make_sound(262, 1.0, 0.3)

def update_timers(dt):
    sound_active = cpu.decrease_timer()

    if sound_active and not sound_player.playing:
        sound_player.play()
    elif not sound_active and sound_player.playing:
        sound_player.pause()


@window.event

def update(dt):
    cpu.decrease_timer()
    for _ in range(11):
        cpu.cycle()
        if cpu.draw_flag:
            break

    if cpu.draw_flag:
        for y in range(32):
            for x in range(64):
                pixels[y][x].color = (255, 255, 255) if cpu.display.buffer[y][x] else (0, 0, 0)
        cpu.draw_flag = False

    window.clear()
    batch.draw()

pyglet.clock.schedule_interval(update_timers, 1/60.0)
pyglet.clock.schedule_interval(update, 1/60.0)  # 60 FPS
pyglet.app.run()
