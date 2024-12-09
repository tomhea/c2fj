from typing import TextIO


RV_LUI = 0b0110111
RV_AUIPC = 0b0010111
RV_JAL = 0b1101111
RV_JALR = 0b1100111

RV_B = 0b1100011
RV_BEQ = 0b000
RV_BNE = 0b001
RV_BLT = 0b100
RV_BGE = 0b101
RV_BLTU = 0b110
RV_BGEU = 0b111

RV_L = 0b0000011
RV_LB = 0b000
RV_LH = 0b001
RV_LW = 0b010
RV_LBU = 0b100
RV_LHU = 0b101

RV_S = 0b0100011  # TODO implement
RV_SB = 0b000
RV_SH = 0b001
RV_SW = 0b010

RV_ALU_IMM = 0b0010011  # TODO 9 ALU ops with immediate

RV_ALU = 0b0110011  # TODO 10 ALU ops

RV_FENCE = 0b000111  # TODO implement. Single op in ISA.

RB_CALL = 0b1110011  # TODO implement. ECALL is I=0, EBREAK is I=1 (everything else is 0)


_WRITE_IMMEDIATE = 2
_READ_IMMEDIATE = 6
_EXIT_IMMEDIATE = 10


global pc_changed


def invalid_exception(op: int) -> str:
    return ''  # TODO


def sign_extend(constant: int, bit_width: int) -> int:
    if constant & (1 << (bit_width - 1)):
        return constant - (1 << bit_width)
    return constant


def fj_hex(constant: int) -> str:
    if constant < 0:
        return f'(0 - {hex(abs(constant))})'
    return hex(constant)


def register_name(register_index: int) -> str:
    """
    @param register_index: the 5 lsb will be used.
    """
    return f'.regs.x{register_index & 0x1f}'


def get_hex_comment(op: int) -> str:
    return f'// op 0x{op:08x}'


def r_type(macro_name: str, op: int) -> str:
    return f'    .{macro_name} {register_name(op >> 7)}, {register_name(op >> 15)}, {register_name(op >> 20)}'\
           f'\t\t{get_hex_comment(op)}\n'


def i_type(macro_name: str, op: int) -> str:
    imm = sign_extend(op >> 20, 12)
    rs1 = (op >> 15) & 0x1f
    rd = (op >> 7) & 0x1f

    return f'    .{macro_name} {register_name(rd)}, {register_name(rs1)}, {fj_hex(imm)}\n'


def jalr_op(op: int, addr: int) -> str:
    imm = sign_extend(op >> 20, 12)
    rs1 = (op >> 15) & 0x1f
    rd = (op >> 7) & 0x1f

    global pc_changed
    pc_changed = True

    return f'    .jalr {rd}, {register_name(rs1)}, {fj_hex(imm)}, {addr}\n'


def s_type(macro_name: str, op: int) -> str:
    imm11_5 = op >> 25
    imm4_0 = (op >> 7) & 0x1f
    imm = (imm11_5 << 5) | (imm4_0 << 0)
    imm = sign_extend(imm, 12)
    return f'    .{macro_name} {register_name(op >> 15)}, {register_name(op >> 20)}, {fj_hex(imm)}' \
           f'\t\t{get_hex_comment(op)}\n'


def b_type(macro_name: str, op: int, addr: int) -> str:
    imm12 = op >> 31
    imm10_5 = (op >> 25) & 0x3f
    imm4_1 = (op >> 8) & 0xf
    imm11 = (op >> 7) & 0x1
    imm = (imm12 << 12) | (imm10_5 << 5) | (imm4_1 << 1) | (imm11 << 11)
    imm = sign_extend(imm, 13)

    rs1 = (op >> 15) & 0x1f
    rs2 = (op >> 20) & 0x1f

    global pc_changed
    pc_changed = True

    return f'    .{macro_name} {register_name(rs1)}, {register_name(rs2)}, {fj_hex(imm)}, {addr}\n'


def u_type(op: int) -> [int, int]:
    imm = sign_extend(op & 0xfffff000, 32)
    rd = (op >> 7) & 0x1f
    return imm, rd


def lui_op(op: int) -> str:
    imm, rd = u_type(op)
    return f'    .lui {rd}, {fj_hex(imm)}\n'


def auipc_op(op: int, addr: int) -> str:
    imm, rd = u_type(op)
    return f'    .auipc {rd}, {fj_hex(imm)}, {addr}\n'


def j_type(macro_name: str, op: int, addr: int) -> str:
    imm20 = op >> 31
    imm10_1 = (op >> 21) & 0x3ff
    imm11 = (op >> 20) & 0x1
    imm_19_12 = (op >> 12) & 0xff
    imm = (imm20 << 20) | (imm10_1 << 1) | (imm11 << 11) | (imm_19_12 << 12)
    imm = sign_extend(imm, 21)

    rd = (op >> 7) & 0x1f

    global pc_changed

    if imm % 4 == 2:
        if imm == _WRITE_IMMEDIATE:
            return f'    .syscall.write_byte {rd}\n'
        elif imm == _READ_IMMEDIATE:
            return f'    .syscall.read_byte {rd}\n'
        elif imm == _EXIT_IMMEDIATE:
            pc_changed = True
            return f'    .syscall.exit {rd}\n'
        else:
            return invalid_exception(op)

    pc_changed = True
    return f'    .{macro_name} {rd}, {fj_hex(imm)}, {addr}\n'


def write_op(ops_file: TextIO, full_op: int, addr: int) -> None:
    ops_file.write('    hex.zero .HLEN, .regs.zero\n')

    opcode = full_op & 0x7f
    funct3 = (full_op >> 12) & 7
    funct7 = full_op >> 25

    global pc_changed
    pc_changed = False

    # TODO verify instruction encoding go right

    if opcode == RV_LUI:
        ops_file.write(lui_op(full_op))
    elif opcode == RV_AUIPC:
        ops_file.write(auipc_op(full_op, addr))
    elif opcode == RV_JAL:
        ops_file.write(j_type('jal', full_op, addr))
    elif opcode == RV_JALR:
        if funct3 != 0:
            ops_file.write(f'    // ERROR - bad funct3 at jalr op - 0x{full_op:08x}\n')
        else:
            ops_file.write(jalr_op(full_op, addr))

    elif opcode == RV_B:
        if funct3 == RV_BEQ:
            ops_file.write(b_type('beq', full_op, addr))
        elif funct3 == RV_BNE:
            ops_file.write(b_type('bne', full_op, addr))
        elif funct3 == RV_BLT:
            ops_file.write(b_type('blt', full_op, addr))
        elif funct3 == RV_BGE:
            ops_file.write(b_type('bge', full_op, addr))
        elif funct3 == RV_BLTU:
            ops_file.write(b_type('bltu', full_op, addr))
        elif funct3 == RV_BGEU:
            ops_file.write(b_type('bgeu', full_op, addr))

    elif opcode == RV_L:
        if funct3 == RV_LB:
            ops_file.write(i_type('lb', full_op))
        elif funct3 == RV_LH:
            ops_file.write(i_type('lh', full_op))
        elif funct3 == RV_LW:
            ops_file.write(i_type('lw', full_op))
        elif funct3 == RV_LBU:
            ops_file.write(i_type('lbu', full_op))
        elif funct3 == RV_LHU:
            ops_file.write(i_type('lhu', full_op))

    else:
        ops_file.write(f'    // TODO not-implemented op 0x{full_op:08x}\n')
        # TODO real ops here.

    if not pc_changed:
        ops_file.write(f'    .inc_pc 0x{addr:08x}\n')

    ops_file.write('\n')
