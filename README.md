[![GitHub](https://img.shields.io/github/license/tomhea/c2fj)](LICENSE)
[![Website](https://img.shields.io/website?down_color=red&down_message=down&up_message=up&url=https%3A%2F%2Fesolangs.org%2Fwiki%2FFlipJump)](https://esolangs.org/wiki/FlipJump)
[![PyPI - Version](https://img.shields.io/pypi/v/c2fj)](https://pypi.org/project/c2fj/)

# c2fj
Compiling C --> RiscV --> Flipjump --> .fjm

An example program, [primes/main.c](tests/programs/primes/main.c):
```c
int main() {
    printf("Calculate primes up to: ");
    int max_number;
    scanf("%d", &max_number);
    
    ...
    
    for (int p = 3; p <= max_number; p += 2) {
        if (non_prime[p] == false) {
            for (int i = p*p; i <= max_number; i += p) {
                non_prime[i] = true;
            }
            printf("%d\n", p);
        }
    }
    
    return 0;
}
```
Compiled into this:

![img.png](res/compiled_elf.png)

Which was compiled into this:

![img.png](res/compiled_fj_files.png)

Which in turn compiled into:

![img.png](res/compiled_fjm.png)

Now, run it (Remember, these are flipjump ops that are running):

```text
Calculate primes up to: 20
2
3
5
7
11
13
17
19
Program exited with exit code 0x0.
```

# How to use

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
GCC := riscv64-unknown-elf-gcc
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
