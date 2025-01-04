#include <stdio.h>


int main() {
    volatile int x = 3;
    volatile int y = 7;
    volatile int ans = x * y;
    printf("3 * 7 == %d\n", ans);
    return 0;
}
