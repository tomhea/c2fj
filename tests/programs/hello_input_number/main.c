#include <stdio.h>
#include <stdlib.h>
#include "c2fj_syscall.h"


int main() {
    int my_number;
    printf("Enter your name: ");
    scanf("%d", &my_number);
    printf("Hello %d!\n", my_number);
    return my_number % 100;
}
