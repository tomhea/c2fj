from pathlib import Path
from typing import TextIO, Iterator, Tuple

import elftools.elf.elffile  # type: ignore

from c2fj.riscv_instructions import write_op_safe


def get_symbol_value(elf: elftools.elf.elffile.ELFFile, symbol_name: str) -> int:
    symtab_section = elf.get_section_by_name('.symtab')
    if symtab_section is None:
        raise ValueError('Symbol section not found.')

    for symbol in symtab_section.iter_symbols():
        if symbol.name == symbol_name:
            return symbol.entry.st_value

    raise ValueError(f'Symbol name "{symbol_name}" not found.')


def get_addr_label_name(addr: int) -> str:
    return f'ADDR_{addr:08X}'


def write_jump_to_addr_label(jmp_file: TextIO, addr: int) -> None:
    jmp_file.write(f';.{get_addr_label_name(addr)}\n')


def write_declare_addr_label(ops_file: TextIO, addr: int) -> None:
    ops_file.write(f'{get_addr_label_name(addr)}:\n')


def write_memory_data(mem_file: TextIO, data: bytes, virtual_address: int, reserved_bytes_size: int) -> None:
    mem_file.write(f'segment .MEM + 0x{virtual_address:08x}*dw\n')
    # for byte in data:
        # mem_file.write(f'riscv.byte {byte}\n')
    if len(data) > 0:
        mem_file.write(f'riscv.byte.vec {len(data)}, 0x{data[::-1].hex()}\n')
    if reserved_bytes_size > 0:
        mem_file.write(f'reserve {hex(reserved_bytes_size)}*dw\n')
    mem_file.write(f'\n\n')


def ops_and_addr_iterator(data: bytes, virtual_address: int) -> Iterator[Tuple[int, int]]:
    return ((int.from_bytes(data[i:i + 4], 'little'), virtual_address + i)
            for i in range(0, len(data), 4))


def write_ops_and_jumps(ops_file: TextIO, jmp_file: TextIO, data: bytes, virtual_address: int,
                        error_on_unimplemented_op: bool = False) -> None:
    jmp_file.write(f'segment .JMP + 0x{virtual_address:08x}/4*dw\n')
    for op, addr in ops_and_addr_iterator(data, virtual_address):
        write_jump_to_addr_label(jmp_file, addr)
        write_declare_addr_label(ops_file, addr)
        write_op_safe(ops_file, op, addr, error_on_unimplemented_op)

    jmp_file.write(f'\n\n')
    ops_file.write(f'\n\n')


def write_open_riscv_namespace(file: TextIO) -> None:
    file.write(f"ns riscv {{\n\n\n")


def write_init_riscv_ops(ops_file: TextIO, start_addr: int) -> None:
    ops_file.write(f"segment 0\n"
                   f".start .{get_addr_label_name(start_addr)}\n\n\n")


def write_close_riscv_namespace(file: TextIO) -> None:
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


def write_file_prefixes(mem_file: TextIO, jmp_file: TextIO, ops_file: TextIO,
                        elf: elftools.elf.elffile.ELFFile) -> None:
    for file in (mem_file, jmp_file, ops_file):
        write_open_riscv_namespace(file)

    write_init_riscv_ops(ops_file, get_start_address(elf))


def write_file_suffixes(mem_file: TextIO, jmp_file: TextIO, ops_file: TextIO) -> None:
    for file in (mem_file, jmp_file, ops_file):
        write_close_riscv_namespace(file)


def get_segments(elf: elftools.elf.elffile.ELFFile) -> Iterator:
    return elf.iter_segments()


def create_fj_files_from_riscv_elf(elf_path: Path, mem_path: Path, jmp_path: Path, ops_path: Path) -> None:
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
