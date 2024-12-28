#pragma once

# define __FORCE_INLINE __attribute__((always_inline)) inline


__FORCE_INLINE void __debug_print_registers(){
    asm volatile ("1: jal x0, 1b+18");
}

__FORCE_INLINE void __debug_print_register(int reg) {
    asm volatile ("1: jal %0, 1b+22" ::"r"(reg));
}