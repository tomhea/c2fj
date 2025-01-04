#include <stdint.h>
#include "c2fj_syscall.h"


int main() {
    // TODO test all 6 branch opcodes.
    int32_t val;

    asm volatile ("lui %0, 0x12345\n":"=r"(val)::"memory");
    c2fj_print_register(val);
    asm volatile ("lui %0, 0xABCDE\n":"=r"(val)::"memory");
    c2fj_print_register(val);
    asm volatile ("lui %0, 0\n":"=r"(val)::"memory");
    c2fj_print_register(val);
    c2fj_print_char('\n');

    asm volatile (
        "auipc a0, 0x123\n"
        "jal a1, 1f\n"
        "addi a0, a0, 0x400\n"
        "1: sub a0, a0, a1\n"
        "lui a1, 0x123\n"
        "sub a1, a1, a0\n"
        "jal a1, .+22\n"    // prints 0x8
    :::"memory");
    c2fj_print_char('\n');

    asm volatile (
        "xor a2, a2, a2\n"
        "auipc a0, 0x1\n"
        "addi a0, a0, -0x7f0\n"
        "addi a0, a0, -0x7f0\n"
        "jalr a1, a0, 8\n"
        "addi a2, a2, 1\n"  // a1
        "addi a2, a2, 1\n"
        "addi a2, a2, 1\n"
        "addi a2, a2, 1\n"
        "addi a2, a2, 1\n"  // a0
        "addi a2, a2, 1\n"
        "addi a2, a2, 1\n"  // a0+8
        "addi a2, a2, 1\n"
        "addi a2, a2, 1\n"
        "addi a2, a2, 1\n"
        "addi a2, a2, 1\n"
        "jal a2, .+22\n"    // prints 0x5
        "sub a2, a0, a1\n"
        "jal a2, .+22\n"    // prints 0x10
    :::"memory");
    c2fj_print_char('\n');

//        asm volatile (
//        "xor a2, a2, a2\n"
//        "lui a0, 0x123\n"
//        "lui a1, 0x123\n"
//        "beq a0, a1, 5f\n"
//        "lui a2, 0x123"
//        "5:"
//    :::"memory");
//    c2fj_print_char('\n');

    return 0;
}
