import io

import pytest

from c2fj.riscv_instructions import InvalidOpcode, fj_hex, sign_extend, write_op, write_op_safe

ADDI_A0_A1_7 = 0x00758513      # addi x10, x11, 7
JAL_RA_8 = 0x008000ef          # jal x1, .+8
JAL_EXIT_SYSCALL = 0x00a0056f  # jal x10, .+10 (the c2fj exit syscall encoding)
BEQ_T0_T1_16 = 0x00628863      # beq x5, x6, .+16
INVALID_OP = 0x00000000

ADDR = 0x1234


def write_op_to_string(full_op: int, addr: int = ADDR) -> str:
    ops_file = io.StringIO()
    write_op(ops_file, full_op, addr)
    return ops_file.getvalue()


@pytest.mark.parametrize("constant, bit_width, expected", [
    (0, 12, 0),
    (5, 12, 5),
    (0x7ff, 12, 2047),
    (0x800, 12, -2048),
    (0xfff, 12, -1),
    (0x80000000, 32, -0x80000000),
])
def test_sign_extend(constant: int, bit_width: int, expected: int) -> None:
    assert sign_extend(constant, bit_width) == expected


@pytest.mark.parametrize("constant, expected", [
    (0, '0x0'),
    (8, '0x8'),
    (-4, '(0 - 0x4)'),
])
def test_fj_hex(constant: int, expected: str) -> None:
    assert fj_hex(constant) == expected


def test_alu_imm_op_increments_pc() -> None:
    output = write_op_to_string(ADDI_A0_A1_7)
    assert '.addi .mov_rs1_to_x10, .mov_x11_to_rs1, 0x7' in output
    assert '.inc_pc 0x00001234' in output


def test_jump_op_does_not_increment_pc() -> None:
    output = write_op_to_string(JAL_RA_8)
    assert '.jal .zero_x1, .regs.x1, 0x8' in output
    assert '.inc_pc' not in output


def test_branch_op_does_not_increment_pc() -> None:
    output = write_op_to_string(BEQ_T0_T1_16)
    assert '.beq .mov_x5_to_rs1, .xor_x6_to_rs2, 0x10' in output
    assert '.inc_pc' not in output


def test_syscall_jal_op_increments_pc() -> None:
    output = write_op_to_string(JAL_EXIT_SYSCALL)
    assert '.syscall.exit .regs.x10' in output
    assert '.inc_pc 0x00001234' in output


def test_pc_state_is_not_shared_between_ops() -> None:
    # Regression test: a jump op mustn't affect the .inc_pc of the ops written after it.
    ops_file = io.StringIO()
    write_op(ops_file, JAL_RA_8, ADDR)
    write_op(ops_file, ADDI_A0_A1_7, ADDR + 4)
    output = ops_file.getvalue()
    assert output.count('.inc_pc') == 1
    assert '.inc_pc 0x00001238' in output


def test_write_op_safe_falls_back_on_invalid_op() -> None:
    ops_file = io.StringIO()
    write_op_safe(ops_file, INVALID_OP, ADDR, error_on_unimplemented_op=False)
    assert 'riscv.unimplemented_op' in ops_file.getvalue()


def test_write_op_safe_raises_on_invalid_op() -> None:
    with pytest.raises(InvalidOpcode):
        write_op_safe(io.StringIO(), INVALID_OP, ADDR, error_on_unimplemented_op=True)
