#include <stdio.h>
#include <stdint.h>
#include <sys/stat.h>
#include "c2fj_syscall.h"


#define PRINT_A2 "jal a2, .+22\n"
extern caddr_t sbrk(int incr);
extern int close(int file);
extern int fstat(int file, struct stat *st);
extern int isatty(int file);
extern int lseek(int file, int ptr, int dir);
extern void kill(int pid, int sig);
extern int getpid(void);
extern void exit(int status);

extern int write(int file, const char *ptr, int len);
extern int puts(const char *str);
extern int read(int file, char *ptr, int len);
extern int fputc(int c, FILE* file);
extern int _getc(FILE* file);
extern int _putc(char c, FILE* file);


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
    c2fj_putc(c2fj_getc());  // read & print newline

    c2fj_print_char('\n');

    uint32_t orig_sbrk = (uint32_t)sbrk(0);
    sbrk(0xfffff124 - orig_sbrk);
    uint32_t new_sbrk = (uint32_t)sbrk(0);
    sbrk(orig_sbrk - new_sbrk);
    c2fj_print_register(new_sbrk);
    c2fj_print_register((uint32_t)sbrk(0) - orig_sbrk);

    c2fj_print_register(close(7));

    struct stat st;
    st.st_mode = S_IFDIR;
    c2fj_print_register(fstat(7, &st));
    c2fj_print_register((uint32_t)st.st_mode - (uint32_t)(S_IFCHR));

    c2fj_print_register(isatty(7));
    c2fj_print_register(lseek(1, 2, 3));
    kill(131, 9);
    c2fj_print_register(getpid());

    c2fj_print_char('\n');

    int res_w0 = write(0, "Hi0\n", 4);
    c2fj_print_register(res_w0);
    int res_w1 = write(1, "Hi1\n", 4);
    c2fj_print_register(res_w1);
    int res_w2 = write(2, "Hi2\n", 4);
    c2fj_print_register(res_w2);
    int res_w3 = write(3, "Hi3\n", 4);
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
    int res_r0 = read(0, buf, 4);
    puts(buf);
    c2fj_print_register(res_r0);

    int res_r1 = read(0, buf, 20);
    puts(buf);
    c2fj_print_register(res_r1);

    int res_r2 = read(1, buf, 4);
    puts(buf);
    c2fj_print_register(res_r2);

    int res_r3 = read(0, buf, 4);
    puts(buf);
    c2fj_print_register(res_r3);

    c2fj_print_char('\n');

    char ch;

    int res_putc0 = _putc('a', stdin);
    int res_putc1 = _putc('b', stdout);
    int res_putc2 = _putc('c', stderr);
    ch = 'A';
    int res_putc3 = _putc(ch, stdout);
    ch++;
    int res_putc4 = _putc(ch, stdout);
    c2fj_print_char('\n');
    c2fj_print_register(res_putc0);
    c2fj_print_register(res_putc1);
    c2fj_print_register(res_putc2);
    c2fj_print_register(res_putc3);
    c2fj_print_register(res_putc4);
    c2fj_print_char('\n');

    int res_fputc0 = fputc('a', stdin);
    int res_fputc1 = fputc('b', stdout);
    int res_fputc2 = fputc('c', stderr);
    ch = 'A';
    int res_fputc3 = fputc(ch, stdout);
    ch++;
    int res_fputc4 = fputc(ch, stdout);
    c2fj_print_char('\n');
    c2fj_print_register(res_fputc0);
    c2fj_print_register(res_fputc1);
    c2fj_print_register(res_fputc2);
    c2fj_print_register(res_fputc3);
    c2fj_print_register(res_fputc4);
    c2fj_print_char('\n');

    _putc(_getc(stdin), stdout);
    _putc(_getc(stdout), stdout);  // works, not validated.
    _putc(_getc(stderr), stdout);  // works, not validated.
    ch = _getc(stdin);
    ch++;
    _putc(ch, stdout);
    _putc(_getc(stdin), stdout);  // read & print newline
    c2fj_print_char('\n');

    exit(7);
    return 0;
}
