#include <stdio.h>
#include <stdlib.h>
#include "c2fj_syscall.h"


int main() {
    printf("Enter your name: ");
    char name[20] = {0};
    scanf("%9s", name);
    printf("Hello %s!\n", name);
    return 0;
}
