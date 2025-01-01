GCC := /opt/riscv32/bin/riscv32-unknown-elf-gcc
RISCV_OPTIONS := -march=rv32im -mabi=ilp32 -specs=nosys.specs -specs=nano.specs -nostartfiles
GCC_FLAGS := -O3 -fno-merge-constants
LINKER_OPTIONS := -T linker_script.ld

SOURCES := c2fj_init.c main.c
OBJECTS := $(SOURCES:.c=.o)

all: |
	mkdir -p ../build
	$(GCC) $(RISCV_OPTIONS) $(GCC_FLAGS) $(SOURCES) $(LINKER_OPTIONS) -o ../build/main.elf

clean:
	rm -r build 2>/dev/null || true

.PHONY: clean all
