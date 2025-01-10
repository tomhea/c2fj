#include <stdint.h>
#include "c2fj_syscall.h"


#define PRINT_A2 "jal a2, .+22\n"
#define PRINT_LN "jal a2, .+3042\n"


void test_mul(int32_t a0, int32_t a1) {
    asm volatile (
        "mv a0, %0\n"
        "mv a1, %1\n"

        "mul a2, a0, a1\n"
        PRINT_A2
        "mulh a2, a0, a1\n"
        PRINT_A2
        "mulhsu a2, a0, a1\n"
        PRINT_A2
        "mulhu a2, a0, a1\n"
        PRINT_A2
    ::"r"(a0), "r"(a1) : "a0", "a1", "a2", "memory");
    c2fj_print_char('\n');
}


void test_div_rem(int32_t a0, int32_t a1) {
    asm volatile (
        "mv a0, %0\n"
        "mv a1, %1\n"

        "div a2, a0, a1\n"
        PRINT_A2
        "rem a2, a0, a1\n"
        PRINT_A2
        "divu a2, a0, a1\n"
        PRINT_A2
        "remu a2, a0, a1\n"
        PRINT_A2
    ::"r"(a0), "r"(a1) : "a0", "a1", "a2", "memory");
    c2fj_print_char('\n');
}


int main() {
    test_mul(0x1110, 0x1112);
    test_mul(0x11111110, 0x11111112);
    test_mul(-0x11, 0x76543210);
    test_mul(0x76543210, -0x11);
    test_mul(-0x76543218, -0x76543);

    test_div_rem(20, 12);
    test_div_rem(20, -12);
    test_div_rem(-20, 12);
    test_div_rem(-20, -12);
    test_div_rem(0x87654321, 0x12345678);
    test_div_rem(0x87654321, -0x13);

    return 0;
}
