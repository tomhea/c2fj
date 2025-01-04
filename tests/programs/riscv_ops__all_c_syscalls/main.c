#include <stdint.h>
#include <sys/stat.h>
#include "c2fj_syscall.h"


#define PRINT_A2 "jal a2, .+22\n"
extern caddr_t _sbrk(int incr);
extern int _close(int file);
extern int _fstat(int file, struct stat *st);
extern int _isatty(int file);
extern int _lseek(int file, int ptr, int dir);
extern void _kill(int pid, int sig);
extern int _getpid(void);
extern void _exit(int status);
int _write(int file, const char *ptr, int len);
int puts(const char *str);
int _read(int file, char *ptr, int len);


int main() {
    // Tested any function in `c2fj_init.c`, `c2fj_syscall.h`, but the c2fj_print_registers()

    c2fj_debug_p(0);
    c2fj_debug_p(1);
    c2fj_debug_p(0x3A);
    c2fj_debug_p(0xA3);
    c2fj_debug_p(0xFF);
    c2fj_print_char('\n');

    c2fj_print_char('C');
    c2fj_print_char('h');
    c2fj_print_char('a');
    c2fj_print_char('r');
    c2fj_print_char('!');
    c2fj_print_char('\n');

    int c = 'Y';
    c2fj_putc(c);
    c = '\n';
    c2fj_putc(c);

    int x = 0x123456;
    c2fj_print_register(x);
    x--;
    c2fj_print_register(x);

    c = c2fj_getc();
    c2fj_putc(c);
    c2fj_putc(c2fj_getc());

    c2fj_print_char('\n');

    uint32_t orig_sbrk = (uint32_t)_sbrk(0);
    _sbrk(0xfffff124 - orig_sbrk);
    uint32_t new_sbrk = (uint32_t)_sbrk(0);
    _sbrk(orig_sbrk - new_sbrk);
    c2fj_print_register(new_sbrk);
    c2fj_print_register((uint32_t)_sbrk(0) - orig_sbrk);

    c2fj_print_register(_close(7));

    struct stat st;
    st.st_mode = S_IFDIR;
    c2fj_print_register(_fstat(7, &st));
    c2fj_print_register((uint32_t)st.st_mode - (uint32_t)(S_IFCHR));

    c2fj_print_register(_isatty(7));
    c2fj_print_register(_lseek(1, 2, 3));
    _kill(131, 9);
    c2fj_print_register(_getpid());

    c2fj_print_char('\n');

    int res_w0 = _write(0, "Hi0\n", 4);
    c2fj_print_register(res_w0);
    int res_w1 = _write(1, "Hi1\n", 4);
    c2fj_print_register(res_w1);
    int res_w2 = _write(2, "Hi2\n", 4);
    c2fj_print_register(res_w2);
    int res_w3 = _write(3, "Hi3\n", 4);
    c2fj_print_register(res_w3);
    c2fj_print_char('\n');

    int res_p0 = puts("Yooo");
    c2fj_print_register(res_p0);
    int res_p1 = puts("");
    c2fj_print_register(res_p1);
    int res_p2 = puts("Yeah\nMe!\n");
    c2fj_print_register(res_p2);
    c2fj_print_char('\n');

    char buf[20] = {0};
    int res_r0 = _read(0, buf, 4);
    puts(buf);
    c2fj_print_register(res_r0);

    int res_r1 = _read(0, buf, 20);
    puts(buf);
    c2fj_print_register(res_r1);

    int res_r2 = _read(1, buf, 4);
    puts(buf);
    c2fj_print_register(res_r2);

    int res_r3 = _read(0, buf, 4);
    puts(buf);
    c2fj_print_register(res_r3);

    c2fj_print_char('\n');

    _exit(7);
    return 0;
}
