class CPU:

    def __init__(self):
        # start fresh
        # self.clear()

        # memory
        self.memory = [0] * 16 * 16 * 16    # 0x000 - 0xFFF

        # registers
        self.Vx = [0] * 8 * 2               # 16 8-bit register (VF usually for flags)
        self.index = 0                      # index register: points to memory location
        self.delay = 0                      # delay timer, ticks own at a rate of 60Hz to 0
        self.sound = 0                      # sound timer, beeps until 0
        self.stack = []                     # 16-bit addresses for subroutines/functions
        self.PC = 0x200                     # points to current instruction in memory starts at 0x200 (usually)

        # input/keypresses
        self.key_inputs = [0] * 16          # 1 2 3 C  typical layout
                                            # 4 5 6 D
                                            # 7 8 9 E
                                            # A 0 B F
        # output/display - 64 x 32 pixel display
        self.display_buffer = [[0] * 64 for _ in range(32)]
        

        
