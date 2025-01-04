#include <stdio.h>
#include <stdlib.h>
#include "c2fj_syscall.h"


int main() {
    char name[20] = {0};
    printf("Enter your name: ");
    scanf("%19s", name);
    printf("Hello %s!\n", name);
    return 0;
}
