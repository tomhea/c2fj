import contextlib
import os
import argparse
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Optional, Iterator, Union

import flipjump
from flipjump.utils.classes import PrintTimer

from c2fj.riscv_to_fj import create_fj_files_from_riscv_elf

COMPILATION_FILES_DIR = Path(__file__).parent / "compilation_files"

C2FJ_MAKE_VARS = {
    'C2FJ_GCC_OPTIONS': '-march=rv32im -mabi=ilp32 -specs=nosys.specs -specs=nano.specs '
                        '-nostartfiles -fno-merge-constants',
    'C2FJ_LINKER_SCRIPT': f'{COMPILATION_FILES_DIR / "linker_script.ld"}',
    'C2FJ_SOURCES': f'{COMPILATION_FILES_DIR / "c2fj_init.c"}',
    'C2FJ_INCLUDE_DIRS': f'{COMPILATION_FILES_DIR / "include"}',
}

C_EXTENSIONS = ['.c', '.h', '.cc']


def compile_c_to_riscv(file: Path, build_path: Path) -> None:
    with PrintTimer('  make c->riscv:   '):
        if file.suffix in C_EXTENSIONS:
            C2FJ_MAKE_VARS['SINGLE_C_FILE'] = str(file)
            makefile = COMPILATION_FILES_DIR / "Makefile_single_c_generic"
        else:
            makefile = file

        C2FJ_MAKE_VARS['ELF_OUT_PATH'] = str(build_path)

        make_vars_string = ' '.join(f'{k}="{v}"' for k, v in C2FJ_MAKE_VARS.items())
        assert 0 == os.system(f"make -s -f {makefile} -C {makefile.parent} {make_vars_string}"), "Make c->riscv failed."


def compile_riscv_to_fj(build_dir: Path) -> None:
    with PrintTimer('  comp riscv->fj:  '):
        create_fj_files_from_riscv_elf(
            elf_path=build_dir / 'main.elf',
            mem_path=build_dir / 'mem.fj',
            jmp_path=build_dir / 'jmp.fj',
            ops_path=build_dir / 'ops.fj',
        )


def compile_fj_to_fjm(build_dir: Path) -> None:
    flipjump.assemble(
        fj_file_paths=[COMPILATION_FILES_DIR / 'riscvlib.fj', build_dir / 'mem.fj', build_dir / 'jmp.fj', build_dir / 'ops.fj'],
        output_fjm_path=build_dir / 'main.fjm',
        warning_as_errors=False,
        debugging_file_path=build_dir / 'debug.fjd',
        show_statistics=False,
    )


def run_fjm(build_dir: Path, breakpoint_addresses: Optional[List[int]] = None, single_step: bool = False) -> None:
    flipjump.debug(
        fjm_path=build_dir / 'main.fjm',
        debugging_file=build_dir / 'debug.fjd',
        last_ops_debugging_list_length=6000,
        breakpoints_contains={"riscv.ADDR_"} if single_step else None,
        breakpoints={f"riscv.ADDR_{addr:08X}" for addr in breakpoint_addresses} if breakpoint_addresses else None,
    )


def c2fj(file: Path, build_dir: Union[None, str, Path] = None) -> None:
    with get_build_directory(build_dir) as build_dir:
        compile_c_to_riscv(file, build_dir / 'main.elf')
        compile_riscv_to_fj(build_dir)
        compile_fj_to_fjm(build_dir)
        run_fjm(build_dir)


@contextlib.contextmanager  # type: ignore
def get_build_directory(build_dir: Union[None, str, Path]) -> Iterator[Path]:
    if build_dir is None:
        with TemporaryDirectory() as build_dir:
            yield Path(build_dir)
        return

    build_dir = Path(build_dir)
    if not build_dir.exists() or not build_dir.is_dir():
        raise NotADirectoryError(f"This isn't a directory: {build_dir}")

    yield build_dir
    return


def main() -> None:
    argument_parser = argparse.ArgumentParser('c2fj', description='Compile C to fj')
    argument_parser.add_argument('file', help=f'Can be both a makefile, or a single c file '
                                              f'(ends with {" ".join(C_EXTENSIONS)})')
    argument_parser.add_argument('build_dir', default=None,
                                 help='If specified, the builds will be stored in this directory')
    args = argument_parser.parse_args()

    file = Path(args.file)
    if not file.exists() or not file.is_file():
        raise FileNotFoundError(f"This isn't a file: {file}")

    c2fj(file, args.build_dir)


if __name__ == '__main__':
    main()
