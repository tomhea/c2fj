#include <stdio.h>
#include "c2fj_syscall.h"


int c = 0x34;
int d;


int calculate_int() {
    static int e = 8;
    static int f;
    int a = 1;
    int b = 2;

    a ^= b;
    a |= b;
    a &= b;

    a++;
    b++;
    c++;
    d++;
    e++;
    f++;

    c2fj_debug_p(1);

    a += b;
    a += c;
    a += d;
    a += e;
    a += f;

    int g = 2;
    c2fj_debug_p(2);
    c2fj_print_registers();
    c2fj_debug_p(3);
    c2fj_print_register(g);
    c2fj_debug_p(2);
    c2fj_print_register(a);
    c2fj_debug_p(4);
    c2fj_print_register(a+1);
    c2fj_debug_p(0xff);

    c2fj_print_char('E');
    c2fj_print_char('n');
    c2fj_print_char('d');
    c2fj_print_char('\n');

    c = 3;
    d = 12;
    c *= d;
    a -= c;

    long long x = -3;
    long long y = -3;
    c2fj_print_register((x*y) >> 32);
    c2fj_print_register((x*y) & 0xffffffff);


    int rs1 = 7;
    int rs2 = 3;
    c2fj_print_char('\n');
    c2fj_print_register(rs1 / rs2);
    c2fj_print_register(rs1 % rs2);

    rs1 = 7;
    rs2 = -3;
    c2fj_print_char('\n');
    c2fj_print_register(rs1 / rs2);
    c2fj_print_register(rs1 % rs2);

    rs1 = -7;
    rs2 = 3;
    c2fj_print_char('\n');
    c2fj_print_register(rs1 / rs2);
    c2fj_print_register(rs1 % rs2);

    rs1 = -7;
    rs2 = -3;
    c2fj_print_char('\n');
    c2fj_print_register(rs1 / rs2);
    c2fj_print_register(rs1 % rs2);

    unsigned int u_rs1 = 7;
    unsigned int u_rs2 = 3;
    c2fj_print_char('\n');
    c2fj_print_register(u_rs1 / u_rs2);
    c2fj_print_register(u_rs1 % u_rs2);

    return a >> g;
}


int main() {
    printf("Hello world\n");
    return calculate_int();
}
