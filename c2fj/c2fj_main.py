import argparse
import contextlib
import os
import shutil
from enum import Enum
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Optional, Iterator, Union

import flipjump
from flipjump.utils.classes import PrintTimer

from c2fj.riscv_to_fj import create_fj_files_from_riscv_elf

COMPILATION_FILES_DIR = Path(__file__).parent / "compilation_files"

C2FJ_MAKE_VARS = {
    'C2FJ_GCC_OPTIONS': '-march=rv32im -mabi=ilp32 -specs=nosys.specs -specs=nano.specs '
                        '-nostartfiles -fno-merge-constants -fno-toplevel-reorder -fdata-sections -ffunction-sections',
    'C2FJ_LINKER_SCRIPT': f'{COMPILATION_FILES_DIR / "linker_script.ld"}',
    'C2FJ_SOURCES': f'{COMPILATION_FILES_DIR / "c2fj_init.c"}',
    'C2FJ_INCLUDE_DIRS': f'{COMPILATION_FILES_DIR / "include"}',
}

C_EXTENSIONS = ['.c', '.h', '.cc']
ELF_EXTENSIONS = ['.elf', '.out']


class BuildNames(Enum):
    ELF = 'main.elf'
    OPS_FJ = 'ops.fj'
    MEMORY_FJ = 'mem.fj'
    JUMPS_FJ = 'jmp.fj'
    UNIFIED_FJ = 'unified.fj'
    FJM = 'main.fjm'
    FJ_DEBUG = 'debug.fjd'


def compile_c_to_riscv(file: Path, build_path: Path) -> None:
    if file.suffix in ELF_EXTENSIONS:
        shutil.copy(file, build_path)
        return

    with PrintTimer('  make c->riscv:   '):
        if file.suffix in C_EXTENSIONS:
            C2FJ_MAKE_VARS['SINGLE_C_FILE'] = str(file)
            makefile = COMPILATION_FILES_DIR / "Makefile_single_c_generic"
        else:
            makefile = file

        C2FJ_MAKE_VARS['ELF_OUT_PATH'] = str(build_path)

        make_vars_string = ' '.join(f'{k}="{v}"' for k, v in C2FJ_MAKE_VARS.items())
        assert 0 == os.system(f"make -s -f {makefile} -C {makefile.parent} {make_vars_string}"), "Make c->riscv failed."


def get_fj_files_in_order(build_dir: Path) -> List[Path]:
    """
    @return: The fj files in their compilation order.
    """
    return [COMPILATION_FILES_DIR / 'riscvlib.fj', build_dir / BuildNames.MEMORY_FJ.value,
            build_dir / BuildNames.JUMPS_FJ.value, build_dir / BuildNames.OPS_FJ.value]


def unify_fj_files(ordered_fj_files: List[Path], build_path: Path) -> None:
    with build_path.open('w') as unified:
        for fj_file in ordered_fj_files:
            with fj_file.open('r') as f:
                unified.write(f'// START {fj_file.name}\n\n')
                unified.write(f.read())
                unified.write(f'// END {fj_file.name}\n\n\n\n')


def compile_riscv_to_fj(build_dir: Path, unify_fj: bool = False) -> None:
    with PrintTimer('  comp riscv->fj:  '):
        create_fj_files_from_riscv_elf(
            elf_path=build_dir / BuildNames.ELF.value,
            mem_path=build_dir / BuildNames.MEMORY_FJ.value,
            jmp_path=build_dir / BuildNames.JUMPS_FJ.value,
            ops_path=build_dir / BuildNames.OPS_FJ.value,
        )

    if unify_fj:
        unify_fj_files(get_fj_files_in_order(build_dir), build_dir / BuildNames.UNIFIED_FJ.value)


def compile_fj_to_fjm(build_dir: Path) -> None:
    flipjump.assemble(
        fj_file_paths=get_fj_files_in_order(build_dir),
        output_fjm_path=build_dir / BuildNames.FJM.value,
        warning_as_errors=False,
        debugging_file_path=build_dir / BuildNames.FJ_DEBUG.value,
        show_statistics=False,
    )


def run_fjm(build_dir: Path, breakpoint_addresses: Optional[List[int]] = None, single_step: bool = False) -> None:
    flipjump.debug(
        fjm_path=build_dir / BuildNames.FJM.value,
        debugging_file=build_dir / BuildNames.FJ_DEBUG.value,
        last_ops_debugging_list_length=6000,
        breakpoints_contains={"riscv.ADDR_"} if single_step else None,
        breakpoints={f"riscv.ADDR_{addr:08X}" for addr in breakpoint_addresses} if breakpoint_addresses else None,
    )


class FinishCompilingAfter(Enum):
    ELF = 'elf'
    FJ = 'fj'
    FJM = 'fjm'
    RUN = 'run'


def c2fj(file: Path, build_dir: Union[None, str, Path] = None, unify_fj: bool = False,
         finish_compiling_after: FinishCompilingAfter = FinishCompilingAfter.RUN,
         breakpoint_addresses: Optional[List[int]] = None, single_step: bool = False) -> None:
    with get_build_directory(build_dir) as build_dir:
        compile_c_to_riscv(file, build_dir / BuildNames.ELF.value)
        if finish_compiling_after == FinishCompilingAfter.ELF:
            return

        compile_riscv_to_fj(build_dir, unify_fj)
        if finish_compiling_after == FinishCompilingAfter.FJ:
            return

        compile_fj_to_fjm(build_dir)
        if finish_compiling_after == FinishCompilingAfter.FJM:
            return

        run_fjm(build_dir, breakpoint_addresses=breakpoint_addresses, single_step=single_step)


@contextlib.contextmanager  # type: ignore
def get_build_directory(build_dir: Union[None, str, Path]) -> Iterator[Path]:
    if build_dir is None:
        with TemporaryDirectory() as temp_dir:
            yield Path(temp_dir).absolute()
        return

    build_dir = Path(build_dir).absolute()
    if not build_dir.exists() or not build_dir.is_dir():
        raise NotADirectoryError(f"This isn't a directory: {build_dir}")

    yield build_dir
    return


def main() -> None:
    argument_parser = argparse.ArgumentParser('c2fj', description='Compile C to fj')
    argument_parser.add_argument('file', metavar='PATH', help=f'Can be a makefile, '
                                              f'a single c file (ends with {" ".join(C_EXTENSIONS)}), '
                                              f'or a compiled elf file (ends with {" ".join(ELF_EXTENSIONS)})')
    argument_parser.add_argument('--build-dir', metavar='PATH', default=None,
                                 help='If specified, the builds will be stored in this directory')
    argument_parser.add_argument('--unify-fj', '-u', action='store_true',
                                 help=f'Unify the build fj files into a single "{BuildNames.UNIFIED_FJ.value}" file')
    argument_parser.add_argument('--finish-after', '-f', metavar='PHASE',
                                 default=FinishCompilingAfter.RUN.value,
                                 choices=[e.value for e in FinishCompilingAfter])
    argument_parser.add_argument('--breakpoints', '-b', metavar='ADDR', nargs='+', default=None,
                                 type=lambda s: int(s, 0), help='breakpoint addresses')
    argument_parser.add_argument('--single-step', '-s', action='store_true',
                                 help='Stop at the start of every riscv opcode')
    args = argument_parser.parse_args()

    file = Path(args.file)
    if not file.exists() or not file.is_file():
        raise FileNotFoundError(f"This isn't a file: {file}")

    c2fj(file.absolute(), args.build_dir, args.unify_fj, FinishCompilingAfter(args.finish_after),
         args.breakpoints, args.single_step)


if __name__ == '__main__':
    main()
