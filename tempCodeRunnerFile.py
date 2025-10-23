from cpu import CPU

chip8 = CPU()
print("Memory size:", len(chip8.memory))
print("Display size:", len(chip8.display_buffer), "rows x", len(chip8.display_buffer[0]), "cols")
print("Program Counter:", hex(chip8.PC))