GCC := /opt/riscv32/bin/riscv32-unknown-elf-gcc
GCC_FLAGS := -O3
LINKER_OPTIONS := -T linker_script.ld

SOURCES := $(C2FJ_SOURCES) main.c
OBJECTS := $(SOURCES:.c=.o)

all: |
	mkdir -p ../build
	$(GCC) $(C2FJ_GCC_OPTIONS) $(GCC_FLAGS) $(SOURCES) -I $(C2FJ_INCLUDE_DIRS) -T $(C2FJ_LINKER_SCRIPT) -o ../build/main.elf

clean:
	rm -r build 2>/dev/null || true

.PHONY: clean all
