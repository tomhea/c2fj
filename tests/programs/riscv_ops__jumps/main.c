#include <stdint.h>
#include "c2fj_syscall.h"


#define PRINT_A2 "jal a2, .+22\n"


/// Compares in this order beq,bne, blt,bge, bltu,bgeu
/// Foreach: print 1 if taken, 0 if not taken.
void compare_with_numbers(int32_t a0, int32_t a1) {
asm volatile (
        "mv a0, %0\n"
        "mv a1, %1\n"

        "addi a2, zero, 0x1\n"
        "beq a0, a1, 1f\n"
        "xor a2, a2, a2\n"
        "1: " PRINT_A2

        "addi a2, zero, 0x1\n"
        "bne a0, a1, 2f\n"
        "xor a2, a2, a2\n"
        "2: " PRINT_A2

        "addi a2, zero, 0x1\n"
        "blt a0, a1, 3f\n"
        "xor a2, a2, a2\n"
        "3: " PRINT_A2

        "addi a2, zero, 0x1\n"
        "bge a0, a1, 4f\n"
        "xor a2, a2, a2\n"
        "4: " PRINT_A2

        "addi a2, zero, 0x1\n"
        "bltu a0, a1, 5f\n"
        "xor a2, a2, a2\n"
        "5: " PRINT_A2

        "addi a2, zero, 0x1\n"
        "bgeu a0, a1, 6f\n"
        "xor a2, a2, a2\n"
        "6: " PRINT_A2

    ::"r"(a0), "r"(a1) : "a0", "a1", "a2", "memory");
    c2fj_print_char('\n');
}


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
        "sub a2, a1, a0\n"
        PRINT_A2            // prints 0x8
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
        PRINT_A2            // prints 0x5
        "sub a2, a0, a1\n"
        PRINT_A2            // prints 0x10
    :::"memory");
    c2fj_print_char('\n');

    compare_with_numbers(0x123, 0x123);
    compare_with_numbers(0x234, 0x123);
    compare_with_numbers(0x123, 0x234);

    compare_with_numbers(-0x123, 0x234);
    compare_with_numbers(-0x234, 0x123);

    compare_with_numbers(-0x123, -0x234);
    compare_with_numbers(-0x234, -0x123);

    return 0;
}
