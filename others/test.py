import pygame

pygame.init()
import random
from collections import OrderedDict


class UInt:

    def __init__(self, size, value):
        self._max_value = 2 ** size
        self._value = value % self._max_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._value %= self._max_value


class CPU:

    def __init__(self, rom, logging=False):
        self._init_general_vars(logging)
        self._init_registers()
        self._init_gfx_ram()
        self._init_keypad()
        self._init_ram(rom)

    def _init_general_vars(self, logging):
        self._opcode = UInt(16, 0)
        self._opcode_name = "Not yet set"
        # Some opcodes do not increment the PC by two, this is set to true if
        # any of them are called.
        self._special_opcode = False
        self._cycle_count = 0
        self._logging = logging
        if self._logging:
            dir = r"C:\Users\John\Desktop\Programming\Python\CHIP-8\log.txt"
            self._log_file = open(dir, "w")

    def _init_registers(self):
        self._V = [UInt(16, 0) for x in range(16)]
        self._I = UInt(16, 0)
        self._DT = UInt(8, 0)
        self._ST = UInt(8, 0)
        self._PC = UInt(16, 512)
        # The SP starts at -1 as calling a subroutine increments the SP,
        # so starting at -1 allows it to point to the true start(index 0)
        # instead of the second element(index 1) the first time one is called.
        self._SP = UInt(8, -1)
        self._stack = [UInt(16, 0) for x in range(16)]

    def _init_gfx_ram(self):
        self.gfx_w = 64
        self.gfx_h = 32
        self.gfx_ram = [[0 for y in range(self.gfx_h)]
                        for x in range(self.gfx_w)]

    def _init_keypad(self):
        self._keypad_state = [0 for x in range(16)]

    def _update_keypad(self):
        keys = pygame.key.get_pressed()
        self._keypad_state[0] = keys[pygame.K_1]
        self._keypad_state[1] = keys[pygame.K_2]
        self._keypad_state[2] = keys[pygame.K_3]
        self._keypad_state[3] = keys[pygame.K_4]
        self._keypad_state[4] = keys[pygame.K_q]
        self._keypad_state[5] = keys[pygame.K_w]
        self._keypad_state[6] = keys[pygame.K_e]
        self._keypad_state[7] = keys[pygame.K_r]
        self._keypad_state[8] = keys[pygame.K_a]
        self._keypad_state[9] = keys[pygame.K_s]
        self._keypad_state[10] = keys[pygame.K_d]
        self._keypad_state[11] = keys[pygame.K_f]
        self._keypad_state[12] = keys[pygame.K_z]
        self._keypad_state[13] = keys[pygame.K_x]
        self._keypad_state[14] = keys[pygame.K_c]
        self._keypad_state[15] = keys[pygame.K_v]

    def _init_ram(self, rom):
        self._ram = [UInt(8, 0) for x in range(4096)]
        self._load_fontset()
        self._load_rom(rom)

    def _load_fontset(self):
        self._fontset_loc = 0
        self._fontset = [[0xF0, 0x90, 0x90, 0x90, 0xF0],  # 0
                         [0x20, 0x60, 0x20, 0x20, 0x70],  # 1
                         [0xF0, 0x10, 0xF0, 0x80, 0xF0],  # 2
                         [0xF0, 0x10, 0xF0, 0x10, 0xF0],  # 3
                         [0x90, 0x90, 0xF0, 0x10, 0x10],  # 4
                         [0xF0, 0x80, 0xF0, 0x10, 0xF0],  # 5
                         [0xF0, 0x80, 0xF0, 0x90, 0xF0],  # 6
                         [0xF0, 0x10, 0x20, 0x40, 0x40],  # 7
                         [0xF0, 0x90, 0xF0, 0x90, 0xF0],  # 8
                         [0xF0, 0x90, 0xF0, 0x10, 0xF0],  # 9
                         [0xF0, 0x90, 0xF0, 0x90, 0x90],  # A
                         [0xE0, 0x90, 0xE0, 0x90, 0xE0],  # B
                         [0xF0, 0x80, 0x80, 0x80, 0xF0],  # C
                         [0xE0, 0x90, 0x90, 0x90, 0xE0],  # D
                         [0xF0, 0x80, 0xF0, 0x80, 0xF0],  # E
                         [0xF0, 0x80, 0xF0, 0x80, 0x80]]  # F
        for sprite_count, sprite in enumerate(self._fontset):
            block = self._fontset_loc + sprite_count * 5
            for byte_count, byte in enumerate(sprite):
                sub_block = block + byte_count
                self._ram[sub_block].value = byte

    def _load_rom(self, rom):
        prog_space = len(self._ram) - self._PC.value
        rom_stream = (byte for byte in rom.read(prog_space))
        for i, byte in enumerate(rom_stream, self._PC.value):
            self._ram[i].value = byte

    def _x(self):
        return (self._opcode.value & 0x0F00) >> 8

    def _y(self):
        return (self._opcode.value & 0x00F0) >> 4

    def _kk(self):
        return self._opcode.value & 0x00FF

    def _n(self):
        return self._opcode.value & 0x000F

    def _nnn(self):
        return self._opcode.value & 0x0FFF

    def _log_state(self):
        state = OrderedDict([("opcode name", self._opcode_name),
                             ("opcode", hex(self._opcode.value)),
                             ("cycle count", self._cycle_count),
                             ("V", [reg.value for reg in self._V]),
                             ("I", self._I.value),
                             ("DT", self._DT.value),
                             ("ST", self._ST.value),
                             ("PC", self._PC.value),
                             ("SP", self._SP.value),
                             ("stack", [reg.value for reg in self._stack]),
                             ("keypad_state", [value for value in
                                               self._keypad_state])])
        for key, value in state.items():
            self._log_file.write(key)
            self._log_file.write(" : ")
            self._log_file.write(str(value))
            self._log_file.write("\n")
        self._log_file.write("\n")
        for key, value in state.items():
            print(key, ":", value)
        print("\n")

    # Instruction set starts here
    # ---------------------------
    def _CLS(self):
        """Clears the display."""
        for x in range(self.gfx_w):
            for y in range(self.gfx_h):
                self.gfx_ram[x][y] = 0

    def _RET(self):
        """Sets the program counter to the address at the top of the stack,
        then subtracts 1 from the stack pointer."""
        self._PC.value = self._stack[self._SP.value].value
        self._SP.value -= 1
        self._special_opcode = True

    def _JP_addr(self):
        """Sets the program counter to nnn."""
        self._PC.value = self._nnn()
        self._special_opcode = True

    def _CALL_addr(self):
        """Increments the stack pointer, then puts the current program counter
        on the top of the stack. The program counter is then set to nnn"""
        self._SP.value += 1
        self._stack[self._SP.value].value = self._PC.value
        self._PC.value = self._nnn()
        self._special_opcode = True

    def _SE_Vx_byte(self):
        """Compares register Vx to kk, and if they are equal, increments the
        program counter by 2."""
        if self._V[self._x()].value == self._kk():
            self._PC.value += 2

    def _SNE_Vx_byte(self):
        """Compares register Vx to kk, and if they are not equal,
        increments the program counter by 2."""
        if self._V[self._x()].value != self._kk():
            self._PC.value += 2

    def _SE_Vx_Vy(self):
        """Compares register Vx to register Vy, and if the are equal,
        increments the program counter by 2."""
        if self._V[self._x()].value == self._V[self._y()].value:
            self._PC.value += 2

    def _LD_Vx_byte(self):
        """Puts the value kk into register Vx."""
        self._V[self._x()].value = self._kk()

    def _ADD_Vx_byte(self):
        """Adds the value kk to the value of register Vx, then stores the
        result in Vx."""
        self._V[self._x()].value += self._kk()

    def _LD_Vx_Vy(self):
        """Stores the value of register Vy in register Vx."""
        self._V[self._x()].value = self._V[self._y()].value

    def _OR_Vx_Vy(self):
        """Performs a bitwise OR on the values of Vx and Vy,
        then stores the result in Vx."""
        self._V[self._x()].value |= self._V[self._y()]

    def _AND_Vx_Vy(self):
        """Performs a bitwise AND on the values of Vx and Vy,
        then stores the result in Vx."""
        self._V[self._x()].value &= self._V[self._y()].value

    def _XOR_Vx_Vy(self):
        """Performs a bitwise exclusive OR on the values of Vx and Vy,
        then stores the result in Vx."""
        self._V[self._x()].value ^= self._V[self._y()].value

    def _ADD_Vx_Vy(self):
        """The values of Vx and Vy are added together. If the result is
        greater than 8 bits(255) VF is set to 1, otherwise 0. Only the lowest
        8 bits of the result are kept, and stored in Vx."""
        result = self._V[self._x()].value + self._V[self._y()].value
        if result > 255:
            self._V[15].value = 1
        else:
            self._V[15].value = 0
        result &= 0xFF
        self._V[self._x()].value = result

    def _SUB_Vx_Vy(self):
        """If Vx > Vy, then VF is set to 1, otherwise 0. Then Vy is subtracted
        from Vx, and the result is stored in Vx."""
        if self._V[self._x()].value > self._V[self._y()].value:
            self._V[15].value = 1
        else:
            self._V[15].value = 0
        self._V[self._x()].value -= self._V[self._y()].value

    def _SHR_Vx_Vy(self):
        """If the least significant bit of Vx is 1, then VF is set to 1,
        otherwise 0. Then Vx is divided by 2."""
        if self._V[self._x()].value & 1 == 1:
            self._V[15].value = 1
        else:
            self._V[15].value = 0
        self._V[self._x()].value /= 2

    def _SUBN_Vx_Vy(self):
        """If Vy > Vx, then VF is set to 1, otherwise 0. Then Vx is subtracted
        from Vy, and the result is stored in Vx."""
        if self._V[self_y()].value > self._V[self._x()].value:
            self.__V[15].value = 1
        else:
            self.__V[15].value = 0
        result = self._V[self_y()].value - self._V[self._x()].value
        self._V[self._x()].value = result

    def _SHL_Vx_Vy(self):
        """If the most significant bit of Vx is 1, then VF is set to 1,
        otherwise 0. Then Vx is multiplied by 2."""
        if (self._V[self._x()].value & 0x80) >> 8 == 1:
            self._V[15].value = 1
        else:
            self._V[15].value = 0
        self._V[self._x()].value *= 2

    def _SNE_Vx_Vy(self):
        """The values of Vx and Vy are compared, and if they are equal,
        the program counter is incremented by 2."""
        if self._V[self._x()].value == self._V[self._y()].value:
            self._PC.value += 2

    def _LD_I_addr(self):
        """The value of register I is set to nnn."""
        self._I.value = self._nnn()

    def _JP_V0_addr(self):
        """The program counter is set to nnn plus the value of V0."""
        self._PC.value = self._nnn() + self._V[0].value

    def _RND_Vx_byte(self):
        """Generates a random number from 0 to 255, which is then ANDed with
        the value of kk. The results are stored in Vx."""
        self._V[self._x()].value = random.randrange(0, 256) & self._kk()

    def _DRW_Vx_Vy_nibble(self):
        """Reads n bytes from memory, starting at the address stored in I.
        These bytes are then displayed as sprites on screen at the coordinates
        (Vx, Vy). Sprites are XORed onto the existing screen. If this causes
        any pixels to be erased, VF is set to 1, otherwise 0. If the sprite is
        positioned so part of it is outside the coordinates of the display,
        it wraps around to the opposite side of the screen."""
        sprites = (self._ram[self._I.value + n].value for n in range(self._n()))
        for sprite_count, sprite in enumerate(sprites):
            for bit_count in range(8):
                # Extracts the bit in the place equal to variable bit_1.
                sprite_bit = (sprite >> bit_count) & 1
                # We use modular arithmetic to wrap the coordinates.
                x = (self._V[self._x()].value + (7 - bit_count)) % self.gfx_w
                y = (self._V[self._y()].value + sprite_count) % self.gfx_h
                if sprite_bit ^ self.gfx_ram[x][y] == 0:
                    self._V[15].value = 1
                else:
                    self._V[15].value = 0
                self.gfx_ram[x][y] ^= sprite_bit

    def _SKP_Vx(self):
        """Checks the keyboard, and if the key corresponding to the value of
        Vx is currently in the down position, the program counter is
        incremented by 2."""
        if self._keypad_state[self._V[self._x()].value]:
            self._PC.value += 2

    def _SKNP_Vx(self):
        """Checks the keyboard, and if the key corresponding to the value of
        Vx is currently in the up position, the program counter is
        incremented by 2."""
        if not self._keypad_state[self._V[self._x()].value]:
            self._PC.value += 2

    def _LD_Vx_DT(self):
        """The value of DT is placed into Vx."""
        self._V[self._x()].value = self._DT.value

    def _LD_Vx_K(self):
        """All execution stops until a key is pressed, then the value of that
        key is stored in Vx."""
        while True:
            for i, key in enumerate(self._keypad_state):
                if key:
                    self._V[self._x()].value = i
                    return
            self._update_keypad()

    def _LD_DT_Vx(self):
        """DT is set equal to the value of Vx."""
        self._DT.value = self._V[self._x()].value

    def _LD_ST_Vx(self):
        """ST is set equal to the value of Vx."""
        self._ST.value = self._V[self._x()].value

    def _ADD_I_Vx(self):
        """The values of I and Vx are added, and the result is stored in I."""
        self._I.value += self._V[self._x()].value

    def _LD_F_Vx(self):
        """The value of I is set to the location for the hexadecimal sprite
        corresponding to the value of Vx."""
        self._I.value = (self._V[self._x()].value * 5) + self._fontset_loc

    def _LD_B_Vx(self):
        """Takes the decimal value of Vx, and places the hundreds digit in
        memory at location I, the tens digit at location I+1, and the ones
        digit at location I+2."""
        value = self._V[self._x()].value
        for i in range(3):
            self._ram[self._I.value + i].value = int(value % 10)
            value /= 10

    def _LD_I_Vx(self):
        """Copies the values of registers V0 through Vx into memory,
        starting at address I."""
        for i in range(self._x()):
            self._ram[self._I.value + i].value = self._V[i].value

    def _LD_Vx_I(self):
        """Reads values from memory starting at I into registers V0 through
        Vx."""
        for i in range(self._x()):
            self._V[i].value = self._ram[self._I.value + i].value

    # -------------------------
    # Instruction set ends here

    def _fetch_opcode(self):
        self._opcode.value = self._ram[self._PC.value].value << 8
        self._opcode.value |= self._ram[self._PC.value + 1].value

    def _decode_opcode(self):
        if self._opcode.value & 0xFFFF == 0x00E0:
            self._opcode_name = "CLS"
            self._CLS()
        elif self._opcode.value & 0xFFFF == 0x00EE:
            self._opcode_name = "RET"
            self._RET()
        elif self._opcode.value & 0xF000 == 0x1000:
            self._opcode_name = "JP_addr"
            self._JP_addr()
        elif self._opcode.value & 0xF000 == 0x2000:
            self._opcode_name = "CALL_addr"
            self._CALL_addr()
        elif self._opcode.value & 0xF000 == 0x3000:
            self._opcode_name = "SE_Vx_byte"
            self._SE_Vx_byte()
        elif self._opcode.value & 0xF000 == 0x4000:
            self._opcode_name = "SNE_Vx_byte"
            self._SNE_Vx_byte()
        elif self._opcode.value & 0xF000 == 0x5000:
            self._opcode_name = "SE_Vx_Vy"
            self._SE_Vx_Vy()
        elif self._opcode.value & 0xF000 == 0x6000:
            self._opcode_name = "LD_Vx_byte"
            self._LD_Vx_byte()
        elif self._opcode.value & 0xF000 == 0x7000:
            self._opcode_name = "ADD_Vx_byte"
            self._ADD_Vx_byte()
        elif self._opcode.value & 0xF00F == 0x8000:
            self._opcode_name = "LD_Vx_Vy"
            self._LD_Vx_Vy()
        elif self._opcode.value & 0xF00F == 0x8001:
            self._opcode_name = "OR_Vx_Vy"
            self._OR_Vx_Vy()
        elif self._opcode.value & 0xF00F == 0x8002:
            self._opcode_name = "AND_Vx_Vy"
            self._AND_Vx_Vy()
        elif self._opcode.value & 0xF00F == 0x8003:
            self._opcode_name = "XOR_Vx_Vy"
            self._XOR_Vx_Vy()
        elif self._opcode.value & 0xF00F == 0x8004:
            self._opcode_name = "ADD_Vx_Vy"
            self._ADD_Vx_Vy()
        elif self._opcode.value & 0xF00F == 0x8005:
            self._opcode_name = "SUB_Vx_Vy"
            self._SUB_Vx_Vy()
        elif self._opcode.value & 0xF00F == 0x8006:
            self._opcode_name = "SHR_Vx_Vy"
            self._SHR_Vx_Vy()
        elif self._opcode.value & 0xF00F == 0x8007:
            self._opcode_name = "SUBN_Vx_Vy"
            self._SUBN_Vx_Vy()
        elif self._opcode.value & 0xF00F == 0x800E:
            self._opcode_name = "SHL_Vx_Vy"
            self._SHL_Vx_Vy()
        elif self._opcode.value & 0xF00F == 0x9000:
            self._opcoe_name = "SNE_Vx_Vy"
            self._SNE_Vx_Vy()
        elif self._opcode.value & 0xF000 == 0xA000:
            self._opcode_name = "LD_I_addr"
            self._LD_I_addr()
        elif self._opcode.value & 0xF000 == 0xB000:
            self._opcode_name = "JP_V0_addr"
            self._JP_V0_addr()
        elif self._opcode.value & 0xF000 == 0xC000:
            self._opcode_name = "RND_Vx_byte"
            self._RND_Vx_byte()
        elif self._opcode.value & 0xF000 == 0xD000:
            self._opcode_name = "DRW_Vx_Vy_nibble"
            self._DRW_Vx_Vy_nibble()
        elif self._opcode.value & 0xF0FF == 0xE09E:
            self._opcode_name = "SKP_Vx"
            self._SKP_Vx()
        elif self._opcode.value & 0xF0FF == 0xE0A1:
            self._opcode_name = "SKNP_Vx"
            self._SKNP_Vx()
        elif self._opcode.value & 0xF0FF == 0xF007:
            self._opcode_name = "LD_Vx_DT"
            self._LD_Vx_DT()
        elif self._opcode.value & 0xF0FF == 0xF00A:
            self._opcode_name = "LD_Vx_K"
            self._LD_Vx_K()
        elif self._opcode.value & 0xF0FF == 0xF015:
            self._opcode_name = "LD_DT_Vx"
            self._LD_DT_Vx()
        elif self._opcode.value & 0xF0FF == 0xF018:
            self._opcode_name = "LD_ST_Vx"
            self._LD_ST_Vx()
        elif self._opcode.value & 0xF0FF == 0xF01E:
            self._opcode_name = "ADD_I_Vx"
            self._ADD_I_Vx()
        elif self._opcode.value & 0xF0FF == 0xF029:
            self._opcode_name = "LD_F_Vx"
            self._LD_F_Vx()
        elif self._opcode.value & 0xF0FF == 0xF033:
            self._opcode_name = "LD_B_Vx"
            self._LD_B_Vx()
        elif self._opcode.value & 0xF0FF == 0xF055:
            self._opcode_name = "LD_I_Vx"
            self._LD_I_Vx()
        elif self._opcode.value & 0xF0FF == 0xF065:
            self._opcode_name = "LD_Vx_I"
            self._LD_Vx_I()
        else:
            self._opcode_name = "Unknown"

    def emulate_cycle(self):
        self._update_keypad()
        self._fetch_opcode()
        self._decode_opcode()
        self._cycle_count += 1
        if not self._special_opcode:
            self._PC.value += 2
        self._special_opcode = False
        if self._logging:
            self._log_state()


def main():
    dir = "/home/rahul/projects/CHIP8/ROMS/PongForOne.ch8"
    rom = open(dir, "rb")
    cpu = CPU(rom)
    res = (cpu.gfx_w, cpu.gfx_h)
    scale = 20
    scaled_res = (res[0] * scale, res[1] * scale)
    white = (255, 255, 255)
    black = (0, 0, 0)
    clock = pygame.time.Clock()
    buf = pygame.Surface(res)
    window = pygame.display.set_mode(scaled_res)
    pygame.display.set_caption("CHIP-8")

    while True:
        cpu.emulate_cycle()

        for x in range(cpu.gfx_w):
            for y in range(cpu.gfx_h):
                if cpu.gfx_ram[x][y] == 1:
                    buf.set_at((x, y), white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.transform.scale(buf, scaled_res, window)
        buf.fill(black)
        pygame.display.flip()
        clock.tick()


if __name__ == "__main__":
    main()

