#include <stdint.h>
#include "c2fj_syscall.h"


#define PRINT_A2 "jal a2, .+22\n"
#define PRINT_LN "jal a2, .+3042\n"


int main() {
    asm volatile (
        "addi x2, x2, -1000\n"

        "lui a0, 0x12345\n"
        "addi a0, a0, 0x678\n"
        "sw a0, 4(x2)\n"
        "lw a2, 4(x2)\n"
        PRINT_A2
        "lh a2, 4(x2)\n"
        PRINT_A2
        "lhu a2, 4(x2)\n"
        PRINT_A2
        "lb a2, 4(x2)\n"
        PRINT_A2
        "lbu a2, 4(x2)\n"
        PRINT_A2
        PRINT_LN

        "lui a0, 0xDEADC\n"
        "addi a0, a0, 0xEEF-0x1000\n"
        "xor a2, a2, a2\n"
        "sw a0, 4(x2)\n"
        "lw a2, 4(x2)\n"
        PRINT_A2
        "lh a2, 4(x2)\n"
        PRINT_A2
        "lhu a2, 4(x2)\n"
        PRINT_A2
        "lb a2, 4(x2)\n"
        PRINT_A2
        "lbu a2, 4(x2)\n"
        PRINT_A2
        PRINT_LN

        "lui a0, 0x12345\n"
        "addi a0, a0, 0x678\n"
        "sh a0, 4(x2)\n"
        "lw a2, 4(x2)\n"
        PRINT_A2
        "sh a0, 6(x2)\n"
        "lw a2, 4(x2)\n"
        PRINT_A2
        PRINT_LN

        "lui a0, 0xDEADC\n"
        "addi a0, a0, 0xEEF-0x1000\n"
        "sb a0, 4(x2)\n"
        "lw a2, 4(x2)\n"
        PRINT_A2
        "sb a0, 7(x2)\n"
        "lw a2, 4(x2)\n"
        PRINT_A2
        PRINT_LN

        "addi x2, x2, +1000\n"
    :::"memory");

    return 0;
}
