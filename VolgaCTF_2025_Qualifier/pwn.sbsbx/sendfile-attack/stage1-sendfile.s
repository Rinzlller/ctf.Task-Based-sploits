BITS 64
global _start

_start:

    mov DWORD [rsp+0x8], 0x67616c66
    ret