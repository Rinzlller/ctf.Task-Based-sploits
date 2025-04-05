BITS 64
global _start

_start:

    xchg esi, edi
    inc edi
    mov al, 40
    syscall