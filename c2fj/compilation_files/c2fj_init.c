#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

#include "c2fj_syscall.h"


extern uint32_t _stack_end;
extern uint32_t _sdata;
extern uint32_t __heap_start;
extern void __libc_init_array(void);
extern void __libc_fini_array(void);
extern int main();


caddr_t sbrk(int incr) {
    asm volatile ("jal %0, .+14" : "+r"(incr)::"memory");
    return (caddr_t) incr;  // The fj-sbrk returns the previous address in the same register.
}

void exit(int status) {
    asm volatile ("jal %0, .+10" ::"r"(status):"memory");
    __builtin_unreachable();
}

int close(int file) {
    return -1;
}

int fstat(int file, struct stat *st) {
    st->st_mode = S_IFCHR;

    return 0;
}

int isatty(int file) {
    return 1;
}

int lseek(int file, int ptr, int dir) {
    return 0;
}

void kill(int pid, int sig) {
    return;
}

int getpid(void) {
    return -1;
}

int write(int file, const char *ptr, int len) {
    if ((file != 1) && (file != 2)) {
        return -1;
    }

    const char* end_ptr = ptr + len;
    for (; ptr < end_ptr; ptr++) {
        char char_to_print = *ptr;
        c2fj_putc(char_to_print);
    }
    return len;
}

int puts(const char* str) {
    for (char ch = *str; ch; ch = *(++str)) {
        c2fj_putc(ch);
    }
    c2fj_putc('\n');
    return 0;
}

int _putc(char c, FILE* file) {
    (void) file;
    c2fj_putc(c);
    return c;
}

int _getc(FILE* file) {
    (void) file;
    return c2fj_getc();
}


int read(int file, char *ptr, int len) {
    if (file != 0) {
        return -1;
    }

    char* start_ptr = ptr;
    char* end_ptr = ptr + len;
    for (; ptr < end_ptr; ptr++) {
        *ptr = c2fj_getc();
        if (*ptr == '\n') {
            return (ptr - start_ptr) + 1;
        }
    }
    return len;
}


static FILE __stdin = FDEV_SETUP_STREAM(NULL, _getc, NULL, __SRD);
static FILE __stdout = FDEV_SETUP_STREAM(_putc, NULL, NULL, __SWR);
FILE *const stdin = &__stdin;
FILE *const stdout = &__stdout;
__strong_reference(stdout, stderr);


int fputc(int c, FILE* file) {
    if (file != stdout && file != stderr) {
        return EOF;
    }

    c2fj_putc(c);
    return c;
}


__attribute__((naked)) void _start(void) {
    asm volatile ("la sp, _stack_end - 8":::"memory");
    asm volatile ("la gp, _sdata + 0x800":::"memory");
    sbrk((int32_t)&__heap_start - (int32_t)sbrk(0));

    __libc_init_array();
    int status = main();

    __libc_fini_array();
    exit(status);

    while (1);
}
