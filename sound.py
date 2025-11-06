import pyglet

class SoundPlayer:
    def __init__(self, frequency=440, volume=0.3):
        # Create a short tone but it will be looped
        tone = pyglet.media.synthesis.Square(1.0, frequency)
        self.source = pyglet.media.StaticSource(tone)
        
        self.player = pyglet.media.Player()
        self.player.queue(self.source)
        self.player.loop = True
        self.player.volume = volume

    def play(self):
        if not self.player.playing:
            self.player.play()

    def stop(self):
        if self.player.playing:
            self.player.pause()
            # Reset playback to the beginning
            self.player.seek(0.0)

def schedule_timers(cpu, sound_player):
    def update_timers(dt):
        # Decrease the CHIP-8 sound timer
        sound_active = cpu.decrease_timer()
        if sound_active:
            sound_player.play()
        else:
            sound_player.stop()

    pyglet.clock.schedule_interval(update_timers, 1/60.0)
