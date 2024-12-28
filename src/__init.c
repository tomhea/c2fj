#include <stdarg.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>


int main();


extern int _end;
extern uint32_t _stext;
extern uint32_t _etext;
extern uint32_t _sbss;
extern uint32_t _ebss;
extern uint32_t _sdata;
extern uint32_t _edata;
extern uint32_t _sstack;
extern uint32_t _estack;


// TODO define the "vectors" (the interrupt vectors).


caddr_t _sbrk(int incr) {
    asm volatile ("1: jal %0, 1b+14" : "+r"(incr));
    return (caddr_t) incr;  // The fj-sbrk returns the previous address in the same register.
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

void _exit(int status) {
    asm volatile ("1: jal %0, 1b+10" ::"r"(status));
    __builtin_unreachable();
}

void _kill(int pid, int sig) {
    return;
}

int _getpid(void) {
    return -1;
}

int _write(int file, char *ptr, int len) {
    if ((file != 1) && (file != 2) && (file != 3)) {
        return -1;
    }

    char* end_ptr = ptr + len;
    for (; ptr < end_ptr; ptr++) {
        char char_to_print = *ptr;
        asm volatile ("1: jal %0, 1b+2" ::"r"(char_to_print));
    }
    return len;
}

int _read(int file, char *ptr, int len) {
    if (file != 0) {
        return -1;
    }

    char* end_ptr = ptr + len;
    for (; ptr < end_ptr; ptr++) {
        char byte_was_read;
        asm volatile ("1: jal %0, 1b+6" : "=r"(byte_was_read));
        *ptr = byte_was_read;
    }
    return len;
}


void start(void) {
    int status = main();

    _exit(status);

    /* Infinite loop */
    while (1);
}
