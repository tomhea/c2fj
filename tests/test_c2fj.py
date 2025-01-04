from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
from flipjump import run_test_output
from flipjump.utils.constants import IO_BYTES_ENCODING

from c2fj.c2fj_main import c2fj, FinishCompilingAfter, BuildNames

PROGRAMS_DIR = Path(__file__).parent / "programs"


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
    "sanity",
    "hello_world",
    "hello_math",
    "hello_input",
    "hello_input_number",
])
def test_c2fj_c_file(directory_name: str) -> None:
    directory = PROGRAMS_DIR / directory_name
    run_c2fj_test(directory / "main.c", directory / "input.txt", directory / "output.txt")


@pytest.mark.parametrize("directory_name", [
    "multiple_files",
    "riscv_ops__all_c_syscalls",
    "riscv_ops__alu",
    "riscv_ops__alu_imm",
    "riscv_ops__jumps",
    "riscv_ops__memory",
    "riscv_ops__rv32m",
])
def test_c2fj_makefile(directory_name: str):
    directory = PROGRAMS_DIR / directory_name
    run_c2fj_test(directory / "Makefile", directory / "input.txt", directory / "output.txt")
