GCC := /opt/riscv32/bin/riscv32-unknown-elf-gcc
GCC_OPTIONS := -march=rv32im -mabi=ilp32 -specs=nosys.specs -specs=nano.specs -nostartfiles
LINKER_OPTIONS := -T linker_script.ld

SOURCES := __init.c main.c
OBJECTS := $(SOURCES:.c=.o)

all: |
	mkdir -p ../build
	$(GCC) $(GCC_OPTIONS) $(SOURCES) $(LINKER_OPTIONS) -o ../build/main.elf

clean:
	rm -r build 2>/dev/null || true

.PHONY: clean all
