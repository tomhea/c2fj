#include <stdio.h>


extern void __debug_print_registers();

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

    a += b;
    a += c;
    a += d;
    a += e;
    a += f;

    int g = 2;
    __debug_print_registers();
    return a >> g;
}


int main() {
    printf("Hello world\n");
    return calculate_int();
}
