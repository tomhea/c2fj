from pathlib import Path

from c2fj.c2fj_main import c2fj


PROGRAMS_DIR = Path(__file__).parent / "programs"


def test_c2fj_makefile():
    c2fj(PROGRAMS_DIR / "main" / "Makefile")


def test_c2fj_c_file():
    c2fj(PROGRAMS_DIR / "main" / "main.c")
