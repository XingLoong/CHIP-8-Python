from pyglet.window import key
   # 1 2 3 C  <- typical layout  1 2 3 4
   # 4 5 6 D       modern ->     Q W E R   
   # 7 8 9 E                     A S D F
   # A 0 B F                     Z X C V 
KEY_MAP = {
    key._1: 0x1, key._2: 0x2, key._3: 0x3, key._4: 0xC,
    key.Q: 0x4, key.W: 0x5, key.E: 0x6, key.R: 0xD,
    key.A: 0x7, key.S: 0x8, key.D: 0x9, key.F: 0xE,
    key.Z: 0xA, key.X: 0x0, key.C: 0xB, key.V: 0xF,
}

class Keypad:
    def __init__(self):
        self.keys = [False] * 16
        self.last_pressed = None
        self.key_map = KEY_MAP

    def on_key_press(self, symbol, modifiers):
        print(f"Key pressed raw symbol: {symbol}")
        if symbol in self.key_map:
            key_id = self.key_map[symbol]
            self.keys[key_id] = True
            self.last_pressed = key_id
            print(f"Key pressed: {hex(key_id)}")

    def on_key_release(self, symbol, modifiers):
        if symbol in self.key_map:
            key_id = self.key_map[symbol]
            self.keys[key_id] = False
            print(f"Key released: {hex(key_id)}")

    def is_key_pressed(self, chip8_key):
        if not isinstance(chip8_key, int):
            return False
        if 0 <= chip8_key < 16:
            return self.keys[chip8_key]
        return False
    
    def get_pressed_key(self):
        if self.last_pressed is not None:
            key = self.last_pressed
            self.last_pressed = None
            return key
        return None