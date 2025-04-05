#Shellcode #seccomp

# Information

| CTF                                                       | Task  | Category | Solves | Points |
| --------------------------------------------------------- | ----- | -------- | ------ | ------ |
| [VolgaCTF 2025 Qualifier](https://ctftime.org/event/2676) | sbsbx | pwn      | 19     | 316    |

Description:
> *Flag is in the current directory and the filename is `flag`.*

Attachments:
- app (ELF 64-bit)

# Overview

Security status of the ELF:
```bash
$ pwn checksec app
[*] '/home/kali/VolgaCTF/pwn.sbsbx/app'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    Stripped:   No
```

I reversed the ELF using IDA Pro and its Hex-Rays decomplier.

Functionality in the ELF:
- sequential reading of three shellcodes with length limitations:
	- 1st shellcode must be **9 bytes** long,
	- 2nd shellcode must be **10 bytes** long,
	- 3rd shellcode must be **9 bytes** long,
- sequential execution of three shellcodes via the *call* instruction.

Seccomp rules:
```python
$ seccomp-tools dump ./app
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x07 0xc000003e  if (A != ARCH_X86_64) goto 0009
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x04 0xffffffff  if (A != 0xffffffff) goto 0009
 0005: 0x15 0x03 0x00 0x00000000  if (A == read) goto 0009
 0006: 0x15 0x02 0x00 0x0000003b  if (A == execve) goto 0009
 0007: 0x15 0x01 0x00 0x00000142  if (A == execveat) goto 0009
 0008: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0009: 0x06 0x00 0x00 0x00000000  return KILL
```

To be clear this denies ❌ us to use `read`, `execve` and `execveat`.

# Exploiting: `sendfile`

Plan of attack:
1. 1st shellcode → put the string "*flag*" (filename) on the stack,
2. 2nd shellcode → open file "*flag*",
3. 3rd shellcode → print flag from file via `sendfile`.

But we need to run the sploit multiple times until `r10` is fit.

# Exploiting: `readv`

The stack contains the addresses of shellcodes when they are called. We can use it like `iovec` struct for `readv`:
```python
 +0x0000: 0x00000000004018c4  →  ret                ← $rsp
 +0x0008: 0x0000000000000000
 +0x0010: 0x0000000000000000
 +0x0018: 0x00007ffec1045648
 +0x0020: 0x00007fc9dbf10000  →  shellcode (rwx)
 +0x0028: 0x00007fc9dbf11000  →  shellcode (rwx)
 ----------------- iovec struct -----------------
|+0x0030: 0x00007fc9dbf12000  →  shellcode (rwx) |   ← $rax, $rdi
|+0x0038: 0x00000000004bcfd0  →  ret             |   ← $rbp
 ------------------------------------------------
```

Plan of attack:
1. 1st shellcode → prepare future `rdi` for `readv`,
2. 2nd shellcode → call `readv` and read BIG shellcode,
3. 3rd shellcode → jump to BIG shellcode,
4. 4th BIG shellcode → get flag via `pread64` wihout any limitations.