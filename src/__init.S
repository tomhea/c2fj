.global _start
.section .text.entry
_start:
    la sp, _stack_end - 8
    j start
