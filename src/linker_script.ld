RAM_START_ADDRESS = 0x20000000;
RAM_MEMORY_SIZE   = 0xE0000000;
MEMORY_SIZE      = 0x100000000;


MEMORY
{
  rom      (rx)  : ORIGIN = 0x00000000,        LENGTH = RAM_START_ADDRESS
  ram      (rwx) : ORIGIN = RAM_START_ADDRESS, LENGTH = RAM_MEMORY_SIZE
}

GUARD_SEGMENT_SIZE = 0x1000;
STACK_SIZE = 0x20000;


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

    /* .bss section which is used for uninitialized data */
    .bss (NOLOAD) :
    {
        _sbss = . ;
        *(.bss .bss.*)
        *(COMMON)
        _ebss = . ;
    } > ram

    .data :
    {
        _sdata = .;
        *(.data*);
        _edata = .;
    } > ram AT >rom

    .fj_guard_stack (NOLOAD):
    {
        . = ALIGN(8);
        . = . + GUARD_SEGMENT_SIZE;
        . = ALIGN(8);
    } > ram

    /* stack section */
    .stack (NOLOAD):
    {
        . = ALIGN(8);
        _stack = .;
        . = . + STACK_SIZE;
        _stack_end = .;
        . = ALIGN(8);
    } > ram

    .fj_guard_stack_heap (NOLOAD):
    {
        . = ALIGN(8);
        . = . + GUARD_SEGMENT_SIZE;
        . = ALIGN(8);
    } > ram

    .heap (NOLOAD):
    {
        . = ALIGN(8);
        _heap_start = . ;
        . = ALIGN(MEMORY_SIZE - GUARD_SEGMENT_SIZE);
    } > ram


}