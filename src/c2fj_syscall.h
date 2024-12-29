#pragma once

#include <sys/types.h>


// Stringify macros
#define __TO_STRING_INNER(x) #x
#define __TO_STRING(x) __TO_STRING_INNER(x)


#define __DEBUG_P_VALUE_INNER(p_value) (1002 + 4 * (p_value))
#define __DEBUG_P_VALUE(p_value) __DEBUG_P_VALUE_INNER(p_value)
#define __DEBUG_P_VALUE_STRING(p_value) __TO_STRING(__DEBUG_P_VALUE(p_value))
#define c2fj_debug_p(p_value) asm volatile ("1: jal x0, 1b+" __DEBUG_P_VALUE_STRING(p_value));


#define __PRINT_CHAR_VALUE_INNER(p_value) (3002 + 4 * (p_value))
#define __PRINT_CHAR_VALUE(p_value) __PRINT_CHAR_VALUE_INNER(p_value)
#define __PRINT_CHAR_VALUE_STRING(p_value) __TO_STRING(__PRINT_CHAR_VALUE(p_value))
#define c2fj_print_char(p_value) asm volatile ("1: jal x0, 1b+" __PRINT_CHAR_VALUE_STRING(p_value));


#define __FORCE_INLINE static __attribute__((always_inline)) inline


__FORCE_INLINE void c2fj_print_registers(){
    asm volatile ("1: jal x0, 1b+18");
}

__FORCE_INLINE void c2fj_print_register(int reg) {
    asm volatile ("1: jal %0, 1b+22" ::"r"(reg));
}

__FORCE_INLINE caddr_t _sbrk(int incr) {
    asm volatile ("1: jal %0, 1b+14" : "+r"(incr));
    return (caddr_t) incr;  // The fj-sbrk returns the previous address in the same register.
}

__FORCE_INLINE void _exit(int status) {
    asm volatile ("1: jal %0, 1b+10" ::"r"(status));
    __builtin_unreachable();
}

__FORCE_INLINE void c2fj_putc(const char char_to_print) {
    asm volatile ("1: jal %0, 1b+2" ::"r"(char_to_print));
}

__FORCE_INLINE char c2fj_getc() {
    char new_byte;
    asm volatile ("1: jal %0, 1b+6" : "=r"(new_byte));
    return new_byte;
}
