import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from flipjump import run_test_output
from flipjump.utils.constants import IO_BYTES_ENCODING

from c2fj.c2fj_main import (c2fj, compile_c_to_riscv, C2FJ_MAKE_VARS, FinishCompilingAfter, BuildNames,
                            MakeFailedError)

PROGRAMS_DIR = Path(__file__).parent / "programs"


def create_uncompilable_c_file(directory: Path) -> Path:
    bad_c_file = directory / "bad.c"
    bad_c_file.write_text("int main( { this is not C ")
    return bad_c_file


def run_c2fj_test(file: Path, fixed_input_file: Path, expected_output_file: Path) -> None:
    with TemporaryDirectory() as temp_dir:
        build_dir = Path(temp_dir)

        c2fj(file, build_dir=build_dir, finish_compiling_after=FinishCompilingAfter.FJM)
        run_test_output(
            build_dir / BuildNames.FJM.value,
            fixed_input=fixed_input_file.read_text().encode(IO_BYTES_ENCODING),
            expected_output=expected_output_file.read_text().encode(IO_BYTES_ENCODING),
            should_raise_assertion_error=True,
            debugging_file=build_dir / BuildNames.FJ_DEBUG.value,
        )


@pytest.mark.parametrize("directory_name", [
    "primes",
    "print_alice",
    "hello_float",
    "hello_input_number",
    "hello_input",
    "hello_math",
    "hello_world",
    "sanity",
])
def test_c2fj_c_file(directory_name: str) -> None:
    directory = PROGRAMS_DIR / directory_name
    run_c2fj_test(directory / "main.c", directory / "input.txt", directory / "output.txt")


@pytest.mark.parametrize("directory_name", [
    "riscv_ops__all_c_syscalls",
    "multiple_files",
    "riscv_ops__rv32m",
    "riscv_ops__alu",
    "riscv_ops__alu_imm",
    "riscv_ops__jumps",
    "riscv_ops__memory",
])
def test_c2fj_makefile(directory_name: str):
    directory = PROGRAMS_DIR / directory_name
    run_c2fj_test(directory / "Makefile", directory / "input.txt", directory / "output.txt")


def test_c2fj_c_file_in_directory_with_spaces(tmp_path: Path) -> None:
    hello_world_dir = PROGRAMS_DIR / "hello_world"
    spaced_main_c = tmp_path / "dir with spaces" / "main.c"
    spaced_main_c.parent.mkdir()
    shutil.copy(hello_world_dir / "main.c", spaced_main_c)
    run_c2fj_test(spaced_main_c, hello_world_dir / "input.txt", hello_world_dir / "output.txt")


def test_c2fj_sequential_compilations_in_the_same_process() -> None:
    # Regression test: compiling a single c file mustn't affect the next Makefile-based compilation
    #  (e.g. by leaking the SINGLE_C_FILE make variable).
    c_file_dir = PROGRAMS_DIR / "hello_world"
    makefile_dir = PROGRAMS_DIR / "multiple_files"
    run_c2fj_test(c_file_dir / "main.c", c_file_dir / "input.txt", c_file_dir / "output.txt")
    run_c2fj_test(makefile_dir / "Makefile", makefile_dir / "input.txt", makefile_dir / "output.txt")


@pytest.mark.parametrize("finish_compiling_after", [
    FinishCompilingAfter.ELF,
    FinishCompilingAfter.FJ,
    FinishCompilingAfter.FJM,
])
def test_c2fj_finish_after_requires_build_dir(finish_compiling_after: FinishCompilingAfter) -> None:
    with pytest.raises(ValueError):
        c2fj(PROGRAMS_DIR / "hello_world" / "main.c", build_dir=None,
             finish_compiling_after=finish_compiling_after)


def test_c2fj_failing_compilation_raises(tmp_path: Path) -> None:
    bad_c_file = create_uncompilable_c_file(tmp_path)
    with pytest.raises(MakeFailedError):
        compile_c_to_riscv(bad_c_file, tmp_path / "main.elf")


def test_c2fj_make_vars_are_not_mutated(tmp_path: Path) -> None:
    bad_c_file = create_uncompilable_c_file(tmp_path)
    with pytest.raises(MakeFailedError):
        compile_c_to_riscv(bad_c_file, tmp_path / "main.elf")

    assert 'SINGLE_C_FILE' not in C2FJ_MAKE_VARS
    assert 'ELF_OUT_PATH' not in C2FJ_MAKE_VARS
