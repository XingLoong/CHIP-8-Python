from memory import Memory
from display import Display
import random

class CPU:

    def __init__(self, keypad):
        # start fresh
        # =Memory=
        self.memory = Memory()
        # =Registers=
        self.V = [0] * 8 * 2                # 16 8-bit register (VF usually for flags)
        self.index = 0                      # index register: points to memory location
        # timers
        self.delay_timer = 0                # delay timer, ticks own at a rate of 60Hz to 0
        self.sound_timer = 0                # sound timer, beeps until 0
        # =opcode stuff=
        self.stack = []                     # 16-bit addresses for subroutines/functions
        self.PC = 0x200                     # points to current instruction in memory starts at 0x200 (usually)
        self.opcode = 0                     # blank state
        # =Keypad=
        self.keypad = keypad
        # =Display=
        self.display = Display()

        # =Opcodes=
        self.opcode_table = {
            0x0000: lambda opcode: self.opcode_0(opcode),
            0x1000: lambda opcode: self.opcode_1(opcode & 0xFFF),
            0x2000: lambda opcode: self.opcode_2(opcode & 0xFFF),
            0x3000: lambda opcode: self.opcode_3((opcode >> 8) & 0xF, opcode & 0xFF),
            0x4000: lambda opcode: self.opcode_4((opcode >> 8) & 0xF, opcode & 0xFF),
            0x5000: lambda opcode: self.opcode_5((opcode >> 8) & 0xF, (opcode >> 4) & 0xF),
            0x6000: lambda opcode: self.opcode_6((opcode >> 8) & 0xF, opcode & 0xFF),
            0x7000: lambda opcode: self.opcode_7((opcode >> 8) & 0xF, opcode & 0xFF),
            0x8000: lambda opcode: self.opcode_8((opcode & 0x0F00) >> 8, (opcode & 0x00F0) >> 4, opcode & 0xF),
            0x9000: lambda opcode: self.opcode_9((opcode >> 8) & 0xF, (opcode >> 4) & 0xF),
            0xA000: lambda opcode: self.opcode_A(opcode & 0xFFF),
            0xB000: lambda opcode: self.opcode_B(opcode & 0xFFF),
            0xC000: lambda opcode: self.opcode_C((opcode >> 8) & 0xF, opcode & 0xFF),
            0xD000: lambda opcode: self.opcode_D((opcode >> 8) & 0xF, (opcode >> 4) & 0xF, opcode & 0xF),
            0xE000: lambda opcode: self.opcode_E((opcode & 0x00FF), (opcode >> 8) & 0xF),
            0xF000: lambda opcode: self.opcode_F((opcode & 0x00FF), (opcode >> 8) & 0xF),
        }
        self.opcode_0_dispatch = {
            0x00E0: self.display.clear,
            0x00EE: self.return_from_subroutine,
        }
        self.opcode_8_dispatch = {
            0x0: lambda X, Y: self.V.__setitem__(X, self.V[Y]),
            0x1: lambda X, Y: self.V.__setitem__(X, self.V[X] | self.V[Y]),
            0x2: lambda X, Y: self.V.__setitem__(X, self.V[X] & self.V[Y]),
            0x3: lambda X, Y: self.V.__setitem__(X, self.V[X] ^ self.V[Y]), 
            0x4: lambda X, Y: self._add_with_carry(X, Y), 
            0x5: lambda X, Y: self._sub_with_borrow(X, Y), 
            0x6: lambda X, Y: self._shift_right(X), 
            0x7: lambda X, Y: self._reverse_sub(X, Y), 
            0xE: lambda X, Y: self._shift_left(X),
        }
        self.opcode_E_dispatch = {
            0x009E: self._pressed_skip,
            0x00A1: self._unpressed_skip,
        }
        self.opcode_F_dispatch = {
            0x0007: lambda X: self.V.__setitem__(X, self.delay_timer),
            0x000A: lambda X: self.V.__setitem__(X, self.keypad.on_key_press),
            0x0015: lambda X: setattr(self, "delay_timer", self.V[X]),
            0x0018: lambda X: setattr(self, "sound_timer", self.V[X]),
            0x001E: lambda X: setattr(self, 'index', (self.index + self.V[X]) & 0xFFF),
            0x0029: lambda X: setattr(self, 'index', (5 * self.V[X]) & 0xFFF),
            0x0033: lambda X: self._set_decimal(X),
            0x0055: lambda X: self._write_memory(X),
            0x0065: lambda X: self._read_memory(X),
        }
    def load_rom(self, path):
        with open(path, "rb") as f:
            rom = f.read()
        for i, byte in enumerate(rom):
            self.memory[0x200 + i] = byte
    def clear_screen(self):
        self.display_buffer = [[0] * 64 for _ in range(32)]
    def return_from_subroutine(self):
        if not self.stack:
            return False
        self.PC = self.stack.pop()
        return False
    def _add_with_carry(self, X, Y):
        sum = self.V[X] + self.V[Y]
        self.V[X] = sum & 0xFF
        self.V[0xF] = 1 if sum > 0xFF else 0
    def _sub_with_borrow(self, X, Y):
        diff = self.V[X] - self.V[Y]
        temp = self.V[X]
        self.V[X] = diff & 0xFF
        self.V[0xF] = 1 if temp >= self.V[Y] else 0
    def _reverse_sub(self, X, Y):
        diff = self.V[Y] - self.V[X]
        temp = self.V[X]
        self.V[X] = diff & 0xFF
        self.V[0xF] = 1 if self.V[Y] >= temp else 0
    def _shift_right(self, X):
        temp = self.V[X]
        self.V[X] >>= 1
        self.V[0xF] = temp & 0x1 
    def _shift_left(self, X):
        temp = self.V[X]
        self.V[X] = (self.V[X] << 1) & 0xFF 
        self.V[0xF] = (temp >> 7) & 0x1
    def _wait_for_key(self, X):
        key = self.keypad.get_key_pressed()
        self.V[X] = key
    def _pressed_skip(self, X):
        if self.keypad.is_key_pressed(self.V[X]):
            self.PC += 4
            return False
    def _unpressed_skip(self, X):
        if not self.keypad.is_key_pressed(self.V[X]):
            self.PC += 4
            return False
    def _set_decimal(self, X):
        value = self.V[X]
        self.memory[self.index] = value // 100
        self.memory[self.index + 1] = (value // 10) % 10
        self.memory[self.index + 2] = value % 10
    def _write_memory(self, X):
        for i in range(X + 1):
            self.memory[self.index + i] = self.V[i]
    def _read_memory(self, X):
        for i in range(X + 1):
            self.V[i] = self.memory[self.index + i]
    def _update_timers(self):
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            if self.sound_timer ==0:
                #stop audio?
                pass
        # =opcode family=
    def opcode_0(self, opcode): 
        if opcode in self.opcode_0_dispatch:
            self.opcode_0_dispatch[opcode]()
        else:
            pass
    def opcode_1(self, NNN):
        self.PC = NNN & 0xFFF
        return False
    def opcode_2(self, NNN):
        self.stack.append(self.PC)
        self.PC = NNN & 0xFFF
        return False
    def opcode_3(self, X, NN):
        if self.V[X] == NN:
            self.PC += 4
            return False
    def opcode_4(self, X, NN):
        if self.V[X] != NN:
            self.PC += 4
            return False
    def opcode_5(self, X, Y):
        if self.V[X] == self.V[Y]:
            self.PC += 4
            return False
    def opcode_6(self, X, NN):
        self.V[X] = NN & 0xFF
    def opcode_7(self, X, NN):
        self.V[X] = (self.V[X] + NN) & 0xFF
    def opcode_8(self, X, Y, N): 
        handler = self.opcode_8_dispatch.get(N)
        if handler:
            handler(X, Y)
    def opcode_9(self, X, Y):
        if self.V[X] != self.V[Y]:
            self.PC += 4
            return False
    def opcode_A(self, NNN):
        self.index = NNN & 0xFFF
    def opcode_B(self, NNN):
        self.PC = (NNN & 0xFFF) + self.V[0] & 0xFFF
    def opcode_C(self, X, NN):
        self.V[X] = (random.randint(0, 255) & NN) & 0xFF
    def opcode_D(self, X, Y, N):
        x = self.V[X]
        y = self.V[Y]
        height = N
        sprite = [self.memory[self.index + i] for i in range(height)]
        collision = self.display.draw_sprite(x, y, sprite)
        self.V[0xF] = collision
    def opcode_E(self, subcode, X): 
        if subcode in self.opcode_E_dispatch:
            self.opcode_E_dispatch[subcode](X)
        else:
            return
    def opcode_F(self, subcode, X):
        if subcode in self.opcode_F_dispatch:
            self.opcode_F_dispatch[subcode](X)
        else:
            return

        

    
    def cycle(self):
        # =fetch=
        self.opcode = (self.memory[self.PC] << 8) | self.memory[self.PC+1]
        # =decode=
        mask = self.opcode & 0xF000
        # =execute=
        increment_PC = True
        handler = self.opcode_table.get(mask) 
        if handler:
            increment_PC = handler(self.opcode) is not False
        # =Update PC=
        if increment_PC:
            self.PC += 2

        # =update timers=
  
        

        
