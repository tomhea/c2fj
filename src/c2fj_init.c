#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

#include "c2fj_syscall.h"


int main();

extern uint32_t _stack_end;


caddr_t _sbrk(int incr) {
    asm volatile ("1: jal %0, 1b+14" : "+r"(incr));
    return (caddr_t) incr;  // The fj-sbrk returns the previous address in the same register.
}

void _exit(int status) {
    asm volatile ("1: jal %0, 1b+10" ::"r"(status));
    __builtin_unreachable();
}

int _close(int file) {
    return -1;
}

int _fstat(int file, struct stat *st) {
    st->st_mode = S_IFCHR;

    return 0;
}

int _isatty(int file) {
    return 1;
}

int _lseek(int file, int ptr, int dir) {
    return 0;
}

void _kill(int pid, int sig) {
    return;
}

int _getpid(void) {
    return -1;
}

int _write(int file, const char *ptr, int len) {
    if ((file != 1) && (file != 2) && (file != 3)) {
        return -1;
    }

    const char* end_ptr = ptr + len;
    for (; ptr < end_ptr; ptr++) {
        char char_to_print = *ptr;
        c2fj_putc(char_to_print);
    }
    return len;
}

int puts(const char *str) {
    int len = strlen(str);
    if (_write(1, str, len) != len) {
        return -1;
    }

    c2fj_putc('\n');
    return 0;
}

int _read(int file, char *ptr, int len) {
    if (file != 0) {
        return -1;
    }

    char* end_ptr = ptr + len;
    for (; ptr < end_ptr; ptr++) {
        *ptr = c2fj_getc();
    }
    return len;
}

__attribute__((naked)) void _start(void) {
    asm volatile ("la sp, _stack_end - 8");

    int status = main();

    _exit(status);

    /* Infinite loop */
    while (1);
}
