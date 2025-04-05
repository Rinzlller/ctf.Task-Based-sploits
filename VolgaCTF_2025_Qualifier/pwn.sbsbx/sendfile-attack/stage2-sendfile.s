BITS 64
global _start

_start:

    lea rdi, [rsp+0x8]
    mov al, 2
    syscall
    ret