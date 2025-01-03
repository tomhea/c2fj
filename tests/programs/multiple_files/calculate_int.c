extern int c;
extern int d;


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

    return a;
}
