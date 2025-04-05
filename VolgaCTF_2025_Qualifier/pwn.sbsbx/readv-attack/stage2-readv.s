BITS 64
global _start

_start:

    mov    al,0x13
    xchg   rsi,rdi
    mov    dl,0x1
    syscall
    ret