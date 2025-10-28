from font import FONTSET

class Memory:

    def __init__(self):
        # memory
        self.memory = [0] * 16 * 16 * 16    # 0x000 - 0xFFF
        self.fontset = FONTSET
        self.load_fontset()

    def __getitem__(self, addr):
        return self.memory[addr]
    
    def __setitem__(self, addr, value):
        self.memory[addr] = value

    def load_fontset(self, start = 0x50):
        for i, byte in enumerate(self.fontset):
            self.memory[start + i] = byte

    def load_rom(self, path):
        with open(path, "rb") as f:
            rom = f.read()
        for i, byte in enumerate(rom):
            self[0x200 + i] = byte

    def read(self, addr):
        return self[addr]
    
    def write(self, addr, value):
        self[addr] = value & 0xFF