# c2fj
Compiling C --> RiscV --> Flipjump --> .fjm

Simply `python3 c2fj.py file.c` will compile your c file into an elf, into fj files, into fjm, then run it.

`c2fj` supports the next flags:
- `--breakpoints` Place a fj-breakpoint at the start of the specified riscv addresses
- `--single-step` Place fj-breakpoints at the start of all riscv opcodes
- `--unify_fj` Unify the generated fj files into a single file
- `--finish-after` Stop the compilation at any step (before running, before creating fjm, etc.)
- `--build-dir` Save the builds in this directory


## What if my project is more then a single c?

We support specifying a `Makefile` path, instead of the c file!  
Your Makefile will have to rely on some constants that `c2fj` will fill:
```c
C2FJ_GCC_OPTIONS
C2FJ_LINKER_SCRIPT
C2FJ_SOURCES
C2FJ_INCLUDE_DIRS
ELF_OUT_PATH
```

An example Makefile:
```makefile
GCC := /opt/riscv32/bin/riscv32-unknown-elf-gcc
GCC_FLAGS := -O3

SOURCES := $(C2FJ_SOURCES) main.c globals.c calculate_int.c
OBJECTS := $(SOURCES:.c=.o)

all: |
	$(GCC) $(C2FJ_GCC_OPTIONS) $(GCC_FLAGS) $(SOURCES) -I $(C2FJ_INCLUDE_DIRS) -T $(C2FJ_LINKER_SCRIPT) -o $(ELF_OUT_PATH)

clean:
	rm -r build 2>/dev/null || true

.PHONY: clean all

```

## Tests

Simply run `pytest` to run the tests.
