class CPU:

    def __init__(self):
        # start fresh
        # self.clear()

        # memory
        self.memory = [0] * 16 * 16 * 16    # 0x000 - 0xFFF

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
        # font? 050 - 09F (first 512 is okay)

        # input/keypresses
        self.key_inputs = [0] * 16          # 1 2 3 C  typical layout
                                            # 4 5 6 D
                                            # 7 8 9 E
                                            # A 0 B F
        # display - 64 x 32 pixel display
        self.display_buffer = [[0] * 64 for _ in range(32)]

    def cycle(self):
        # =fetch=
        self.opcode = (self.memory[self.PC] << 8) | self.memory[self.PC+1]

        # =decode=  0x(N1)(N2)(N3)(N)
        self.N1 = self.opcode >> 12
        self.N2 = (self.opcode >> 8) & 0xF      # usually Vx
        self.N3 = (self.opcode >> 4) & 0xF      # usuall Vy
        self.N = self.opcode & 0xF             # mask 0xF etc
        self.NN = self.opcode & 0xFF
        self.NNN = self.opcode & 0xFFF

        # =execute=
        if self.N1 == 0:
            if self.opcode == 0x00E0:
                self.display_buffer = [[0] * 64 for _ in range(32)] #clear screen
            elif self.opcode == 0x00EE:
                self.PC = self.stack.pop()              #returns to subroutine
                return
        elif self.N1 == 1:
            self.PC = self.NNN 
            return
        elif self.N1 == 2:
            self.stack.append(self.PC + 2)
            self.PC = self.NNN      # jumps to subroutine
            return
        elif self.N1 == 3:
            if self.V[self.N2] == self.NN:
                self.PC += 4
            return
        elif self.N1 == 4:
            if self.V[self.N2] != self.NN:
                self.PC += 4
            return
        elif self.N1 == 6:
            self.V[self.N2] = (self.N3 << 4) | self.N
        elif self.N1 == 8:
            if self.N == 0x0:
            # 8xy0: Set Vx = Vy
                self.V[self.N2] = self.V[self.N3]

            elif self.N == 0x1:
                # 8xy1: Set Vx = Vx OR Vy
                self.V[self.N2] |= self.V[self.N3]

            elif self.N == 0x2:
                # 8xy2: Set Vx = Vx AND Vy
                self.V[self.N2] &= self.V[self.N3]

            elif self.N == 0x3:
                # 8xy3: Set Vx = Vx XOR Vy
                self.V[self.N2] ^= self.V[self.N3]

            elif self.N == 0x4:
                # 8xy4: Add Vy to Vx, set VF = carry
                temp = self.V[self.N2] + self.V[self.N3]
                self.V[0xF] = 1 if temp > 0xFF else 0
                self.V[self.N2] = temp & 0xFF

            elif self.N == 0x5:
                # 8xy5: Subtract Vy from Vx, set VF = NOT borrow
                self.V[0xF] = 1 if self.V[self.N2] >= self.V[self.N3] else 0
                self.V[self.N2] = (self.V[self.N2] - self.V[self.N3]) & 0xFF

            elif self.N == 0x6:
                # 8xy6: Shift Vx right by 1, store LSB in VF
                self.V[0xF] = self.V[self.N2] & 0x1
                self.V[self.N2] >>= 1

            elif self.N == 0x7:
                # 8xy7: Set Vx = Vy - Vx, set VF = NOT borrow
                self.V[0xF] = 1 if self.V[self.N3] >= self.V[self.N2] else 0
                self.V[self.N2] = (self.V[self.N3] - self.V[self.N2]) & 0xFF

            elif self.N == 0xE:
                # 8xyE: Shift Vx left by 1, store MSB in VF
                self.V[0xF] = (self.V[self.N2] >> 7) & 0x1
                self.V[self.N2] = (self.V[self.N2] << 1) & 0xFF

        #else:

        # =Update PC=
        self.PC += 2

      
        

        
