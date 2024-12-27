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

RV_S = 0b0100011
RV_SB = 0b000
RV_SH = 0b001
RV_SW = 0b010

RV_ALU_IMM = 0b0010011
RV_ADDI = 0b000
RV_SLTI = 0b010
RV_SLTIU = 0b011
RV_XORI = 0b100
RV_ORI = 0b110
RV_ANDI = 0b111
RV_SLLI = 0b001
RV_SRI = 0b101
RV_SLLI_FUNCT7 = 0b0000000
RV_SRLI_FUNCT7 = 0b0000000
RV_SRAI_FUNCT7 = 0b0100000

RV_ALU = 0b0110011
RV_ADD_SUB = 0b000
RV_SLL = 0b001
RV_SLT = 0b010
RV_SLTU = 0b011
RV_XOR = 0b100
RV_SR = 0b101
RV_OR = 0b110
RV_AND = 0b111
RV_ADD_FUNCT7 = 0b0000000
RV_SUB_FUNCT7 = 0b0100000
RV_SLL_FUNCT7 = 0b0000000
RV_SLT_FUNCT7 = 0b0000000
RV_SLTU_FUNCT7 = 0b0000000
RV_XOR_FUNCT7 = 0b0000000
RV_SRL_FUNCT7 = 0b0000000
RV_SRA_FUNCT7 = 0b0100000
RV_OR_FUNCT7 = 0b0000000
RV_AND_FUNCT7 = 0b0000000

RV32M_FUNCT7 = 0b0000001  # TODO implement the 8 mul/div/rem ops from RV32M.

RV_FENCE = 0b0001111
RV_FENCE_FUNCT3 = 0b000

RV_CALL = 0b1110011
RV_ECALL_FULL_OP = RV_CALL
RV_EBREAK_FULL_OP = (1 << 20) | RV_CALL


_WRITE_IMMEDIATE = 2
_READ_IMMEDIATE = 6
_EXIT_IMMEDIATE = 10
_SBRK_IMMEDIATE = 14
_DEBUG_REGISTERS_IMMEDIATE = 18


global pc_changed


class InvalidOpcode(ValueError):
    pass


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


def mov_to_rs1(register_index: int) -> str:
    """
    @param register_index: the 5 lsb will be used.
    """
    return f'.mov_x{register_index & 0x1f}_to_rs1'


def xor_to_rs2(register_index: int) -> str:
    """
    @param register_index: the 5 lsb will be used.
    """
    return f'.xor_x{register_index & 0x1f}_to_rs2'


def mov_rs1_to(register_index: int) -> str:
    """
    @param register_index: the 5 lsb will be used.
    """
    return f'.mov_rs1_to_x{register_index & 0x1f}'


def mov_rd_to(register_index: int) -> str:
    """
    @param register_index: the 5 lsb will be used.
    """
    return f'.mov_rd_to_x{register_index & 0x1f}'


def get_hex_comment(op: int) -> str:
    return f'// op 0x{op:08x}'


def r_type(macro_name: str, op: int, dst_is_rs1: bool = True) -> str:
    rd = (op >> 7) & 0x1f
    rs1 = (op >> 15) & 0x1f
    rs2 = (op >> 20) & 0x1f

    mov_to_dst_reg = mov_rs1_to(rd) if dst_is_rs1 else mov_rd_to(rd)
    return f'    .{macro_name} {mov_to_dst_reg}, {mov_to_rs1(rs1)}, {xor_to_rs2(rs2)}\n'


def i_type(macro_name: str, op: int, dst_is_rs1: bool = True) -> str:
    imm = sign_extend(op >> 20, 12)
    rs1 = (op >> 15) & 0x1f
    rd = (op >> 7) & 0x1f

    mov_to_dst_reg = mov_rs1_to(rd) if dst_is_rs1 else mov_rd_to(rd)

    if macro_name in ['addi', 'xori', 'ori', 'andi', 'slti', 'sltiu']:
        return f'    .{macro_name} {mov_to_dst_reg}, {mov_to_rs1(rs1)}, {fj_hex(imm)}\n'

    return f'    .{macro_name} {register_name(rd)}, {register_name(rs1)}, {fj_hex(imm)}\n'


def shift_imm_op(macro_name: str, op: int) -> str:
    shift_const = (op >> 20) & 0x1f
    rs1 = (op >> 15) & 0x1f
    rd = (op >> 7) & 0x1f

    return f'    .{macro_name} {register_name(rd)}, {register_name(rs1)}, {fj_hex(shift_const)}\n'


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

    rs1 = (op >> 15) & 0x1f
    rs2 = (op >> 20) & 0x1f

    return f'    .{macro_name} {register_name(rs1)}, {register_name(rs2)}, {fj_hex(imm)}\n'


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
            return f'    .syscall.write_byte {register_name(rd)}\n'
        elif imm == _READ_IMMEDIATE:
            return f'    .syscall.read_byte {register_name(rd)}\n'
        elif imm == _EXIT_IMMEDIATE:
            pc_changed = True
            return f'    .syscall.exit {register_name(rd)}\n'
        elif imm == _SBRK_IMMEDIATE:
            return f'    .syscall.sbrk {register_name(rd)}\n'
        elif imm == _DEBUG_REGISTERS_IMMEDIATE:
            return f'    .syscall.debug_print_regs\n'
        else:
            raise InvalidOpcode(f"Bad imm offset in j-type op: 0x{op:08x} (address 0x{addr:08x}).")

    pc_changed = True
    return f'    .{macro_name} {rd}, {fj_hex(imm)}, {addr}\n'


