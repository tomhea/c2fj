#include <stdint.h>
#include "c2fj_syscall.h"


#define PRINT_A2 "jal a2, .+22\n"
#define PRINT_LN "jal a2, .+3042\n"


void test_slt() {
    asm volatile(
        "lui a0, 0x12345\n"
        "addi a0, a0, 0x678\n"

        "slti a2, a0, 0\n"
        PRINT_A2
        "slti a2, a0, -1\n"
        PRINT_A2
        "sltiu a2, a0, 0\n"
        PRINT_A2
        "sltiu a2, a0, -1\n"
        PRINT_A2
        PRINT_LN

        "lui a0, 0x00000\n"
        "addi a0, a0, 0x123\n"

        "slti a2, a0, 0\n"
        PRINT_A2
        "slti a2, a0, -1\n"
        PRINT_A2
        "slti a2, a0, 0x400\n"
        PRINT_A2
        "sltiu a2, a0, 0\n"
        PRINT_A2
        "sltiu a2, a0, -1\n"
        PRINT_A2
        "sltiu a2, a0, 0x400\n"
        PRINT_A2
        PRINT_LN

        "addi a0, zero, -0xA0\n"

        "slti a2, a0, 0\n"
        PRINT_A2
        "slti a2, a0, -1\n"
        PRINT_A2
        "slti a2, a0, 0x400\n"
        PRINT_A2
        "slti a2, a0, -0x400\n"
        PRINT_A2
        "sltiu a2, a0, 0\n"
        PRINT_A2
        "sltiu a2, a0, -1\n"
        PRINT_A2
        "sltiu a2, a0, 0x400\n"
        PRINT_A2
        "sltiu a2, a0, -0x400\n"
        PRINT_A2
        PRINT_LN
    :::"memory");
}

void test_shifts() {
    asm volatile(
        "lui a0, 0x12345\n"
        "addi a0, a0, 0x678\n"

        "slli a2, a0, 0\n"
        PRINT_A2
        "slli a2, a0, 1\n"
        PRINT_A2
        "slli a2, a0, 4\n"
        PRINT_A2
        "slli a2, a0, 5\n"
        PRINT_A2
        "slli a2, a0, 28\n"
        PRINT_A2
        "slli a2, a0, 31\n"
        PRINT_A2
        PRINT_LN

        "srli a2, a0, 0\n"
        PRINT_A2
        "srli a2, a0, 1\n"
        PRINT_A2
        "srli a2, a0, 4\n"
        PRINT_A2
        "srli a2, a0, 5\n"
        PRINT_A2
        "srli a2, a0, 28\n"
        PRINT_A2
        "srli a2, a0, 31\n"
        PRINT_A2
        PRINT_LN

        "srai a2, a0, 0\n"
        PRINT_A2
        "srai a2, a0, 1\n"
        PRINT_A2
        "srai a2, a0, 4\n"
        PRINT_A2
        "srai a2, a0, 5\n"
        PRINT_A2
        "srai a2, a0, 28\n"
        PRINT_A2
        "srai a2, a0, 31\n"
        PRINT_A2
        PRINT_LN

        "lui a0, 0x87654\n"
        "addi a0, a0, 0x321\n"

        "slli a2, a0, 0\n"
        PRINT_A2
        "slli a2, a0, 1\n"
        PRINT_A2
        "slli a2, a0, 4\n"
        PRINT_A2
        "slli a2, a0, 5\n"
        PRINT_A2
        "slli a2, a0, 28\n"
        PRINT_A2
        "slli a2, a0, 31\n"
        PRINT_A2
        PRINT_LN

        "srli a2, a0, 0\n"
        PRINT_A2
        "srli a2, a0, 1\n"
        PRINT_A2
        "srli a2, a0, 4\n"
        PRINT_A2
        "srli a2, a0, 5\n"
        PRINT_A2
        "srli a2, a0, 28\n"
        PRINT_A2
        "srli a2, a0, 31\n"
        PRINT_A2
        PRINT_LN

        "srai a2, a0, 0\n"
        PRINT_A2
        "srai a2, a0, 1\n"
        PRINT_A2
        "srai a2, a0, 4\n"
        PRINT_A2
        "srai a2, a0, 5\n"
        PRINT_A2
        "srai a2, a0, 28\n"
        PRINT_A2
        "srai a2, a0, 31\n"
        PRINT_A2
        PRINT_LN
    :::"memory");
}

void test_regular_alu() {
    asm volatile(
        "lui a0, 0x12345\n"
        "addi a0, a0, 0x678\n"

        "addi a2, a0, 0x111\n"
        PRINT_A2
        "addi a2, a0, -0x111\n"
        PRINT_A2
        "addi a2, a0, 0\n"
        PRINT_A2
        "addi a2, a0, -0x679\n"
        PRINT_A2
        "addi a2, zero, 0x111\n"
        PRINT_A2
        PRINT_LN

        "xori a2, a0, -0x1\n"
        PRINT_A2
        "xori a2, a0, -0x10\n"
        PRINT_A2
        "xori a2, a0, 0x0\n"
        PRINT_A2
        "xori a2, a0, 0x135\n"
        PRINT_A2
        PRINT_LN

        "ori a2, a0, -0x1\n"
        PRINT_A2
        "ori a2, a0, -0x10\n"
        PRINT_A2
        "ori a2, a0, 0x0\n"
        PRINT_A2
        "ori a2, a0, 0x135\n"
        PRINT_A2
        PRINT_LN

        "andi a2, a0, -0x1\n"
        PRINT_A2
        "andi a2, a0, -0x10\n"
        PRINT_A2
        "andi a2, a0, 0x0\n"
        PRINT_A2
        "andi a2, a0, 0x135\n"
        PRINT_A2
        PRINT_LN
    :::"memory");
}


int main() {
    test_regular_alu();
    test_shifts();
    test_slt();

    return 0;
}
