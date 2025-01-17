#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


int main() {
    printf("Calculate primes up to: ");
    int max_number;
    scanf("%d", &max_number);

    if (max_number < 0) {
        return 1;
    }
    if (max_number <= 1) {
        return 0;
    }
    printf("2\n");

    bool* non_prime = malloc(max_number + 1);
    for (int i = 0; i <= max_number; i++) {
        non_prime[i] = false;
    }

    for (int p = 3; p <= max_number; p += 2) {
        if (non_prime[p] == false) {
            for (int i = p*p; i <= max_number; i += p) {
                non_prime[i] = true;
            }
            printf("%d\n", p);
        }
    }

    free(non_prime);
    return 0;
}
