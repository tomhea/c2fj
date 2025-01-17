#include <stdio.h>


int main() {
    volatile double x = 1.23;
    volatile double y = 4.56;
    volatile double ans = x * y;
    printf("1.23 * 4.56 == %.5f\n", ans);
    return 0;
}
