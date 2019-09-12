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
        self.display = None
        # Predefined fonts (0-F) for easy displaying of numbers
        self.fontset = None  # 16 different fonts, each 5 bytes long so total 16*5 = 80 bytes

        # ##################### Memory ########################## #
        self.memory = None  # 4096 bytes

        # Total Memory: 0-4095 (0x000 to 0xFFF) i.e 4096 bytes
        #   - 0-511 (0x000 to 0x1FF) i.e 512 bytes reserved for Chip8 Interpreter but since in our case python is the
        #   interpreter, we are free to use this space.
        #       - 0-79 (0x000 to 0x050) i.e 80 bytes to store fontset
        #   - 512-3743 (0x000 to 0xE9F) i.e 3232 bytes to store the program (the one we want to execute) data
        #   - 3744 -3839 (0xEA0 to 0xEFF) i.e 96 bytes to store the call stack, internal use, and other variables.
        #       - 3744 - 3775 (0xEA0 to EBF) i.e 32 bytes for call stack
        #   - 3840-4095 (0xF00 to 0xFFF) i.e 256 bytes for display

    def initialise(self):
        pass

    def load_rom(self, memory, rom):
        pass

    def emulate_cycle(self, memory):
        """Fetches, decodes and executes the instruction at the memory address pointed by the pc register"""
        pass
