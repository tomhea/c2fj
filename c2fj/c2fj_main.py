import os
import argparse
from pathlib import Path
from typing import List, Optional

import flipjump
from flipjump.utils.classes import PrintTimer

from c2fj.riscv_to_fj import create_fj_files_from_riscv_elf

BUILD_DIR = Path(__file__).parent.parent / "build"
COMPILATION_FILES_DIR = Path(__file__).parent / "compilation_files"

C2FJ_MAKE_VARS = {
    'C2FJ_GCC_OPTIONS': '-march=rv32im -mabi=ilp32 -specs=nosys.specs -specs=nano.specs '
                        '-nostartfiles -fno-merge-constants',
    'C2FJ_LINKER_SCRIPT': f'{COMPILATION_FILES_DIR / "linker_script.ld"}',
    'C2FJ_SOURCES': f'{COMPILATION_FILES_DIR / "c2fj_init.c"}',
    'C2FJ_INCLUDE_DIRS': f'{COMPILATION_FILES_DIR / "include"}',
}


def compile_c_to_riscv(file: Path) -> None:
    with PrintTimer('  make c->riscv:   '):
        if not file.exists() or not file.is_file():
            raise FileNotFoundError(f"This isn't a file: {file}")

        if file.suffix in ['.c', '.h', '.cc']:
            C2FJ_MAKE_VARS['SINGLE_C_FILE'] = str(file)
            makefile = COMPILATION_FILES_DIR / "Makefile_single_c_generic"
        else:
            makefile = file

        make_vars_string = ' '.join(f'{k}="{v}"' for k, v in C2FJ_MAKE_VARS.items())
        assert 0 == os.system(f"make -s -f {makefile} -C {makefile.parent} {make_vars_string}"), "Make c->riscv failed."


def compile_riscv_to_fj() -> None:
    with PrintTimer('  comp riscv->fj:  '):
        create_fj_files_from_riscv_elf(
            elf_path=BUILD_DIR / 'main.elf',
            mem_path=BUILD_DIR / 'mem.fj',
            jmp_path=BUILD_DIR / 'jmp.fj',
            ops_path=BUILD_DIR / 'ops.fj',
        )


def compile_fj_to_fjm() -> None:
    flipjump.assemble(
        fj_file_paths=[COMPILATION_FILES_DIR / 'riscvlib.fj', BUILD_DIR / 'mem.fj', BUILD_DIR / 'jmp.fj', BUILD_DIR / 'ops.fj'],
        output_fjm_path=BUILD_DIR / 'main.fjm',
        warning_as_errors=False,
        debugging_file_path=BUILD_DIR / 'debug.fjd',
        show_statistics=False,
    )


def run_fjm(breakpoint_addresses: Optional[List[int]] = None, single_step: bool = False) -> None:
    flipjump.debug(
        fjm_path=BUILD_DIR / 'main.fjm',
        debugging_file=BUILD_DIR / 'debug.fjd',
        last_ops_debugging_list_length=6000,
        breakpoints_contains={"riscv.ADDR_"} if single_step else None,
        breakpoints={f"riscv.ADDR_{addr:08X}" for addr in breakpoint_addresses} if breakpoint_addresses else None,
    )


def c2fj(file: Path):
    compile_c_to_riscv(file)
    compile_riscv_to_fj()
    compile_fj_to_fjm()
    run_fjm()


def main() -> None:
    argument_parser = argparse.ArgumentParser('c2fj', description='Compile C to fj')
    argument_parser.add_argument('file', help='Can be both a makefile, or a single c file (ends with .c)')
    args = argument_parser.parse_args()

    c2fj(Path(args.file))


if __name__ == '__main__':
    main()
