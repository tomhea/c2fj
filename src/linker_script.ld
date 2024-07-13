MEMORY
{
  rom      (rx)  : ORIGIN = 0x00000000, LENGTH = 0x00040000  # TODO change?
  ram      (rwx) : ORIGIN = 0x20000000, LENGTH = 0x00008000  # TODO change?
}

STACK_SIZE = 0x2000;  #  TODO change?

/* Entry point of the program */
ENTRY(_start)

/* Section Definitions */
SECTIONS
{
    .text :
    {
        _start = .;        /* Mark the start of the code section */
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

    /* stack section */
    .stack (NOLOAD):
    {
        . = ALIGN(8);
        . = . + STACK_SIZE;
        . = ALIGN(8);
    } > ram

    _end = . ;
}