def write_op(ops_file: TextIO, full_op: int, addr: int) -> None:
    ops_file.write('    hex.zero .HLEN, .regs.zero\n')

    opcode = full_op & 0x7f
    funct3 = (full_op >> 12) & 7
    funct7 = full_op >> 25

    global pc_changed
    pc_changed = False

    if opcode == RV_LUI:
        ops_file.write(lui_op(full_op))
    elif opcode == RV_AUIPC:
        ops_file.write(auipc_op(full_op, addr))
    elif opcode == RV_JAL:
        ops_file.write(j_type('jal', full_op, addr))
    elif opcode == RV_JALR:
        if funct3 != 0:
            raise InvalidOpcode(f"bad funct3 at jalr op: 0x{full_op:08x} (address 0x{addr:08x}).")
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
        else:
            raise InvalidOpcode(f"bad funct3 at branch op: 0x{full_op:08x} (address 0x{addr:08x}).")

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
            raise InvalidOpcode(f"bad funct3 at load op: 0x{full_op:08x} (address 0x{addr:08x}).")

    elif opcode == RV_S:
        if funct3 == RV_SB:
            ops_file.write(s_type('sb', full_op))
        elif funct3 == RV_SH:
            ops_file.write(s_type('sh', full_op))
        elif funct3 == RV_SW:
            ops_file.write(s_type('sw', full_op))
        else:
            raise InvalidOpcode(f"bad funct3 at store op: 0x{full_op:08x} (address 0x{addr:08x}).")

    elif opcode == RV_ALU_IMM:
        if funct3 == RV_ADDI:
            ops_file.write(i_type('addi', full_op))
        elif funct3 == RV_SLTI:
            ops_file.write(i_type('slti', full_op, dst_is_rs1=False))
        elif funct3 == RV_SLTIU:
            ops_file.write(i_type('sltiu', full_op, dst_is_rs1=False))
        elif funct3 == RV_XORI:
            ops_file.write(i_type('xori', full_op))
        elif funct3 == RV_ORI:
            ops_file.write(i_type('ori', full_op))
        elif funct3 == RV_ANDI:
            ops_file.write(i_type('andi', full_op))
        elif funct3 == RV_SLLI and funct7 == RV_SLLI_FUNCT7:
            ops_file.write(shift_imm_op('slli', full_op))
        elif funct3 == RV_SRI and funct7 == RV_SRLI_FUNCT7:
            ops_file.write(shift_imm_op('srli', full_op))
        elif funct3 == RV_SRI and funct7 == RV_SRAI_FUNCT7:
            ops_file.write(shift_imm_op('srai', full_op))
        else:
            raise InvalidOpcode(f"bad funct3/funct7 at alu_imm op: 0x{full_op:08x} (address 0x{addr:08x}).")

    elif opcode == RV_ALU:
        if funct3 == RV_ADD_SUB and funct7 == RV_ADD_FUNCT7:
            ops_file.write(r_type('add', full_op))
        elif funct3 == RV_ADD_SUB and funct7 == RV_SUB_FUNCT7:
            ops_file.write(r_type('sub', full_op))
        elif funct3 == RV_XOR and funct7 == RV_XOR_FUNCT7:
            ops_file.write(r_type('xor', full_op))
        elif funct3 == RV_OR and funct7 == RV_OR_FUNCT7:
            ops_file.write(r_type('or', full_op))
        elif funct3 == RV_AND and funct7 == RV_AND_FUNCT7:
            ops_file.write(r_type('and', full_op))
        elif funct3 == RV_SLT and funct7 == RV_SLT_FUNCT7:
            ops_file.write(r_type('slt', full_op, dst_is_rs1=False))
        elif funct3 == RV_SLTU and funct7 == RV_SLTU_FUNCT7:
            ops_file.write(r_type('sltu', full_op, dst_is_rs1=False))
        elif funct3 == RV_SLL and funct7 == RV_SLL_FUNCT7:
            ops_file.write(r_type('sll', full_op))
        elif funct3 == RV_SR and funct7 == RV_SRL_FUNCT7:
            ops_file.write(r_type('srl', full_op))
        elif funct3 == RV_SR and funct7 == RV_SRA_FUNCT7:
            ops_file.write(r_type('sra', full_op))
        else:
            raise InvalidOpcode(f"bad funct3/funct7 at alu op: 0x{full_op:08x} (address 0x{addr:08x}).")

    elif opcode == RV_FENCE:
        if funct3 == RV_FENCE_FUNCT3:
            raise InvalidOpcode(f"C2fj doesn't support fence ops: encoding=0x{full_op:08x} (address 0x{addr:08x}).")
        else:
            raise InvalidOpcode(f"bad funct3 at fence op: 0x{full_op:08x} (address 0x{addr:08x}).")

    elif opcode == RV_CALL:
        if full_op == RV_ECALL_FULL_OP:
            raise InvalidOpcode(f"C2fj doesn't support ecall ops (newlib shouldn't have produced it) (address 0x{addr:08x}).")
        elif full_op == RV_EBREAK_FULL_OP:
            raise InvalidOpcode(f"C2fj doesn't support ebreak ops (newlib shouldn't have produced it) (address 0x{addr:08x}).")
        else:
            raise InvalidOpcode(f"bad instruction at env call/break op: 0x{full_op:08x} (address 0x{addr:08x}).")

    else:
        raise InvalidOpcode(f"invalid op: 0x{full_op:08x} (address 0x{addr:08x}).")

    if not pc_changed:
        ops_file.write(f'    .inc_pc 0x{addr:08x}\n')

    ops_file.write('\n')
