import sys
from emulator import Emulator
from sound import SoundPlayer, schedule_timers
import pyglet

rom_path = sys.argv[1] if len(sys.argv) > 1 else "./ROMs/6-keypad.ch8"

emulator = Emulator(rom_path)
sound_player = SoundPlayer(frequency=262, volume=0.3)
schedule_timers(emulator.cpu, sound_player)

def update(dt):
    for _ in range(13):
        emulator.cpu.cycle()
        if emulator.cpu.draw_flag:
            break

    if emulator.cpu.draw_flag:
        emulator.draw()
        emulator.cpu.draw_flag = False

    emulator.window.clear()
    emulator.batch.draw()

pyglet.clock.schedule_interval(update, 1/60.0)  # 60 FPS
pyglet.app.run()
