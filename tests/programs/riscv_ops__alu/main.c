#include <stdint.h>
#include "c2fj_syscall.h"


#define PRINT_A2 "jal a2, .+22\n"
#define PRINT_LN "jal a2, .+3042\n"


void test_slt() {
    asm volatile(
        "lui a0, 0x12345\n"
        "addi a0, a0, 0x678\n"

        "addi a1, zero, 0\n"
        "slt a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -1\n"
        "slt a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0\n"
        "sltu a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -1\n"
        "sltu a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "lui a0, 0x00000\n"
        "addi a0, a0, 0x123\n"

        "addi a1, zero, 0\n"
        "slt a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -1\n"
        "slt a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x400\n"
        "slt a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0\n"
        "sltu a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -1\n"
        "sltu a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x400\n"
        "sltu a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "addi a0, zero, -0xA0\n"

        "addi a1, zero, 0\n"
        "slt a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -1\n"
        "slt a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x400\n"
        "slt a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -0x400\n"
        "slt a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0\n"
        "sltu a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -1\n"
        "sltu a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x400\n"
        "sltu a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -0x400\n"
        "sltu a2, a0, a1\n"
        PRINT_A2
        PRINT_LN
    :::"memory");
}

void test_shifts() {
    asm volatile(
        "lui a0, 0x12345\n"
        "addi a0, a0, 0x678\n"

        "addi a1, zero, 0\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 1\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 4\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 5\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 69\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 28\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 31\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "addi a1, zero, 0\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 1\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 4\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 5\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 69\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 28\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 31\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "addi a1, zero, 0\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 1\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 4\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 5\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 69\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 28\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 31\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "lui a0, 0x87654\n"
        "addi a0, a0, 0x321\n"

        "addi a1, zero, 0\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 1\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 4\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 5\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 69\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 28\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 31\n"
        "sll a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "addi a1, zero, 0\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 1\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 4\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 5\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 69\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 28\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 31\n"
        "srl a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "addi a1, zero, 0\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 1\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 4\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 5\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 69\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 28\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 31\n"
        "sra a2, a0, a1\n"
        PRINT_A2
        PRINT_LN
    :::"memory");
}

void test_regular_alu() {
    asm volatile(
        "lui a0, 0x12345\n"
        "addi a0, a0, 0x678\n"

        "addi a1, zero, 0x111\n"
        "add a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -0x111\n"
        "add a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0\n"
        "add a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -0x679\n"
        "add a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x111\n"
        "add a2, zero, a1\n"
        PRINT_A2
        "lui a1, 0xEDCBB\n"
        "addi a1, a1, -0x677\n"
        "add a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "addi a1, zero, 0x111\n"
        "sub a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -0x111\n"
        "sub a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0\n"
        "sub a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x679\n"
        "sub a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -0x679\n"
        "sub a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x111\n"
        "sub a2, zero, a1\n"
        PRINT_A2
        "lui a1, 0x12345\n"
        "addi a1, a1, 0x679\n"
        "sub a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "addi a1, zero, -0x1\n"
        "xor a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -0x10\n"
        "xor a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x0\n"
        "xor a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x135\n"
        "xor a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "addi a1, zero, -0x1\n"
        "or a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -0x10\n"
        "or a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x0\n"
        "or a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x135\n"
        "or a2, a0, a1\n"
        PRINT_A2
        PRINT_LN

        "addi a1, zero, -0x1\n"
        "and a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, -0x10\n"
        "and a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x0\n"
        "and a2, a0, a1\n"
        PRINT_A2
        "addi a1, zero, 0x135\n"
        "and a2, a0, a1\n"
        PRINT_A2
        PRINT_LN
    :::"memory");
}


int main() {
    test_regular_alu();
    test_shifts();
    test_slt();

    // TODO test sub too.
    // TODO think of special cases to test with reg OP reg.

    return 0;
}
