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
    static unsigned char *heap = NULL;
    unsigned char *prev_heap;

    if (heap == NULL) {
        heap = (unsigned char *) &_end;
    }
    prev_heap = heap;

    heap += incr;

    return (caddr_t) prev_heap;
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
    // TODO print exit status.
    asm volatile ("__exit_label: jal %0, __exit_label+10" ::"r"(status));
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
        asm volatile ("__write_label: jal %0, __write_label+2" ::"r"(char_to_print));
        // TODO: stl__put_char((uint8_t)*ptr);
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
        asm volatile ("__read_label: jal %0, __read_label+6" ::"r"(byte_was_read));
        *ptr = byte_was_read;
        // TODO: stl__read_char((uint8_t *)ptr);
    }
    return len;
}


void _start(void) {
    /* Copy init values from text to data */
    uint32_t *init_values_ptr = &_etext;
    uint32_t *data_ptr = &_sdata;

    if (init_values_ptr != data_ptr) {
        for (; data_ptr < &_edata;) {
            *data_ptr++ = *init_values_ptr++;
        }
    }

    /* Clear the zero segment */
    for (uint32_t *bss_ptr = &_sbss; bss_ptr < &_ebss;) {
        *bss_ptr++ = 0;
    }

    /* Branch to main function */
    int status = main();

    _exit(status);

    /* Infinite loop */
    while (1);
}
