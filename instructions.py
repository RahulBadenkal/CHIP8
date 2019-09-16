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


def execute_instruction(instruction_name):
    pass

