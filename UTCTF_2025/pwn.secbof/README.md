# Information

#BufferOverflow #ROP #seccomp

| CTF                                          | Category | Solves | Points |
| -------------------------------------------- | -------- | ------ | ------ |
| [UTCTF 2025](https://ctftime.org/event/2641) | pwn      | 125    | 839    |

Description:

> A buffer overflow, but secure. Flag can be accessed at "./flag.txt"
> By Anthony (@stuckin414141 on discord)

- chal
- Dockerfile
- start.sh

# Overview

Security status of the ELF:

```bash
─$ pwn checksec chal        
[*] '/home/kali/UTCTF/pwn.secbof/chal'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

I reversed the ELF using IDA Pro and its Hex-Rays decomplier.

Functionality in the ELF:
- set seccomp rules,
- read user input and exit.

Based on the Dockerfile, the flag is located on the file system at path `/flag.txt`.

Seccomp rules:

```bash
─$ seccomp-tools dump ./chal
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x01 0x00 0xc000003e  if (A == ARCH_X86_64) goto 0003
 0002: 0x06 0x00 0x00 0x00000000  return KILL
 0003: 0x20 0x00 0x00 0x00000000  A = sys_number
 0004: 0x15 0x00 0x01 0x00000000  if (A != read) goto 0006
 0005: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0006: 0x15 0x00 0x01 0x00000001  if (A != write) goto 0008
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0008: 0x15 0x00 0x01 0x00000002  if (A != open) goto 0010
 0009: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0010: 0x15 0x00 0x01 0x0000003c  if (A != exit) goto 0012
 0011: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0012: 0x06 0x00 0x00 0x00000000  return KILL
```

To be clear this allows us to use `open`, `read`, `write` and `exit`.
# Vulnerability

Simply Buffer Overflow:

```c
void __fastcall main(int argc, const char **argv, const char **envp)
{
  char input[128]; // [rsp+0h] [rbp-80h] BYREF

  setvbuf(stdout, 0LL, 2LL, 0LL);
  setvbuf(stdin,  0LL, 2LL, 0LL);

  install_filter(); //     ← seccomp
  
  printf("Input> ");
  read(0LL, input, 1000LL); //  /!\ BOF
  printf("Flag: ");
}
```

# Exploiting

Plan of attack:
1. ROP *(Return Oriented Programming)*:
	1. `read` the flag filename somewhere in RW memory,
	2. `open` the flag file,
	3. `read` the flag from the file (descriptor),
	4. `write` the flag.