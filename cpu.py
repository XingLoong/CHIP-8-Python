class CPU:

    def __init__(self):
        # start fresh
        # self.clear()

        # memory
        self.memory = [0] * 16 * 16 * 16    # 0x000 - 0xFFF

        # registers
        self.Vx = [0] * 8 * 2               # 16 8-bit register (VF usually for flags)
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

        # =decode=
        self.N1 = self.opcode >> 12
        self.N2 = (self.opcode >> 8) & 0xF
        self.N3 = (self.opcode >> 4) & 0xF
        self.N4 = self.opcode & 0xF             # mask 0xF etc
        self.NN = self.opcode & 0xFF
        self.NNN = self.opcode & 0xFFF

        # =execute=
        if self.N1 == 1:
            self.PC = self.NNN 
            return
        elif self.N1 == 6:
            self.Vx[self.N2] = (self.N3 << 4) | self.N4
        else:

        # =Update PC=
            self.PC += 2

      
        

        
