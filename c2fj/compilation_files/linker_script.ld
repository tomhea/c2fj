RAM_START_ADDRESS  = 0x20000000;
MEMORY_SIZE        = 0x100000000;
GUARD_SEGMENT_SIZE = 0x1000;
STACK_SIZE         = 0x20000;

RAM_STACK_START = RAM_START_ADDRESS + GUARD_SEGMENT_SIZE;
GENERIC_RAM_START = RAM_STACK_START + STACK_SIZE + GUARD_SEGMENT_SIZE;
GENERIC_RAM_END = MEMORY_SIZE - GUARD_SEGMENT_SIZE - GENERIC_RAM_START;

MEMORY
{
  rom        (rx)  : ORIGIN = 0x00000000,        LENGTH = RAM_START_ADDRESS
  ram_stack  (rwx) : ORIGIN = RAM_STACK_START,   LENGTH = STACK_SIZE
  ram        (rwx) : ORIGIN = GENERIC_RAM_START, LENGTH = GENERIC_RAM_END
}

/* Entry point of the program */
ENTRY(_start)

/* Section Definitions */
SECTIONS
{
    .text :
    {
        *(.text.*)
        *(.rodata.*)
        _etext = .;
    } > rom

    /* stack section */
    .stack (NOLOAD):
    {
        . = ALIGN(8);
        _stack = .;
        . = . + STACK_SIZE;
        _stack_end = .;
        . = ALIGN(8);
    } > ram_stack

    .data :
    {
        _sdata = .;
        *(.data*);
        *(.sdata*);
        *(.rodata*);
        *(.eh_frame*);
        _edata = .;
    } > ram AT >rom

    /* .bss section which is used for uninitialized data */
    .bss (NOLOAD) :
    {
        _sbss = . ;
        *(.bss)
        *(.bss.*)
        *(COMMON)
        _ebss = . ;
    } > ram

    .heap (NOLOAD):
    {
        . = ALIGN(8);
        _heap_start = . ;
        . = ALIGN(MEMORY_SIZE - GUARD_SEGMENT_SIZE);
    } > ram


}