from pathlib import Path
import elftools.elf.elffile  # type: ignore
from typing import TextIO, Iterator, Tuple


def register_name(register_index: int) -> str:
    """
    @param register_index: the 4 lsb will be used.
    """
    return f'.regs.r{register_index & 0xf}'


def get_hex_comment(op: int) -> str:
    return f'\\\\ op 0x{op:08x}'


def write_op(ops_file: TextIO, full_op: int) -> None:
    ops_file.write(f"  {get_hex_comment(full_op)}\n")
    pass  # TODO implement for arm. Current skeleton implementation is for riscv..
    # opcode = full_op & 0x7f
    # funct3 = (full_op >> 12) & 7
    # funct7 = full_op >> 25
    # x0_changed = False
    #
    # if opcode == RV_LUI:
    #     ops_file.write(u_type('lui', full_op))
    # elif opcode == RV_AUIPC:
    #     ops_file.write(u_type('auipc', full_op))
    # elif opcode == RV_JAL:
    #     ops_file.write(j_type('jal', full_op))
    # elif opcode == RV_JALR:
    #     if funct3 != 0:
    #         ops_file.write(f'    // ERROR - bad funct3 at jalr op - 0x{full_op:08x}\n')
    #     else:
    #         ops_file.write(i_type('jalr', full_op))
    #
    # elif opcode == RV_B:
    #     if funct3 == RV_BEQ:
    #         ops_file.write(b_type('beq', full_op))
    #     elif funct3 == RV_BNE:
    #         ops_file.write(b_type('bne', full_op))
    #     elif funct3 == RV_BLT:
    #         ops_file.write(b_type('blt', full_op))
    #     elif funct3 == RV_BGE:
    #         ops_file.write(b_type('bge', full_op))
    #     elif funct3 == RV_BLTU:
    #         ops_file.write(b_type('bltu', full_op))
    #     elif funct3 == RV_BGEU:
    #         ops_file.write(b_type('bgeu', full_op))
    #
    # else:
    #     ops_file.write(f'    \\\\TODO not-implemented op 0x{full_op:08x}\n')
    #     # TODO real ops here.
    #
    # x0_changed = True
    # if x0_changed:
    #     ops_file.write('    hex.zero 8 .regs.zero\n')
    #
    # ops_file.write('\n')


def get_addr_label_name(addr: int) -> str:
    return f'ADDR_{addr:08X}'


def write_jump_to_addr_label(jmp_file: TextIO, addr: int) -> None:
    jmp_file.write(f';.{get_addr_label_name(addr)}\n')


def write_declare_addr_label(ops_file: TextIO, addr: int) -> None:
    ops_file.write(f'{get_addr_label_name(addr)}:\n')


def write_memory_data(mem_file: TextIO, data: bytes, virtual_address: int, reserved_bytes_size: int) -> None:
    mem_file.write(f'segment .MEM + 0x{virtual_address:08x}*dw\n')
    # for byte in data:
        # mem_file.write(f'arm.byte {byte}\n')
    mem_file.write(f'arm.byte.vec {len(data)}, 0x{data[::-1].hex()}\n')
    if reserved_bytes_size > 0:
        mem_file.write(f'reserve {reserved_bytes_size}*dw\n')
    mem_file.write(f'\n\n')


def ops_and_addr_iterator(data: bytes, virtual_address: int) -> Iterator[Tuple[int, int]]:
    return ((int.from_bytes(data[i:i+4], 'little'), virtual_address + i)
            for i in range(0, len(data), 4))


def write_ops_and_jumps(ops_file: TextIO, jmp_file: TextIO, data: bytes, virtual_address: int) -> None:
    jmp_file.write(f'segment .JMP + 0x{virtual_address:08x}/4*dw\n')
    for op, addr in ops_and_addr_iterator(data, virtual_address):
        write_jump_to_addr_label(jmp_file, addr)
        write_declare_addr_label(ops_file, addr)
        write_op(ops_file, op)

    jmp_file.write(f'\n\n')
    ops_file.write(f'\n\n')


def write_open_arm_namespace(file: TextIO) -> None:
    file.write(f"ns arm {{\n\n\n")


def write_init_arm_ops(ops_file: TextIO, start_addr: int) -> None:
    ops_file.write(f"MEM = 1<<(w-1)                      \\\\ start of memory\n"
                   f"JMP = .MEM - (.MEM / 32)            \\\\ start of jump table\n\n"  # TODO is it right?
                   f";.{get_addr_label_name(start_addr)}                     \\\\ entry point\n"
                   f".init                               \\\\ init registers, structs, functions\n\n\n\n")


def write_close_arm_namespace(file: TextIO) -> None:
    file.write(f"}}\n")


def is_loaded_to_memory(segment):
    return segment['p_type'] == 'PT_LOAD'


def is_segment_executable(segment):
    return segment['p_flags'] & 1


def get_virtual_start_address(segment):
    return segment['p_vaddr']


def get_reserved_byte_size(segment):
    return segment['p_memsz'] - segment['p_filesz']


def get_segment_data(segment) -> bytes:
    return segment.data()


def write_segment(mem_file: TextIO, jmp_file: TextIO, ops_file: TextIO, segment) -> None:
    virtual_address = get_virtual_start_address(segment)
    reserved_byte_size = get_reserved_byte_size(segment)
    data = get_segment_data(segment)

    if is_segment_executable(segment):
        write_ops_and_jumps(ops_file, jmp_file, data, virtual_address)
    write_memory_data(mem_file, data, virtual_address, reserved_byte_size)


def get_start_address(elf: elftools.elf.elffile.ELFFile) -> int:
    return elf['e_entry']


def write_file_prefixes(mem_file: TextIO, jmp_file: TextIO, ops_file: TextIO, elf: elftools.elf.elffile.ELFFile) -> None:
    for file in (mem_file, jmp_file, ops_file):
        write_open_arm_namespace(file)

    write_init_arm_ops(ops_file, get_start_address(elf))


def write_file_suffixes(mem_file: TextIO, jmp_file: TextIO, ops_file: TextIO) -> None:
    for file in (mem_file, jmp_file, ops_file):
        write_close_arm_namespace(file)


def get_segments(elf: elftools.elf.elffile.ELFFile) -> Iterator:
    return elf.iter_segments()


def create_fj_files_from_arm_elf(elf_path: Path, mem_path: Path, jmp_path: Path, ops_path: Path) -> None:
    with mem_path.open('w') as mem_file, \
            jmp_path.open('w') as jmp_file, \
            ops_path.open('w') as ops_file, \
            elf_path.open('rb') as elf_file:

        elf = elftools.elf.elffile.ELFFile(elf_file)
        write_file_prefixes(mem_file, jmp_file, ops_file, elf)

        for segment in get_segments(elf):
            if is_loaded_to_memory(segment):
                write_segment(mem_file, jmp_file, ops_file, segment)

        write_file_suffixes(mem_file, jmp_file, ops_file)
