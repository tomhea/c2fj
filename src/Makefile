GCC := arm-none-eabi-gcc
LD := arm-none-eabi-ld
GCC_OPTIONS := -march=armv7-a -marm -nostartfiles -specs=nano.specs
LINKER_OPTIONS := -T linker_script.ld

SOURCES := __init.c main.c
OBJECTS := $(SOURCES:.c=.o)

all: |
	mkdir -p build
	$(GCC) $(GCC_OPTIONS) $(SOURCES) $(LINKER_OPTIONS) -o build/main.elf

clean:
	rm -r build 2>/dev/null || true

.PHONY: clean all
