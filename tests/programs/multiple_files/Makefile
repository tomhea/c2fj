GCC := riscv64-unknown-elf-gcc
GCC_FLAGS := -O3

SOURCES := $(C2FJ_SOURCES) main.c globals.c calculate_int.c
OBJECTS := $(SOURCES:.c=.o)

all: |
	$(GCC) $(C2FJ_GCC_OPTIONS) $(GCC_FLAGS) $(SOURCES) -I $(C2FJ_INCLUDE_DIRS) -T $(C2FJ_LINKER_SCRIPT) -o $(ELF_OUT_PATH)

clean:
	rm -r build 2>/dev/null || true

.PHONY: clean all
