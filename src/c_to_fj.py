from pathlib import Path
import os
from riscv_to_fj import create_fj_files_from_riscv_elf
import flipjump


BUILD_DIR = Path(__file__).parent.parent / "build"


def compile_c_to_riscv() -> None:
    os.system(f"make")


def compile_riscv_to_fj() -> None:
    create_fj_files_from_riscv_elf(
        elf_path=BUILD_DIR / 'main.elf',
        mem_path=BUILD_DIR / 'mem.fj',
        jmp_path=BUILD_DIR / 'jmp.fj',
        ops_path=BUILD_DIR / 'ops.fj',
    )


def compile_fj_to_fjm() -> None:
    flipjump.assemble(
        fj_file_paths=[Path('riscvlib.fj'), BUILD_DIR / 'mem.fj', BUILD_DIR / 'jmp.fj', BUILD_DIR / 'ops.fj'],
        output_fjm_path=BUILD_DIR / 'main.fjm',
        warning_as_errors=False,
        debugging_file_path=BUILD_DIR / 'debug.fjd',
        show_statistics=False,
    )


def run_fjm() -> None:
    flipjump.debug(
        fjm_path=BUILD_DIR / 'main.fjm',
        debugging_file=BUILD_DIR / 'debug.fjd',
        last_ops_debugging_list_length=3000,
        # breakpoints={"riscv.ADDR_00000014"},
    )


def main() -> None:
    compile_c_to_riscv()
    compile_riscv_to_fj()
    compile_fj_to_fjm()
    run_fjm()


if __name__ == '__main__':
    main()
