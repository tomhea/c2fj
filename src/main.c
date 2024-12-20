//#include <stdio.h>


extern void __debug_print_registers();

int c = 0x34;
int d;

int main() {
    static int e = 8;
    static int f;
    unsigned int a = 1;
    int b = 2;

//    printf("Hello world\n");

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

    a += 0xb;
    int g = 2;
    __debug_print_registers();
    return a >> g;
}
