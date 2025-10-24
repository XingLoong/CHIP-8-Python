from memory import Memory
from display import Display

class CPU:

    def __init__(self):
        # start fresh
        # self.clear()

        # =Memory=
        self.memory = Memory()

        # registers
        self.V = [0] * 8 * 2               # 16 8-bit register (VF usually for flags)
        self.index = 0                      # index register: points to memory location

        # timers
        self.delay_timer = 0                      # delay timer, ticks own at a rate of 60Hz to 0
        self.sound_timer = 0                      # sound timer, beeps until 0

        # other
        self.stack = []                     # 16-bit addresses for subroutines/functions
        self.PC = 0x200                     # points to current instruction in memory starts at 0x200 (usually)
        self.opcode = 0                     # blank state
        

        # input/keypresses
        self.key_inputs = [0] * 16          # 1 2 3 C  <- typical layout  1 2 3 4
                                            # 4 5 6 D       modern ->     Q W E R   
                                            # 7 8 9 E                     A S D F
                                            # A 0 B F                     Z X C V   
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
            0x8000: lambda opcode: self.opcode_8((opcode >> 12) & 0xF, (opcode >> 8) & 0xF, (opcode >> 4) & 0xF, opcode & 0xF),
            0xA000: lambda opcode: self.opcode_A(opcode & 0xFFF),
            0xB000: lambda opcode: self.opcode_B(opcode & 0xFFF),
            0xC000: lambda opcode: self.opcode_C((opcode >> 8) & 0xF, opcode & 0xFF),
            0xD000: lambda opcode: self.opcode_D((opcode >> 8) & 0xF, (opcode >> 4) & 0xF, opcode & 0xF),
            0xE000: lambda opcode: self.opcode_E((opcode >> 8) & 0xF),
            0xF000: lambda opcode: self.opcode_F((opcode >> 8) & 0xF, opcode & 0xFF),
        }

    def load_rom(self, path):
        with open(path, "rb") as f:
            rom = f.read()
        for i, byte in enumerate(rom):
            self.memory[0x200 + i] = byte
    def clear_screen(self):
        self.display_buffer = [[0] * 64 for _ in range(32)]
    def return_from_subroutine(self):
        self.PC = self.stack.pop()              
        return

        
        # =opcode family=
    def opcode_0(self, opcode):
        opcode_0_dispatch = {
            0x00E0: self.clear_screen,
            0x00EE: self.return_from_subroutine
        }
        if opcode in opcode_0_dispatch:
            opcode_0_dispatch[opcode]()
        else:
            pass
    def opcode_1(self, NNN):
        self.PC = NNN
        return
    def opcode_2(self, NNN):
        self.stack.append(self.PC + 2)
        self.PC = NNN
        return
    def opcode_3(self, X, NN):
        if self.V[X] == NN:
            self.PC += 4
        return
    def opcode_4(self, X, NN):
        if self.V[X] != NN:
            self.PC += 4
        return
    def opcode_5(self, X, Y):
        if self.V[X] == self.V[Y]:
            self.PC += 4
        return
    def opcode_6(self, X, NN):
        self.V[X] = NN
    def opcode_7(self, X, NN):
        self.V[X] = self.V[X] + NN
    def opcode_8(self, M, X, Y, N):
        def op_0():
            self.V[X] = self.V[Y]
        def op_1():
            self.V[X] != self.V[Y]
        def op_2():
            self.V[X] &= self.V[Y]
        def op_3():
            self.V[X] ^= self.V[Y]
        def op_4():
            sum = self.V[X] + self.V[Y]
            self.V[0xF] = 1 if sum > 0xFF else 0
            self.V[X] = sum & 0xFF
        def op_5():
            self.V[0xF] = 1 if self.V[X] >= self.V[Y] else 0
            self.V[X] -= self.V[Y] & 0xFF
        def op_6():
            self.V[X] = self.V[X] > 1
            self.V[0xF] = N & 0xF
        def op_7():
            self.V[0xF] = 1 if self.V[Y] >= self.V[X] else 0
            self.V[X] = (self.V[Y] - self.V[X]) & 0xFF
        def op_E():
            self.V[0xF] = (self.V[X] >> 7) & 0x1
            self.V[X] = (self.V[X] << 1) & 0xFF  
        opcode_8_dispatch = {
            0: op_0, 1: op_1, 2: op_2, 3: op_3, 4: op_4, 5:op_5, 6:op_6, 7:op_7, 0xE:op_E,
        }
        if M in opcode_8_dispatch:
            opcode_8_dispatch[M]()
    def opcode_A(self, NNN):
        self.index = NNN
    def opcode_B(self, NNN):
        self.PC = NNN + self.V[0]
    def opcode_C(self, X, NN):
        self.V[X] = ((id(object()) * 37) % 256) & NN
    def opcode_D(self, X, Y, N):
        x = self.V[X]
        y = self.V[Y]
        height = N

        sprite = [self.memory[self.index + i] for i in range(height)]

        collision = self.display.draw_sprite(x, y, sprite)
        self.V[0xF] = collision
    def opcode_E(self, X): 
        pass
    def opcode_F(self, X, mask):
        def op_07(self):
            self.V[X] = self.delay_timer
        def op_0A(self):
            pass

        opcode_F_dispatch = {
            0x07: op_07,
            0x0A: op_0A,
        }

    
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
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            # play sound?

      
        

        
