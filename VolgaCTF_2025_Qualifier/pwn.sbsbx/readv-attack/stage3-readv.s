BITS 64
global _start

_start:

    mov    rax,QWORD [rbp-0x8]
    jmp    rax
    nop
    nop
    nop