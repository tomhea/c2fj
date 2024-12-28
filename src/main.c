#include <stdio.h>
#include "debug_c2fj.h"


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
    return a >> g;
}


int main() {
    printf("Hello world\n");
    return calculate_int();
}
