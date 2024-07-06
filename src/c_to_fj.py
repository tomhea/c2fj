from pathlib import Path
import os
from arm_to_fj import create_fj_files_from_arm_elf
import flipjump


def compile_c_to_arm() -> None:
    os.system(f"make")


def compile_arm_to_fj() -> None:
    create_fj_files_from_arm_elf(
        elf_path=Path('build/main.elf'),
        mem_path=Path('build/mem.fj'),
        jmp_path=Path('build/jmp.fj'),
        ops_path=Path('build/ops.fj'),
    )


def compile_fj_to_fjm() -> None:
    flipjump.assemble(
        fj_file_paths=[Path('build/mem.fj'), Path('build/jmp.fj'), Path('build/ops.fj'), Path('armv7lib.fj')],
        output_fjm_path=Path('build/main.fjm')
    )


def run_fjm() -> None:
    flipjump.run(fjm_path=Path('build/main.fjm'))


def main() -> None:
    compile_c_to_arm()
    compile_arm_to_fj()
    compile_fj_to_fjm()
    run_fjm()


if __name__ == '__main__':
    main()
