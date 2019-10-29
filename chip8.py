import random

class Chip8State:
    def __init__(self):
        # ################## Registers ########################## #
        # 16 General purpose registers, each is 1 byte, denoted by V0 to VF
        self.gen_regs = None  # = [0x00]*16
        self.index_reg = None  # 1 Index Register (2 bytes long)
        # 1 Program Counter Register, points to the currently executing address in RAM (2 bytes long)
        self.pc_reg = None
        # 1 Stack Pointer points to the topmost level of the stack (Stack is reserved in main memory). 2 bytes long
        self.sp_reg = None

        # ##################### Timers ########################## #
        self.delay_timer = None  # 1 Delay register (1 bytes long)
        self.sound_timer = None  # 1 Sound Register (1 bytes long)

        # TODO: Replace Additional variables with the actual Chip8 Implementation
        # ############### Additional variables ################## #
        # I couldn't figure out how the actual chip8 implements the below variables, so I just created dummy variables
        # in python to emulate them. These are (I am guessing) stored somewhere on the memory but to make things easier
        # I created python variables (outside of the main memory) and stored them there
        self.stack = None  # 16 level deep, each 2 bytes so total 16*2 = 32 bytes
        self.keypad = None  # 16 keys (0x0 to 0xF) each 1 bit so total 16*1 = 16bits = 2bytes
        # Screen size = 64x32 pixels (each pixel is either 0(black) or 1(white))
        # Total size (in bytes) required = 64*32 bits = 64*32/8 bytes = 256 bytes
        self.width = None
        self.height = None
        self.display = None
        # Predefined fonts (0-F) for easy displaying of numbers
        self.fontset_loc = None
        self.fontset = None  # 16 different fonts, each 5 bytes long so total 16*5 = 80 bytes
        # Currently read opcode
        self.opcode = None

        # ##################### Memory ########################## #
        self.memory = None  # 4096 bytes

        # Total Memory: 0-4095 (0x000 to 0xFFF) i.e 4096 bytes
        #   - 0-511 (0x000 to 0x1FF) i.e 512 bytes reserved for Chip8 Interpreter but since in our case python is the
        #   interpreter, we are free to use this space.
        #       - 0-79 (0x000 to 0x050) i.e 80 bytes to store fontset
        #   - 512-3743 (0x200 to 0xE9F) i.e 3232 bytes to store the program (the one we want to execute) data
        #   - 3744 -3839 (0xEA0 to 0xEFF) i.e 96 bytes to store the call stack, internal use, and other variables.
        #       - 3744 - 3775 (0xEA0 to EBF) i.e 32 bytes for call stack
        #   - 3840-4095 (0xF00 to 0xFFF) i.e 256 bytes for display

    def initialise(self):
        self.gen_regs = [0]*16
        self.index_reg = 0
        self.pc_reg = 512
        self.sp_reg = -1

        self.stack = [0]*16

        self.memory = [0] * 4096

        self.keypad = [0]*16

        self.delay_timer = 0
        self.sound_timer = 0

        self.width, self.height = 64, 32  # in pixels
        self.display = [[0]*self.height for _ in range(self.width)]

        self.fontset_loc = 0
        self.fontset = [[0xF0, 0x90, 0x90, 0x90, 0xF0],  # 0
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
        for sprite_count, sprite in enumerate(self.fontset):
            block = self.fontset_loc + sprite_count * 5
            for byte_count, byte in enumerate(sprite):
                sub_block = block + byte_count
                self.memory[sub_block] = byte

    def load_rom(self, rom):
        self.memory[self.pc_reg: self.pc_reg + len(rom)] = rom

    def cpu_cycle(self):
        """Fetches, decodes and executes the instruction at the memory address pointed by the pc register

        """
        # Fetch
        # All instructions are 2 bytes long. Read 1 byte. Read the next byte. Join them
        self.opcode = (self.memory[self.pc_reg] << 8) | self.memory[self.pc_reg + 1]

        # Decode
        instruction_name = self.get_instruction_name(self.opcode)
        print('{}: {}, {}'.format(self.pc_reg, hex(self.opcode), instruction_name))

        # Execute instruction and move pc
        self.execute_instruction(instruction_name)

    @staticmethod
    def get_instruction_name(opcode):
        # Checking which one of 35 known instructions does the opcode belong to
        if opcode == 0x00E0:
            inst_name = 'CLS'
        elif opcode == 0x00EE:
            inst_name = 'RET'
        elif opcode & 0xF000 == 0x0000:
            inst_name = 'SYS'
        elif opcode & 0xF000 == 0x1000:
            inst_name = 'JP'
        elif opcode & 0xF000 == 0x2000:
            inst_name = 'CALL'
        elif opcode & 0xF000 == 0x3000:
            inst_name = 'SE_Vx'
        elif opcode & 0xF000 == 0x4000:
            inst_name = 'SNE_Vx'
        elif opcode & 0xF00F == 0x5000:
            inst_name = 'SE_Vy_Vy'
        elif opcode & 0xF000 == 0x6000:
            inst_name = 'LD_Vx'
        elif opcode & 0xF000 == 0x7000:
            inst_name = 'ADD_Vx'
        elif opcode & 0xF00F == 0x8000:
            inst_name = 'LD_Vx_Vy'
        elif opcode & 0xF00F == 0x8001:
            inst_name = 'OR_Vx_Vy'
        elif opcode & 0xF00F == 0x8002:
            inst_name = 'AND_Vx_Vy'
        elif opcode & 0xF00F == 0x8003:
            inst_name = 'XOR_Vx_Vy'
        elif opcode & 0xF00F == 0x8004:
            inst_name = 'ADD_Vx_Vy'
        elif opcode & 0xF00F == 0x8005:
            inst_name = 'SUB_Vx_Vy'
        elif opcode & 0xF00F == 0x8006:
            inst_name = 'SHR_Vx_Vy'
        elif opcode & 0xF00F == 0x8007:
            inst_name = 'SUBN_Vx_Vy'
        elif opcode & 0xF00F == 0x800E:
            inst_name = 'SHL_Vx_Vy'
        elif opcode & 0xF00F == 0x9000:
            inst_name = 'SNE_Vx_Vy'
        elif opcode & 0xF000 == 0xA000:
            inst_name = 'LD_I'
        elif opcode & 0xF000 == 0xB000:
            inst_name = 'JP_V0'
        elif opcode & 0xF000 == 0xC000:
            inst_name = 'RND_Vx'
        elif opcode & 0xF000 == 0xD000:
            inst_name = 'DRW_Vx_Vy'
        elif opcode & 0xF0FF == 0xE09E:
            inst_name = 'SKP_Vx'
        elif opcode & 0xF0FF == 0xE0A1:
            inst_name = 'SKNP_Vx'
        elif opcode & 0xF0FF == 0xF007:
            inst_name = 'LD_Vx_DT'
        elif opcode & 0xF0FF == 0xF00A:
            inst_name = 'LD_Vx_K'
        elif opcode & 0xF0FF == 0xF015:
            inst_name = 'LD_DT_Vx'
        elif opcode & 0xF0FF == 0xF018:
            inst_name = 'LD_ST_Vx'
        elif opcode & 0xF0FF == 0xF01E:
            inst_name = 'ADD_I_Vx'
        elif opcode & 0xF0FF == 0xF029:
            inst_name = 'LD_F_Vx'
        elif opcode & 0xF0FF == 0xF033:
            inst_name = 'LD_B_Vx'
        elif opcode & 0xF0FF == 0xF055:
            inst_name = 'LD_I_Vx'
        elif opcode & 0xF0FF == 0xF065:
            inst_name = 'LD_Vx_I'
        else:
            raise ValueError('opcode {} is not a valid instruction'.format(opcode))

        return inst_name

    def execute_instruction(self, instruction_name):
        # Helpers
        # default bitwise right shift is arithmetic but we want logical but since we know we only deal with
        # unsigned numbers there is no problem (as for unsigned numbers arithmetic and logical bitwise right
        # shifts are the same)
        def get_x():
            # opcode is of form 0x6xkk. x is the 2nd from right (in hex representation)
            return (self.opcode & 0x0F00) >> 8

        def get_y():
            # opcode is of form 0x5xy0. y is the 3nd from right (in hex representation)
            return (self.opcode & 0x00F0) >> 4

        # Instruction definitions
        def _cls():
            for i in range(len(self.display)):
                self.display[i] = 0
            self.pc_reg += 2
            return

        def _ret():
            # Not incrementing pc by 2
            self.pc_reg = self.stack[self.sp_reg]
            self.sp_reg -= 1
            return

        def _sys():
            # TODO: Implement this
            return

        def _jp():
            # Not incrementing pc by 2
            self.pc_reg = self.opcode & 0x0FFF
            return

        def _call():
            # Not incrementing pc by 2
            self.sp_reg += 1
            self.stack[self.sp_reg] = self.pc_reg + 2
            self.pc_reg = self.opcode & 0x0FFF
            return

        def _se_vx():
            if self.gen_regs[get_x()] == self.opcode & 0x00FF:
                self.pc_reg += 2
            self.pc_reg += 2
            return

        def _sne_vx():
            if self.gen_regs[get_x()] != self.opcode & 0x00FF:
                self.pc_reg += 2
            self.pc_reg += 2
            return

        def _se_vx_vy():
            if self.gen_regs[get_x()] == self.gen_regs[get_y()]:
                self.pc_reg += 2
            self.pc_reg += 2
            return

        def _ld_vx():
            self.gen_regs[get_x()] = self.opcode & 0x00FF
            self.pc_reg += 2
            return

        def _add_vx():
            x_pos = get_x()
            a = self.gen_regs[x_pos] + self.opcode & 0x00FF
            a = a & 0xFF  # Making sure it remains 1 bytes long (as every gen_reg is 1 byte long)
            self.gen_regs[x_pos] = a
            self.pc_reg += 2
            return

        def _ld_vx_vy():
            self.gen_regs[get_x()] = self.gen_regs[get_y()]
            self.pc_reg += 2
            return

        def _or_vx_vy():
            x_pos = get_x()
            y_pos = get_y()
            self.gen_regs[x_pos] = self.gen_regs[x_pos] | self.gen_regs[y_pos]
            self.pc_reg += 2
            return

        def _and_vx_vy():
            x_pos = get_x()
            y_pos = get_y()
            self.gen_regs[x_pos] = self.gen_regs[x_pos] & self.gen_regs[y_pos]
            self.pc_reg += 2
            return

        def _xor_vx_vy():
            x_pos = get_x()
            y_pos = get_y()
            self.gen_regs[x_pos] = self.gen_regs[x_pos] ^ self.gen_regs[y_pos]
            self.pc_reg += 2
            return

        def _add_vx_vy():
            x_pos = get_x()
            y_pos = get_y()
            a = self.gen_regs[x_pos] + self.gen_regs[y_pos]
            add = a & 0xFF  # Making sure it remains 1 bytes long (as every gen_reg is 1 byte long)
            carry = 0 if a == add else 1
            self.gen_regs[x_pos] = add
            self.gen_regs[15] = carry
            self.pc_reg += 2
            return

        def _sub_vx_vy():
            x_pos = get_x()
            y_pos = get_y()
            if self.gen_regs[x_pos] > self.gen_regs[y_pos]:
                self.gen_regs[15] = 1
            else:
                self.gen_regs[15] = 0
            self.gen_regs[x_pos] -= self.gen_regs[y_pos]
            self.pc_reg += 2
            return

        def _shr_vx_vy():
            x_pos = get_x()
            self.gen_regs[15] = self.gen_regs[x_pos] & 0b1
            self.gen_regs[x_pos] = self.gen_regs[x_pos] >> 1
            self.pc_reg += 2
            return

        def _subn_vx_vy():
            x_pos = get_x()
            y_pos = get_y()
            if self.gen_regs[y_pos] > self.gen_regs[x_pos]:
                self.gen_regs[15] = 1
            else:
                self.gen_regs[15] = 0
            self.gen_regs[x_pos] = self.gen_regs[y_pos] - self.gen_regs[x_pos]
            self.pc_reg += 2
            return

        def _shl_vx_vy():
            x_pos = get_x()
            self.gen_regs[15] = self.gen_regs[x_pos] & 0b1
            self.gen_regs[x_pos] = self.gen_regs[x_pos] << 1
            self.pc_reg += 2
            return

        def _sne_vx_vy():
            if self.gen_regs[get_x()] != self.gen_regs[get_y()]:
                self.pc_reg += 2
            self.pc_reg += 2
            return

        def _ld_i():
            self.index_reg = self.opcode & 0x0FFF
            self.pc_reg += 2
            return

        def _jp_v0():
            # Not incrementing pc by 2
            self.pc_reg = self.opcode & 0x0FFF + self.gen_regs[0]
            return

        def _rnd_vx():
            rand = random.randint(0, 256)
            self.gen_regs[get_x()] = rand & (self.opcode & 0x00FF)
            self.pc_reg += 2
            return

        def _drw_vx_vy():
            # TODO: Understand This
            x_reg_pos = get_x()
            y_reg_pos = get_y()
            nibble = self.opcode & 0x000F
            sprites = [each for each in self.memory[self.index_reg: self.index_reg + nibble]]
            for sprite_count, sprite in enumerate(sprites):
                for bit_count in range(8):
                    sprite_bit = (sprite >> bit_count) & 1
                    x = (self.gen_regs[x_reg_pos] + (7-bit_count)) % self.width
                    y = (self.gen_regs[y_reg_pos] + sprite_count) % self.height
                    if sprite_bit ^ self.display[x][y] == 0:
                        self.gen_regs[15] = 1
                    else:
                        self.gen_regs[15] = 0
                    self.display[x][y] ^= sprite_bit
            self.pc_reg += 2
            return

        def _skp_vx():
            if self.keypad[self.gen_regs[get_x()]] == 1:
                self.pc_reg += 2
            self.pc_reg += 2
            return

        def _sknp_vx():
            if self.keypad[self.gen_regs[get_x()]] != 1:
                self.pc_reg += 2
            self.pc_reg += 2
            return

        def _ld_vx_dt():
            self.gen_regs[get_x()] = self.delay_timer
            self.pc_reg += 2
            return

        def _ld_vx_k():
            loop = True
            while loop is True:
                for each in self.keypad:
                    if each == 1:
                        loop = False
            self.pc_reg += 2
            return

        def _ld_dt_vx():
            self.delay_timer = self.gen_regs[get_x()]
            self.pc_reg += 2
            return

        def _ld_st_vx():
            self.sound_timer = self.gen_regs[get_x()]
            self.pc_reg += 2
            return

        def _add_i_vx():
            a = self.index_reg + self.gen_regs[get_x()]
            self.index_reg = a & 0xFFFF  # Making sure it remains 2 bytes long as index_reg is 2 bytes long
            self.pc_reg += 2
            return

        def _ld_f_vx():
            self.index_reg = self.fontset_loc + (self.gen_regs[get_x()])*5
            self.pc_reg += 2
            return

        def _ld_b_vx():
            vx = self.gen_regs[get_x()]
            self.memory[self.index_reg] = (vx // 100) % 10
            self.memory[self.index_reg + 1] = (vx // 10) % 10
            self.memory[self.index_reg + 2] = vx % 10
            self.pc_reg += 2
            return

        def _ld_i_vx():
            x_pos = get_x()
            for i in range(x_pos + 1):
                self.memory[self.index_reg + i] = self.gen_regs[i]
            self.pc_reg += 2
            return

        def _ld_vx_i():
            x_pos = get_x()
            for i in range(x_pos + 1):
                self.gen_regs[i] = self.memory[self.index_reg + i]
            self.pc_reg += 2
            return

        instruction_map = {
            'CLS': _cls,
            'RET': _ret,
            'SYS': _sys,
            'JP': _jp,
            'CALL': _call,
            'SE_Vx': _se_vx,
            'SNE_Vx': _sne_vx,
            'SE_Vy_Vy': _se_vx_vy,
            'LD_Vx': _ld_vx,
            'ADD_Vx': _add_vx,
            'LD_Vx_Vy': _ld_vx_vy,
            'OR_Vx_Vy': _or_vx_vy,
            'AND_Vx_Vy': _and_vx_vy,
            'XOR_Vx_Vy': _xor_vx_vy,
            'ADD_Vx_Vy': _add_vx_vy,
            'SUB_Vx_Vy': _sub_vx_vy,
            'SHR_Vx_Vy': _shr_vx_vy,
            'SUBN_Vx_Vy': _subn_vx_vy,
            'SHL_Vx_Vy': _shl_vx_vy,
            'SNE_Vx_Vy': _sne_vx_vy,
            'LD_I': _ld_i,
            'JP_V0': _jp_v0,
            'RND_Vx': _rnd_vx,
            'DRW_Vx_Vy': _drw_vx_vy,
            'SKP_Vx': _skp_vx,
            'SKNP_Vx': _sknp_vx,
            'LD_Vx_DT': _ld_vx_dt,
            'LD_Vx_K': _ld_vx_k,
            'LD_DT_Vx': _ld_dt_vx,
            'LD_ST_Vx': _ld_st_vx,
            'ADD_I_Vx': _add_i_vx,
            'LD_F_Vx': _ld_f_vx,
            'LD_B_Vx': _ld_b_vx,
            'LD_I_Vx': _ld_i_vx,
            'LD_Vx_I': _ld_vx_i,
        }

        instruction_map[instruction_name]()
        return
